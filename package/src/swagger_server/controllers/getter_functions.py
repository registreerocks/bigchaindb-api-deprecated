from .global_vars import BDB, MDB
from .general_functions import _get_asset_data, _get_asset_metadata

def _get_all_assets(asset_type, meta_flag):
    files = BDB.assets.get(search=asset_type)
    assets = []
    for f in files:
        if f.get('data').get('asset_type') == asset_type:
            if meta_flag:
                asset_id = f.get('id')
                metadata = BDB.transactions.get(asset_id=asset_id)[-1].get('metadata')
                assets.append({**f, **{'metadata': metadata}})
            else: 
                assets.append(f)
    return assets 

def _get_assets_by_university(university_id, meta_flag, asset_type):
    all_files = _get_all_assets(asset_type, meta_flag)
    university_files = []
    for f in all_files:
        if f.get('data').get('university_id') == university_id:
            university_files.append(f)
    return university_files

def _get_assets_by_key(asset, key, value, meta_flag):
    files = BDB.assets.get(search=value)
    assets = []
    for f in files:
        if (f.get('data').get('asset_type') == asset) and (f.get('data').get(key) == value):
            if meta_flag:
                asset_id = f.get('id')
                metadata = BDB.transactions.get(asset_id=asset_id)[-1].get('metadata')
                assets.append({**f, **{'metadata': metadata}})
            else: 
                assets.append(f)
    return assets

def _get_marks_by_student(student_address):
    mark_assets = get_student_mark_assets(student_address)
    degree_ids, course_ids, mark_data = process(mark_assets)
    mark_data = add_course_info(mark_data, course_ids)
    mark_data = add_degree_info(mark_data, degree_ids)
    return mark_data

def get_student_mark_assets(student_address):
    return list(MDB.assets.find({'data.asset_type':'mark', 'data.student_address': student_address}))

def process(mark_assets):
    course_ids = list()
    degree_ids = list()
    marks = dict()
    for m in mark_assets:
        course_id = m['data']['course_id']
        degree_id = m['data']['degree_id']
        mark_metadata = _get_asset_metadata(m['id'])
        
        if not marks.get(course_id):
            marks[course_id] = dict()
            marks[course_id]['components'] = {m['data']['type']: {'mark': mark_metadata['mark'], 'timestamp': mark_metadata['timestamp'], 'degree_id': m['data']['degree_id']}}
        else:
            marks[course_id]['components'][m['data']['type']] = {'mark': mark_metadata['mark'], 'timestamp': mark_metadata['timestamp'], 'degree_id': m['data']['degree_id']}
            
        course_ids.append(course_id)
        degree_ids.append(degree_id)
        
    course_ids = list(set(course_ids))
    degree_ids = list(set(degree_ids))
    
    return (degree_ids, course_ids, marks)

def add_course_info(marks, course_ids):
    for course_id in course_ids:
        course_asset = _get_asset_data(course_id)
        course_metadata = _get_asset_metadata(course_id)
        
        if marks.get(course_id).get('year', '1900') < course_metadata['timestamp'][:4]:
            marks.get(course_id)['year'] = course_metadata['timestamp'][:4]
        
        marks[course_id] = {**marks[course_id], **course_asset}
        for c in course_metadata['components']:
            if marks[course_id]['components'].get(c['type']):
                marks[course_id]['components'][c['type']]['weighting'] = c['weighting']
            
    return marks

def add_degree_info(marks, degree_ids):
    degree_data = dict()
    for degree_id in degree_ids:
        degree_data[degree_id] = {**_get_asset_data(degree_id), **_get_asset_metadata(degree_id)}
    return {'degree_data': degree_data, 'mark_data': marks}


def _get_asset_by_id(asset_id, meta_flag):
    asset = BDB.transactions.get(asset_id=asset_id)
    if not meta_flag:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id')}
    else:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id'), 'metadata': asset[-1].get('metadata')}

def _get_children(_id, meta_flag, parent_name, child_name):
    parent = _get_asset_by_id(_id, True)
    children = parent.get('metadata').get(child_name + 's')
    collection = []
    for child in children:
        child_id = child.get(child_name + '_id')
        child = _get_asset_by_id(child_id, meta_flag)
        collection.append({**child, **{parent_name + '_info': parent}})
    return collection

def _get_course_marks_by_lecturer(lecturer):
    courses = _get_assets_by_key('course', 'lecturer', lecturer, True)
    course_ids = [item.get('id') for item in courses]
    marks_per_course = dict()
    student_addresses = set()
    for i, course_id in enumerate(course_ids):
        marks = _get_assets_by_key('mark', 'course_id', course_id, True)
        course_marks = dict()
        for mark in marks:
            student_address = mark.get('data').get('student_address')
            mark_data = {'id': mark.get('id'), 'type': mark.get('data').get('type'), 'mark': mark.get('metadata').get('mark')}
            if not course_marks.get(student_address):
                course_marks[student_address] = [mark_data]
            else:
                course_marks[student_address].append(mark_data)
            student_addresses.add(student_address)
        marks_per_course[course_id] = {'name': courses[i].get('data').get('name'), 'components': courses[i].get('metadata').get('components'), 'course_marks': course_marks}
    return {'student_addresses': list(student_addresses), 'marks_per_course': marks_per_course}