# This docker file defines the main API for the bigchainDB_API.
# The container is built and run via the docker-compose file
# wherein the container is named "bigchaindb_api".
# Supervisord is used to start Gunicorn to run the Swagger/Flask
# API that is used to call functions from BigchainDB that runs 
# over the tendermint protocol to synchronize mongodbs

FROM python:3.6

RUN  apt-get update -y && \
    apt-get upgrade -y 

# API
RUN mkdir -p /usr/src/package
COPY ./package /usr/src/package
WORKDIR /usr/src/package
RUN pip install -e .

# Deployment
RUN apt-get install supervisor -y
RUN pip install gunicorn

# Supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start processes
CMD ["/usr/bin/supervisord"]