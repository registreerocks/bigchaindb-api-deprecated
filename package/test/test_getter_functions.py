import mock
import pytest
from bigchaindb_driver import BigchainDB

from src.swagger_server.controllers.getter_functions import (_get_all_assets,
                                                             _get_asset_by_id,
                                                             _get_assets_by_key,
                                                             _get_assets_by_university)


@mock.patch('bigchaindb_driver.BigchainDB.transactions')
@mock.patch('bigchaindb_driver.BigchainDB.assets')
def test_get_all_assets(mock_assets, mock_transactions):
    mock_assets.get.return_value = get_course_assets()
    mock_transactions.get.return_value = get_course_transaction()
    asset_type = "course"
    assert(_get_all_assets(asset_type, False) == get_course_assets())
    assert(_get_all_assets(asset_type, True) == get_course_search_result())

@mock.patch('bigchaindb_driver.BigchainDB.transactions')
@mock.patch('bigchaindb_driver.BigchainDB.assets')
def test_get_university_files(mock_assets, mock_transactions):
    mock_assets.get.side_effect = [get_course_assets(), get_course_assets()]
    mock_transactions.get.return_value = get_course_transaction()
    university_id = "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"
    asset_type = 'course'
    assert(_get_assets_by_university(university_id, False, asset_type) == get_course_assets())
    assert(_get_assets_by_university(university_id, True, asset_type) == get_course_search_result())

@mock.patch('bigchaindb_driver.BigchainDB.transactions')
@mock.patch('bigchaindb_driver.BigchainDB.assets')
def test_get_assets_by_key(mock_assets, mock_transactions):
    mock_assets.get.return_value = get_course_assets()
    mock_transactions.get.return_value = get_course_transaction()
    asset_type = "course"
    key = 'id'
    value = 'Econ104'
    assert(_get_assets_by_key(asset_type, key, value, False) == get_course_assets())
    assert(_get_assets_by_key(asset_type, key, value, True) == get_course_search_result())

@mock.patch('bigchaindb_driver.BigchainDB.transactions')
def test_get_asset_by_id(mock_transactions):
    mock_transactions.get.return_value = get_course_transaction()
    asset_id = "6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb"
    assert(_get_asset_by_id(asset_id, False) == get_course_assets()[0])
    assert(_get_asset_by_id(asset_id, True) == get_course_search_result()[0])

def get_mark_assets():
    return [{
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]

def get_mark_transaction():
    return [{
            'metadata': {'mark': 85},
            'asset': {'data': {'mark': {'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'}}},
            'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]

def get_mark_search_result():
    return [{
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0',
        'metadata': {'mark': 85}
    }]

def get_university_search_result():
    return [{
                "data": {
                    "asset_type": "university",
                    "name": "University of Cape Town",
                    "physical_address": "string",
                    "postal_address": "string",
                    "short": "UCT"
                },
                "id": "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"
            }]

def get_course_assets():
    return [{
            'data': {
                'asset_type': 'course',
                'name': 'Econometrics',
                'description': 'This course is an introductory course in Econometrics',
                'id': 'Econ104',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'
            }]

def get_course_transaction():
    return [{
            'metadata': {
                'passing': 60,
                'distinction': 90,
                'components': [{
                    'type': 'midterm', 
                    'weighting': 0.25, 
                    'required': True},
                    {'type': 'final_exam', 
                    'weighting': 0.75, 
                    'required': True}],
                'prerequisite': [],
                'corequisite': [],
                },
            'asset': {
                'data': {
                    'asset_type': 'course',
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"}},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}]

def get_course_search_result():
    return [{
            'metadata': {
                'passing': 60,
                'distinction': 90,
                'components': [{
                    'type': 'midterm', 
                    'weighting': 0.25, 
                    'required': True},
                    {'type': 'final_exam', 
                    'weighting': 0.75, 
                    'required': True}],
                'prerequisite': [],
                'corequisite': [],
                },
                'data': {
                    'asset_type': 'course',
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"},
                'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}]
