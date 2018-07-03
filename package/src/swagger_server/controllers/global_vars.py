import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

ADMIN = generate_keypair()
BDB = BigchainDB(os.getenv("BDB_ROOT_URL"))
