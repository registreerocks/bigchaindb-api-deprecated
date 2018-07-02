import os

from bigchaindb_driver import BigchainDB

from .general_functions import _fulfill_transaction, _send_transaction

BDB = BigchainDB(os.getenv("BDB_ROOT_URL"))

def _degree_append_courses(asset_id, courses, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _append_course_list(tx, courses)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _degree_delete_course(asset_id, course_id, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _delete_course_from_list(tx, course_id)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _update_metadata_component(updatable, asset_id, new_value, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _update_component(updatable, tx, new_value)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _course_add_requisite(requisite, asset_id, prerequisite_id, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _add_requisite(requisite, tx, prerequisite_id)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _course_delete_requisite(requisite, asset_id, prerequisite_id, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _delete_requisite(requisite, tx, prerequisite_id)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _process_update(asset_id, transaction_input, metadata, admin):
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

def _prepare_update_transaction(asset_id, tx_input, admin, metadata):
    tx_transfer = BDB.transactions.prepare(
        operation='TRANSFER',
        inputs=tx_input,
        asset={'id': asset_id},
        recipients=admin.public_key,
        metadata = metadata
    )
    return tx_transfer

def _append_course_list(tx, courses):
    metadata = tx.get('metadata')
    for course in courses:
        if course not in metadata['courses']:
            metadata['courses'].append(course)
    return metadata

def _delete_course_from_list(tx, course_id):
    metadata = tx.get('metadata')
    metadata['courses'] = [d for d in metadata['courses'] if d.get('course_id') != course_id]
    return metadata

def _update_component(updatable, tx, new_value):
    metadata = tx.get('metadata')
    metadata[updatable] = new_value
    return metadata

def _add_requisite(requisite, tx, requisite_id):
    metadata = tx.get('metadata')
    if requisite_id not in metadata[requisite]:
        metadata[requisite].append(requisite_id)
    return metadata

def _delete_requisite(requisite, tx, requisite_id):
    metadata = tx.get('metadata')
    if requisite_id in metadata[requisite]:
        metadata[requisite].remove(requisite_id)
    return metadata