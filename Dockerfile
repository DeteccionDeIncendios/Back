FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y build-essential python3-pip


#Create the working directory
RUN set -ex && mkdir /app
WORKDIR /app

#Copy only the relevant directories to the working directory
COPY ./ ./app

#Install Python dependencies
RUN set -ex && pip3 install -r app/requirements.txt

#Run the web server
EXPOSE 8080
ENV PYTHONPATH /app
CMD python3 ./app/app.py
