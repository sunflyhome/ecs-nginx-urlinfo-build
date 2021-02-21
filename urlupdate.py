from flask import Flask, render_template
import boto3
import re
import requests
from requests_aws4auth import AWS4Auth


from markupsafe import escape
urlupdate = Flask(__name__)

@urlupdate.route('/', methods=['GET'])
def home():
    return "Welcome"

@urlupdate.route('/<path:subpath>', methods=['GET'])

def mypage(subpath):
    url_to_add = escape(subpath)
    
    region = 'us-west-2'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    host = 'https://vpc-malware-url-repo-2g5a7onmridquyi3hcxkw7kkwq.us-west-2.es.amazonaws.com:9200'
    index = 'lambda-url-index'
    type = 'lambda-type'
    url = host + '/' + index + '/' + type
    
    headers = { "Content-Type": "application/json"}
    
    document = { "url": url_to_add}            
    r = requests.post(url, auth=awsauth, json=document, headers=headers)
    
    return "OK"
        
        