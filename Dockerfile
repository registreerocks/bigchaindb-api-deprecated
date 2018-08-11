FROM python:3.6

#SSL
# RUN openssl req \
#     -new \
#     -newkey rsa:4096 \
#     -days 365 \
#     -nodes \
#     -x509 \
#     -subj "/C=ZA/ST=WC/L=CapeTown/O=Registree/CN=www.registree.rocks" \
#     -keyout server.key \
#     -out server.cert

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
RUN mkdir -p /usr/src/app
COPY ./package /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -e .

EXPOSE 8080

CMD ["python3", "-m", "swagger_server"]