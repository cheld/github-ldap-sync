import os
from flask import Flask, Response, render_template, request, jsonify, make_response
from dotenv import load_dotenv
import re
import traceback

from shared.github_service import GithubService
from shared.storage_service import StorageService

# Load environment variables from the .env file
load_dotenv()
page_data = dict(
    title=os.environ['PAGE_TITLE'],
    company=os.environ['PAGE_COMPANY'],
    contact=os.environ['PAGE_CONTACT'],
    org_name=os.environ['GITHUB_ORG_NAME'],
)
EMAIL_REGEX = os.environ['VALIDATION_EMAIL_REGEX']
GH_ORG_NAME = os.environ['GITHUB_ORG_NAME'],

app = Flask(__name__)
github = GithubService()
storage = StorageService.create()
storage.init()


@app.route('/', methods=['GET'])
def index_page():
  return render_template("main.html", data=page_data)


@app.route('/error', methods=['GET'])
def error_page():
    return render_template("error.html", data=page_data)


@app.route('/api/invite', methods=['PUT'])
def invite():
    try:
        gh_account_login = request.json['username']
        ldap_email = request.json['email']

        if len(gh_account_login)>40:
            response_data = {'error': f"Github account name must be shorter than 40 characters"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)
        if not re.match(EMAIL_REGEX, ldap_email):
            response_data = {'error': f"Allianz email must be used, following the pattern {EMAIL_REGEX}"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)
        
        # Validate email
        #TODO

        # Clean-up previously onboarded github users
        github.open()
        existing_id, existing_login = storage.search_gh_account(ldap_email)
        if existing_id is not None:
            cleanup_succ, msg = github.remove_from_organization(existing_id, existing_login)
            if not cleanup_succ:
                raise Exception(f"Warning. Clean up of account {existing_login} for {ldap_email} failed. Reason: {msg}")

        # Join the organization and store the result   
        success, gh_account_id, msg = github.join_organization(gh_account_login)
        if success:
            storage.onboard_gh_account(ldap_email, gh_account_id, gh_account_login, GH_ORG_NAME)

        # Generate http response code
        if success:
            response_data = {'message': msg}
            status_code = 200
        else:
            response_data = {'error': msg}
            status_code = 400  
        return make_response(jsonify(response_data), status_code)

    except Exception as e:
        traceback.print_exc() 
        return make_response(jsonify({'error': "Operation failed for an unknown reason"}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0")