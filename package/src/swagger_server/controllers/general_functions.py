import datetime

from .global_vars import BDB, MDB


def _fulfill_transaction(transaction, key):
    return BDB.transactions.fulfill(transaction, private_keys=key)

def _send_transaction(transaction):
    return BDB.transactions.send_commit(transaction)

def _add_timestamp(dictionary):
    dictionary['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    return dictionary

def _get_asset_data(_id):
    asset = MDB.assets.find_one({'id': _id})
    return asset['data']

def _get_asset_metadata(asset_id):
    transactions = list(MDB.transactions.find({'asset.id': asset_id}))
    if transactions:
        return MDB.metadata.find_one({'id': transactions[-1]['id']})['metadata']
    else:
        return MDB.metadata.find_one({'id': asset_id})['metadata'] 