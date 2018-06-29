import os

from bigchaindb_driver import BigchainDB

from .general_functions import _fulfill_transaction, _send_transaction

BDB = BigchainDB(os.getenv("BDB_ROOT_URL"))

def _update_degree_course_list(asset_id, course_id, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _update_course_list(tx, course_id)
    transaction = _prepare_update_transaction(asset_id, transaction_input, admin, metadata)
    signed_transaction = _fulfill_transaction(transaction, admin.private_key)
    receipt = _send_transaction(signed_transaction)
    if signed_transaction == receipt:
        return receipt.get('id')

def _get_last_transaction(asset_id):
    transaction = BDB.transactions.get(asset_id=asset_id)[-1]
    transaction_id = transaction.get('id')
    return (transaction, transaction_id)

def _build_input(tx, tx_id):
    output = tx.get('outputs')[-1]
    tx_input = {
        'fulfillment': output.get('condition').get('details'),
        'fulfills': {
            'output_index': 0,
            'transaction_id': tx_id,
        },
        'owners_before': output.get('public_keys'),
    }
    return tx_input

def _update_course_list(tx, course_id):
    metadata = tx.get('metadata')
    metadata.get('courses').append(course_id)
    return metadata

def _prepare_update_transaction(asset_id, tx_input, admin, metadata):
    tx_transfer = BDB.transactions.prepare(
        operation='TRANSFER',
        inputs=tx_input,
        asset={'id': asset_id},
        recipients=admin.public_key,
        metadata = metadata
    )
    return tx_transfer
