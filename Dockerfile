FROM 856809629398.dkr.ecr.us-east-1.amazonaws.com/python:3.8

RUN mkdir -p /opt/logs/af-scanner-service/

RUN mkdir /localite-user-service-backend

WORKDIR /opt/logs/localite-user-service/

RUN touch app.log

WORKDIR /localite-user-service-backend

COPY . /localite-user-service-backend/

RUN apt-get update -y

RUN apt-get -y install wget vim jq

RUN apt-get -y install sudo

ENV PATH $PATH:/usr/local/bin

RUN pip3 install -r requirements.txt

EXPOSE 3000

RUN chmod +x pystart.sh

CMD [ "bash", "pystart.sh"]
