from flask import Flask, render_template
import boto3
import requests
from requests_aws4auth import AWS4Auth
import json


from markupsafe import escape
url_all_in_one = Flask(__name__)

@url_all_in_one .route('/', methods=['GET'])
def home():
    return "Welcome"

@url_all_in_one .route('/urlinfo/1/<path:subpath>', methods=['GET'])

def urlinfo_page(subpath):
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
        return json.dumps({'Found':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'Found':False}), 200, {'ContentType':'application/json'}
@url_all_in_one .route('/urlupdate/<path:subpath>', methods=['GET'])

def urlupdate_page(subpath):
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
    res = requests.post(url, auth=awsauth, json=document, headers=headers)
    res = json.loads(res.text)
    if res['_shards']['failed'] == 0:
        return json.dumps({'Added':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'Added':False}), 200, {'ContentType':'application/json'}


    
    