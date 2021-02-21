=Test Steps =

== URL update ==
http://<elb_address>/urlupdate/<FullUrl>

For exampe:
http://<elb_address>/urlupdate/http://p6.zbjimg.com/task/2011-10/14/1121109/4e97e74d5dd8e.7z

It will insert url into ElasticSearch cluster


== URL Validate ==
http://<elb_address>/urlinfo/1/<FullUrl>

For exampe:
http://<elb_address>/urlinfo/1/http://p6.zbjimg.com/task/2011-10/14/1121109/4e97e74d5dd8e.7z

It returns Ture when url is listed as malware , False if it's not listed 




