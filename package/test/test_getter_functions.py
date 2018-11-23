import mock
import pytest
from bigchaindb_driver import BigchainDB
import pymongo

from src.swagger_server.controllers.getter_functions import (_get_all_assets,  # _retrieve_course_ids,; _retrieve_course_information,; _retrieve_degree_data,; _retrieve_mark_data
                                                             _get_asset_by_id,
                                                             _get_assets_by_key,
                                                             _get_assets_by_university,
                                                             _get_course_marks_by_lecturer,
                                                             _get_marks_by_student)


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

@mock.patch('pymongo.collection.Collection.find')
@mock.patch('pymongo.collection.Collection.find_one')
def test_get_marks_by_student(mock_mongo_find_one, mock_mongo_find):
    mock_mongo_find.side_effect = [get_mark_assets(), [], [], []]
    mock_mongo_find_one.side_effect = [get_mark_transaction()[0], get_course_assets()[0], get_course_metadata(), get_degree_assets()[0], get_degree_transaction()[0]]

    expected_output = {
        'degree_data': {
            '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef7aa': {
                'asset_type': 'degree',
                'courses': [{'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 'semester': 1, 'weighting': 1}],
                'description': 'This course is cool degree',
                'id': 'MPhil-Fintech',
                'level': 'Master',
                'name': 'Fintech',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"
            }
        },
        'mark_data':{
            '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb': {
                'asset_type': 'course',
                'name': 'Econometrics',
                'description': 'This course is an introductory course in Econometrics',
                'id': 'Econ104',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                'year': '2018',
                'lecturer': 'Smith',
                'components': {
                    'midterm': {
                        'mark': 85,
                        'weighting': 0.25, 
                        'degree_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef7aa',
                        'timestamp': '2018-09-10 16:00'
                    }
                }
            }
        }
    }

    assert(_get_marks_by_student('0x03') == expected_output)



# def test_retrieve_course_ids():
#     files = get_mark_assets()
#     student_address = '0x03'
#     assert (_retrieve_course_ids(files, student_address) == (files, ['6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb']))
#     student_address = '0x04'
#     assert (_retrieve_course_ids(files, student_address) == ([], []))

# @mock.patch('bigchaindb_driver.BigchainDB.transactions')
# def test_retrieve_course_information(mock_transactions):
#     mock_transactions.get.return_value = get_course_transaction()
#     expected_output = {'0x00': {'name': 'Econometrics', 
#                                 'lecturer': 'Smith',
#                                 'components': [{
#                                     'type': 'midterm', 
#                                     'weighting': 0.25, 
#                                     'required': True},
#                                     {'type': 'final', 
#                                     'weighting': 0.75, 
#                                     'required': True}]
#                                 }
#     }
#     assert(_retrieve_course_information(['0x00']) == expected_output)

# @mock.patch('bigchaindb_driver.BigchainDB.transactions')
# def test_retrieve_mark_data(mock_transactions):
#     mock_transactions.get.side_effect = [get_mark_transaction(), get_mark_transaction1()]
#     files = get_multiple_mark_assets()
#     course_data = {'6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb': {
#         'name': 'Econometrics', 
#         'lecturer': 'Smith',
#         'components': [{
#             'type': 'midterm', 
#             'weighting': 0.25, 
#             'required': True},
#             {'type': 'final', 
#             'weighting': 0.75, 
#             'required': True}]
#         }
#     }
#     expected_output = {'6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb': {
#         'name': 'Econometrics',
#         'lecturer': 'Smith',
#         'year': '2019',
#         'components': {
#             'midterm': {'mark': 85, 'weighting': 0.25, 'timestamp': '2018-09-10 16:00'},
#             'final': {'mark': 85, 'weighting': 0.75, 'timestamp': '2019-09-10 16:00'}
#             }
#         }}
#     assert(_retrieve_mark_data(files, course_data) == expected_output)

@mock.patch('bigchaindb_driver.BigchainDB.transactions')
@mock.patch('bigchaindb_driver.BigchainDB.assets')
def test_get_course_marks_by_lecturer(mock_assets, mock_transactions):
    mock_assets.get.side_effect = [get_course_assets(), get_mark_assets()]
    mock_transactions.get.side_effect = [get_course_search_result(), get_mark_search_result()]
    expected_output = {'student_addresses': ['0x03'], 
    'marks_per_course':
        {'6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb': {
            'name': 'Econometrics',
            'components': [{
                'type': 'midterm', 
                'weighting': 0.25, 
                'required': True},
                {'type': 'final', 
                'weighting': 0.75, 
                'required': True}], 
            'course_marks': {
                '0x03': {
                    'midterm': 85
            }}}}}
    assert(_get_course_marks_by_lecturer('Smith')==expected_output)

# @mock.patch('bigchaindb_driver.BigchainDB.transactions')
# def test_retrieve_degree_data(mock_transactions):
#     mock_transactions.get.return_value = get_degree_transaction()
    
#     files = get_mark_assets()
#     expected_output = {
#             'name': 'Fintech',
#             'level': 'Master',
#             'courses': [{
#                     'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 
#                     'weighting': 1, 
#                     'semester': 1
#                     }]
#     }
#     assert(_retrieve_degree_data(files) == expected_output)

def get_mark_assets():
    return [{
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'degree_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef7aa',
            'type': 'midterm'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]

def get_multiple_mark_assets():
    return [{
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'},
        {
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'final'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b1'}]

def get_mark_transaction():
    return [{
            'metadata': {'mark': 85, 'timestamp': '2018-09-10 16:00'},
            'asset': {'data': {'mark': {'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'}}},
            'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]

def get_mark_transaction1():
    return [{
            'metadata': {'mark': 85, 'timestamp': '2019-09-10 16:00'},
            'asset': {'data': {'mark': {'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'final'}}},
            'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b1'}]

def get_mark_search_result():
    return [{
        'data': {
            'asset_type': 'mark',
            'student_address': '0x03',
            'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'},
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0',
        'metadata': {'mark': 85, 'timestamp': '2018-09-10 16:00'}
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
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                'lecturer': 'Smith'},
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
                    {'type': 'final', 
                    'weighting': 0.75, 
                    'required': True}],
                'prerequisite': [],
                'corequisite': []                },
            'asset': {
                'data': {
                    'asset_type': 'course',
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                    'lecturer': 'Smith'}},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}]

def get_course_metadata():
    return {
        'metadata': {
            'passing': 60,
            'distinction': 90,
            'components': [{
                'type': 'midterm', 
                'weighting': 0.25, 
                'required': True},
                {'type': 'final', 
                'weighting': 0.75, 
                'required': True}],
            'prerequisite': [],
            'corequisite': [], 
            'timestamp': '2018-01-01'
        }
    }

def get_course_search_result():
    return [{
            'metadata': {
                'passing': 60,
                'distinction': 90,
                'components': [{
                    'type': 'midterm', 
                    'weighting': 0.25, 
                    'required': True},
                    {'type': 'final', 
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
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                    'lecturer': 'Smith'},
                'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}]

def get_degree_assets():
    return [{
            'data': {
                'asset_type': 'degree',
                'level': 'Master',
                'name': 'Fintech',
                'description': 'This course is cool degree',
                'id': 'MPhil-Fintech',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef7bb'
            }]

def get_degree_transaction():
    return [{
            'metadata': {
                'courses': [{
                    'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 
                    'weighting': 1, 
                    'semester': 1
                    }]
                },
            'asset': {
                'data': {
                    'asset_type': 'degree',
                    'level': 'Master',
                    'name': 'Fintech',
                    'description': 'This course is cool degree',
                    'id': 'MPhil-Fintech',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"}},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef7bb'}]
