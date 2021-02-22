== Test Process ==

* Query url ( ayy URL in urls.test.db):

http://urlchecker-16047262.us-west-2.elb.amazonaws.com/urlinfo/1/<url_link>
http://urlchecker-16047262.us-west-2.elb.amazonaws.com/urlinfo/1/http://omega.az/IRS/vGuy-lNs5_lcfNoI-xFr/

Return {"Found": true}

http://urlchecker-16047262.us-west-2.elb.amazonaws.com/urlinfo/1/http://omega.az/IRS/vGuy-lNs5_lcfNoI/

Return {"Found": false}

* Add new url

http://urlchecker-16047262.us-west-2.elb.amazonaws.com/update/1/http://omega.az/IRS/vGuy-lNs5test/

Return {"Added": true}

* System monitor:
http://urlchecker-16047262.us-west-2.elb.amazonaws.com/

Return Welcome

== Service Description ==

Single url_all_in_one.py talks to AWS Elastic Search for indexed text search. Current search pattern in the code set as exact match.

AWS Elastic Search service (AES) is currently hosted in AWS based on Apache Lucene. URL data for test have been pre-loaded into AES via S3 and Lambda function under url_lambda. It also proved quick and fast bulk urls process into search engine while file was uploaded to s3 bucket and s3 triggered lambda function to insert urls.

url_all_in_one.py is built into container with Flask and uWsgi on Centos 7

== Infra Description ==

The container is currently pushed to AWS ECS service into Cluster:  URL-INFO-CLUSTER 

The cluster includes one service and one task to deploy container to EC2 instances in default VPC.

Ec2 instances ( 2 of T2a.small) are being placed behind AWS Elastic Load balancer(ELB) with port 80. 

ELB forwards port 80 to container's service, port 8080.

Container service, based on the path (either urlinfo or urlupdate), send request to ElasticSearch service hosted by a T3.small as demo.

Client -> ELB(port 80) -> Autoscalling group ( 2 instances) -> Target group ( ecs-URL-IN-url-check-sev port 8080)

== Future Improment ==

urlupdate should support POST with BULK file.

Migration all resources from manual creation to Cloudformation stack. ( sameple , ecs_cf_temlate.yml)

Add autoscaling poloicy to elasticlly scaleup based on Ec2 instance CPU , network or Mem usage 

Migrate from http to https with cerificate created from ACM.

Added auth for GET request

== Reference ==

Local Test (vpc endpoint uses 9002 from local dev host to AWS ec2 instance via port-forward ):
https://and1zero.github.io/tech/2019/03/12/connecting-to-aws-elasticsearch-vpc-locally/

Create docker container on AWS:
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_AWSCLI_EC2.html







