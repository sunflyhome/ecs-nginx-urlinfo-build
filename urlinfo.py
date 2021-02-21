from flask import Flask, render_template
import boto3
import re
import requests
from requests_aws4auth import AWS4Auth
import os
import json
import hashlib

from markupsafe import escape
urlinfo = Flask(__name__)

@urlinfo.route('/', methods=['GET'])
def home():
    return "Welcome"

@urlinfo.route('/1/<path:subpath>', methods=['GET'])

def mypage(subpath):
    url_to_serach = escape(subpath)
    
    region = 'us-west-2'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    host = 'https://vpc-malware-url-repo-2g5a7onmridquyi3hcxkw7kkwq.us-west-2.es.amazonaws.com:9200'
    index = 'lambda-url-index'
    type = 'lambda-type'
    url = host + '/' + index + '/_search'
    query = {
            "query":{
                "bool" : {
                    "must" : {
                        "term" : { "url.keyword" : url_to_serach}
                    }
                }
            }
    }
    headers = { "Content-Type": "application/json"}
    url = host + '/' + index + '/_search'
    result = json.loads(requests.get(url, headers=headers, data=json.dumps(query)).text) 
    # Return True if url is listed as malware from ElasticSearch 
    if result['hits']['total']['value'] > 0:
        return 'True'
    else:
        return 'False'


    
    