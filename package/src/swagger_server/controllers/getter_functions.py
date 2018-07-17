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

def _get_marks_by_address(address):
    all_marks = _get_all_assets('mark', True)
    student_marks = []
    for mark in all_marks:
        if mark.get('data').get('student_address') == address:
            student_marks.append(mark)
    return student_marks

def _get_assets_by_key(asset, key, value, meta_flag):
    assets = _get_all_assets(asset, True)
    matches = []
    for asset in assets:
        if (asset['data'].get(key) == value) or (asset['metadata'].get(key) == value):
            if meta_flag:
                matches.append(asset)
            else:
                matches.append({'data': asset.get('data'), 'id': asset.get('id')})
    return matches

def _get_asset_by_id(asset_id, meta_flag):
    asset = BDB.transactions.get(asset_id=asset_id)
    if not meta_flag:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id')}
    else:
        return {'data': asset[0].get('asset').get('data'), 'id': asset[0].get('id'), 'metadata': asset[-1].get('metadata')}