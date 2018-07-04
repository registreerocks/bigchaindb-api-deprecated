from .global_vars import BDB

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

def _get_assets_by_university(university_name, meta_flag, asset_type):
    university = BDB.assets.get(search=university_name)
    if len(university) == 1:
        university_id = university[0].get('id')
        all_files = _get_all_assets(asset_type, meta_flag)
        university_files = []
        for f in all_files:
            if f.get('data').get('university_id') == university_id:
                university_files.append(f)
        return university_files
    elif len(university) < 1:
        return {'ERROR': 'No matching university found'}
    elif len(university) > 1:
        return {'ERROR': 'More than one matching university found. Refine your search.'}

def _get_marks_by_address(address):
    course_marks = []
    marks = BDB.assets.get(search=address)
    for mark in marks:
        mark_type = mark.get('data').get('type')
        course_id = mark.get('data').get('course')
        course_transaction = BDB.transactions.get(asset_id=course_id)
        course = course_transaction[0].get('asset').get('data').get('name')
        mark_id =  mark.get('id')
        course_components = course_transaction[-1].get('metadata').get('components')
        for c in course_components:
            if c.get('type') == mark_type:
                mark_weighting = c.get('weighting')
                break
        mark_transaction = BDB.transactions.get(asset_id=mark_id)
        mark = mark_transaction[-1].get('metadata').get('mark')
        course_marks.append((course, mark_type, mark, mark_weighting))
    return course_marks