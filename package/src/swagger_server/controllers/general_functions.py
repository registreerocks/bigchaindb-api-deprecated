import datetime

from .global_vars import BDB


def _fulfill_transaction(transaction, key):
    return BDB.transactions.fulfill(transaction, private_keys=key)

def _send_transaction(transaction):
    return BDB.transactions.send_commit(transaction)

def _add_timestamp(dictionary):
    dictionary['timestamp'] = datetime.datetime.utcnow()
    return dictionary
