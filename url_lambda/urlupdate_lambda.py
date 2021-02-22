import boto3
import re
import json
import requests
from requests_aws4auth import AWS4Auth




# Lambda execution starts here
def handler(event, context):
    for record in event['Records']:
        # Regular expressions used to parse some url lines
        url_pattern=re.compile('(^http.*)')
        
        region = 'us-west-2'
        service = 'es'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

        host = 'https://vpc-malware-url-repo-2g5a7onmridquyi3hcxkw7kkwq.us-west-2.es.amazonaws.com'
        index = 'lambda-url-index'
        type = 'lambda-type'
        url = host + '/' + index + '/' + type

        headers = { "Content-Type": "application/json" }

        s3 = boto3.client('s3')
        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Get, read, and split the file into lines
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj['Body'].read().decode('utf-8')
        lines = body.splitlines()
        
        # Match the regular expressions to each line and index the JSON
        for line in lines:
            spam_url_each = url_pattern.search(line).group(1)
            
            document = { "url": spam_url_each, "file": key}
           
            print(document)
            r = requests.post(url, auth=awsauth, json=document, headers=headers)
            print(r)
