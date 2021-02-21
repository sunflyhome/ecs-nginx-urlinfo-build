#Use CentOS 8 as the container OS
FROM centos:7

#Copy our files to the container
COPY . ./app

#Install python and other programs required to run our app
RUN yum install -y python3 python3-libs python3-devel python3-pip which gcc

#Change the working directory to /app
WORKDIR /app

#Changing the default python version from 2 to 3. We do this by first renaming the old python version and linking python filename to python3.
RUN mv /usr/bin/python /usr/bin/python_old
RUN cd /usr/bin && ln -s python3 python

#Install the required python packages listed in the requirements file
RUN python -m pip install -r requirements.txt

#Expose port 8080 of the container to the outside
EXPOSE 8080
#Run uwsgi with the configuration in the .ini file
CMD ["uwsgi","--ini","app.ini", \
               "--plugins", "python3", \
               "--protocol", "uwsgi"]

