import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from pymongo import MongoClient

ADMIN = generate_keypair()
BDB = BigchainDB('http://bigchaindb:9984')
MC = MongoClient('mongodb', 27017)
MDB = MC.bigchain