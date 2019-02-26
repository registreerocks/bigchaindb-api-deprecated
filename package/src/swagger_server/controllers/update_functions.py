from .creation_functions import _create
from .general_functions import (_add_timestamp, _fulfill_transaction,
                                _get_asset_data, _get_asset_metadata,
                                _send_transaction)
from .global_vars import BDB, MDB

def _course_average_update(query_dict, admin):
    all_marks = list(MDB.assets.find(query_dict))
    course_marks = _group(all_marks, 'course_id')
    transaction_ids = []
    for course_id, c_marks in course_marks.items():
        weights = _get_course_component_weights(course_id)
        student_marks = _group(c_marks, 'student_address')
        for student_address, s_marks in student_marks.items():
            transaction_ids.append(_process_course_average_update(student_address, s_marks, course_id, weights, admin))
    return transaction_ids

def _process_course_average_update(student_address, student_marks, course_id, weights, admin):
    grouped_marks = _group(student_marks, 'degree_id')
    for degree_id, marks in grouped_marks.items():
        metadata = _compute_average(weights, marks, 'mark', 'type')
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
    weights = {item['type']: item['weighting'] for item in course_metadata['components']}
    return weights

def _group(marks, grouping_param):
    grouped_marks = {}
    for item in marks:
        if not grouped_marks.get(item['data'][grouping_param]):
            grouped_marks[item['data'][grouping_param]] = [item]
        else:
            grouped_marks[item['data'][grouping_param]].append(item)
    return grouped_marks

def _compute_average(weights, marks, mark_key, weight_key):
    average = 0
    sum_of_weights = 0
    for mark in marks:
        mark_metadata = _get_asset_metadata(mark['id'])
        average += mark_metadata[mark_key] * weights[mark['data'][weight_key]]
        sum_of_weights += weights[mark['data'][weight_key]]
    if sum_of_weights >= 1:
        return {'avg': average, 'complete': True}
    else:
        return {'avg': average, 'complete': False}

def _degree_average_update(query_dict, admin):
    course_averages = list(MDB.assets.find(query_dict))
    course_averages_by_degree = _group(course_averages, 'degree_id')
    transaction_ids = []
    for degree_id, d_marks in course_averages_by_degree.items():
        total_credit, credit = _get_degree_component_credits(degree_id)
        weights = _compute_weights_from_credits(total_credit, credit)
        averages_by_student = _group(d_marks, 'student_address')
        for student_address, s_marks in averages_by_student.items():
            transaction_ids.append(process_degree_average_update(weights, s_marks, student_address, degree_id, admin))
    return transaction_ids

def _get_degree_component_credits(degree_id):
    degree_data = _get_asset_data(degree_id)
    total_credit = degree_data['total_credits']
    degree_metadata = _get_asset_metadata(degree_id)
    credit = {item['course_id']: item['credits'] for item in degree_metadata['courses']}
    return (total_credit, credit)

def _compute_weights_from_credits(total_credit, credit):
    return {course_id: cred/total_credit for course_id, cred in credit.items()}

def process_degree_average_update(weights, marks, student_address, degree_id, admin):
    metadata = _compute_average(weights, marks, 'avg', 'course_id')
    previous_average = MDB.assets.find_one({'data.asset_type':'degree_average', 'data.student_address': student_address, 'data.degree_id': degree_id})
    if previous_average:
        tx, tx_id = _get_last_transaction(previous_average['id'])
        transaction_input = _build_input(tx, tx_id)
        return _process_update(previous_average['id'], transaction_input, metadata, admin)
    else:
        asset =  {
            'data': {
                'asset_type': 'degree_average',
                'student_address': student_address,
                'degree_id': degree_id,
                'university_id': marks[0]['data']['university_id']
            }
        }
        return _create(asset, metadata, admin)

def _append_children(asset_id, children, child_name, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _append_children_to_list(tx, children, child_name)
    return _process_update(asset_id, transaction_input, metadata, admin)

def _delete_child(asset_id, child_id, child_name, admin):
    tx, tx_id = _get_last_transaction(asset_id)
    transaction_input = _build_input(tx, tx_id)
    metadata = _delete_child_from_list(tx, child_id, child_name)
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

def _append_children_to_list(tx, children, child_name):
    metadata = tx.get('metadata')
    for child in children:
        if child not in metadata[child_name + 's']:
            metadata[child_name + 's'].append(child)
    return metadata

def _delete_child_from_list(tx, child_id, child_name):
    metadata = tx.get('metadata')
    metadata[child_name + 's'] = [d for d in metadata[child_name + 's'] if d.get(child_name + '_id') != child_id]
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
