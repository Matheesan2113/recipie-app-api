# Alpine is docker
# Alpine is lightweight and fast to compile image
FROM python:3.7-alpine
# Optional, useful to figure out who's maintaing the project
MAINTAINER London App Developer Ltd

# Set Env VAR
ENV PYTHONUNBUFFERED 1
# copy requirements file, to dockerimage
COPY ./requirements.txt /requirements.txt
# Runs PIP install, and stores it in requirements text file
RUN pip install -r /requirements.txt

#Create empty folder, sqqitch to that directory, 
#copy from local machine to docker image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

#Create user for running applications ONLY
#For security purposes, so that you're not running the docker on a root account
#Createing seperate user reduces scope of application
RUN adduser -D user
USER user

