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

def _get_asset_by_id(asset_id, meta_flag):
    asset = BDB.transactions.get(asset_id=asset_id)
    if not meta_flag:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id')}
    else:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id'), 'metadata': asset[-1].get('metadata')}

def _get_courses_by_degree(_id, meta_flag):
    degree = _get_asset_by_id(_id, True)
    courses = degree.get('metadata').get('courses')
    collection = []
    for course in courses:
        course_id = course.get('course_address')
        course_data = _get_asset_by_id(course_id, meta_flag)
        collection.append({**course_data, **{'degree_info': course}})
    return collection
