from .creation_functions import _create
from .general_functions import (_add_timestamp, _fulfill_transaction,
                                _get_asset_metadata, _send_transaction)
from .global_vars import BDB, MDB

def _course_average_update_one(student_address, course_id, admin):
    weights = _get_course_component_weights(course_id)
    student_marks = list(MDB.assets.find({'data.asset_type':'mark', 'data.student_address': student_address, 'data.course_id': course_id}))
    return _process_average_update(student_address, student_marks, course_id, weights, admin)

def _course_average_update_course(course_id, admin):
    weights = _get_course_component_weights(course_id)
    marks = list(MDB.assets.find({'data.asset_type':'mark', 'data.course_id': course_id}))
    student_marks = _group(marks, 'student_address')
    transaction_ids = [] 
    for student_address, marks in student_marks.items():
        transaction_ids.append(_process_average_update(student_address, marks, course_id, weights, admin))
    return transaction_ids

def _process_average_update(student_address, student_marks, course_id, weights, admin):
    grouped_marks = _group(student_marks, 'degree_id')
    for degree_id, marks in grouped_marks.items():
        metadata = _compute_average(weights, marks)
        previous_average = MDB.assets.find_one({'data.asset_type':'course_average', 'data.student_address': student_address, 'data.course_id': course_id})
        if previous_average:
            tx, tx_id = _get_last_transaction(previous_average['id'])
            transaction_input = _build_input(tx, tx_id)
            return _process_update(previous_average['id'], transaction_input, metadata, admin)
        else:
            asset =  {
                'data': {
                    'asset_type': 'course_average',
                    'student_address': student_address,
                    'course_id': course_id,
                    'degree_id': degree_id,
                    'university_id': marks[0]['data']['university_id']
                }
            }
            return _create(asset, metadata, admin)

def _get_course_component_weights(course_id):
    course_metadata = _get_asset_metadata(course_id)
    weights = _weighting_dictionary(course_metadata['components'])
    return weights

def _weighting_dictionary(component_list):
    dictionary = dict()
    for c in component_list:
        dictionary[c['type']] = c['weighting']
    return dictionary

def _group(marks, grouping_param):
    grouped_marks = {}
    for item in marks:
        if not grouped_marks.get(item['data'][grouping_param]):
            grouped_marks[item['data'][grouping_param]] = [item]
        else:
            grouped_marks[item['data'][grouping_param]].append(item)
    return grouped_marks

def _compute_average(weights, student_marks):
    average = 0
    sum_of_weights = 0
    for mark in student_marks:
        mark_metadata = _get_asset_metadata(mark['id'])
        average += mark_metadata['mark'] * weights[mark['data']['type']]
        sum_of_weights += weights[mark['data']['type']]
    if sum_of_weights == 1:
        return {'avg': average, 'complete': True}
    else:
        return {'avg': average, 'complete': False}

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
        metadata = _add_timestamp(metadata)
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
