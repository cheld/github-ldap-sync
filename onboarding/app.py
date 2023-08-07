import os
from flask import Flask, Response, render_template, request, jsonify, make_response
from dotenv import load_dotenv
import re

from githubmanager import GithubManager
from storagemanager import StorageManager

# Load environment variables from the .env file
load_dotenv()
page_data = dict(
    title=os.environ['PAGE_TITLE'],
    company=os.environ['PAGE_COMPANY'],
    contact=os.environ['PAGE_CONTACT'],
    org_name=os.environ['GITHUB_ORG_NAME'],
)
EMAIL_REGEX = os.environ['VALIDATION_EMAIL_REGEX']

app = Flask(__name__)
github = GithubManager()
storage = StorageManager() 


@app.route('/', methods=['GET'])
def index_page():
  return render_template("main.html", data=page_data)


@app.route('/error', methods=['GET'])
def error_page():
    return render_template("error.html", data=page_data)


@app.route('/api/invite', methods=['PUT'])
def invite():
    try:
        username = request.json['username']
        email = request.json['email']

        if len(username)>40:
            response_data = {'error': f"Github account name must be shorter than 40 characters"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)
        if not re.match(EMAIL_REGEX, email):
            response_data = {'error': f"Allianz email must be used, following the pattern {EMAIL_REGEX}"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)

        # Join the organization and store the result
        github.open()
        success, msg = github.join_organization(username)
        if success:
            storage.set_user_onboarded(username, email)

        # Generate http response code
        if success:
            response_data = {'message': msg}
            status_code = 200
        else:
            response_data = {'error': msg}
            status_code = 400  
        return make_response(jsonify(response_data), status_code)

    except Exception as e:
        print(e)
        return make_response(jsonify({'error': "Operation failed for an unknown reason"}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0")