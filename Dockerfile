# This docker file defines the main API for the bigchainDB_API.
# The container is built and run via the docker-compose file
# wherein the container is named "bigchaindb_api".
# Supervisord is used to start Gunicorn to run the Swagger/Flask
# API that is used to call functions from BigchainDB that runs 
# over the tendermint protocol to synchronize mongodbs

FROM python:3.6

# connexion
RUN mkdir -p /usr/src
COPY oas3.zip /usr/src
WORKDIR /usr/src

RUN  apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install unzip -y 

RUN unzip oas3.zip
RUN mv connexion-oas3 connexion
WORKDIR connexion
RUN pip install -e .

# API
RUN mkdir -p /usr/src/package
COPY ./package /usr/src/package
WORKDIR /usr/src/package
RUN pip install -e .

# Deployment
# RUN apt-get install nginx supervisor -y
RUN apt-get install supervisor -y
RUN pip install gunicorn


# Supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# EXPOSE 8080

# Start processes
CMD ["/usr/bin/supervisord"]