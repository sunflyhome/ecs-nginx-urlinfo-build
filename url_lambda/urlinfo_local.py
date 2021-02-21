import boto3
import re
import requests
from requests_aws4auth import AWS4Auth
import json


region = 'us-west-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://vpc-spam-url-repo-22kk5cayfefx6bji3vup5pjuzy.us-west-2.es.amazonaws.com:9200'
index = 'lambda-url-index'
type = 'lambda-type'
url = host + '/' + index + '/_search'
query ={
        "query":{
                    "match": {
                      "url"  :"http://195.5.3.102:44446/bin.sh"
                      }
        },
          "size": 1
}
headers = { "Content-Type": "application/json" }
url = host + '/' + index + '/_search'
result = json.loads(requests.get(url, headers=headers, data=json.dumps(query)).text)    
if result:
    return result
else:
    return result