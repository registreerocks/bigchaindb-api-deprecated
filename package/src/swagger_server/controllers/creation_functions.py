from .general_functions import (_add_timestamp, _fulfill_transaction,
                                _send_transaction)
from .global_vars import BDB

def _create(asset, metadata, user):
    metadata = _timestamp_metadata(metadata)
    transaction = _prepare_create_transaction(asset, metadata, user.public_key)
    signed_transaction = _fulfill_transaction(transaction, user.private_key)
    receipt = _send_transaction(signed_transaction)
    if signed_transaction == receipt:
        return receipt.get('id')

def _component_weighting_equal_one(metadata):
    components = metadata.get('components')
    sum_of_weights = 0
    for item in components:
        sum_of_weights += item.get('weighting')
    if sum_of_weights == 1:
        return True
    else:
        return False

def _prepare_create_transaction(asset, metadata, key):
    prepared_creation_tx = BDB.transactions.prepare(
        operation='CREATE',
        signers=key,
        asset=asset,
        metadata=metadata,
    )
    return prepared_creation_tx

def _timestamp_metadata(metadata):
    if not metadata.get('timestamp'):
        return _add_timestamp(metadata)
    else:
        return metadata
