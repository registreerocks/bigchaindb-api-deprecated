import os

from bigchaindb_driver import BigchainDB

BDB = BigchainDB(os.getenv("BDB_ROOT_URL"))

def _fulfill_transaction(transaction, key):
    return BDB.transactions.fulfill(transaction, private_keys=key)

def _send_transaction(transaction):
    return BDB.transactions.send_commit(transaction)