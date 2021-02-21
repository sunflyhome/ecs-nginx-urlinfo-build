import boto3
import re
import requests
from requests_aws4auth import AWS4Auth
import os

region = 'us-west-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://vpc-malware-url-repo-2g5a7onmridquyi3hcxkw7kkwq.us-west-2.es.amazonaws.com:9200'
index = 'lambda-url-index'
type = 'lambda-type'
url = host + '/' + index + '/' + type

headers = { "Content-Type": "application/json" }

s3 = boto3.client('s3')

# Regular expressions used to parse some url lines

url_pattern=re.compile('(^http.*)')

filename='./urls.test.db'
f=open(filename,'r')
lines=f.readlines()
for line in lines:
            spam_url_each = url_pattern.search(line).group(1)
            
            document = { "url": spam_url_each}
            
            r = requests.post(url, auth=awsauth, json=document, headers=headers)
print('Upload Done')