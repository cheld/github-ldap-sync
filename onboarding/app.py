import os
from flask import Flask, Response, render_template, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
  data = dict(
    org_name=os.environ['GITHUB_ORG_NAME'],
    company=os.environ['COMPANY'],
  )

  return render_template("main.html", data=data)

@app.route('/error')
def error():
  return render_template("error.html")

@app.route('/add', methods=['PUT'])
def add():
  
  org_name = os.environ['GITHUB_ORG_NAME']
  username = request.json['username']
  email = request.json['email']
  success = False

 
  result = None
  if success:
    result = dict(
        url="https://github.com/orgs/{org_name}/invitation".format(org_name=org_name)
    )
  else:
    result = dict(
        url="/error"
    )

  return jsonify(result), 200

if __name__ == "__main__":
  
  # Load environment variables from the .env file
  load_dotenv()
  
  app.run(host="0.0.0.0")