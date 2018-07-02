import mock
import pytest
from bigchaindb_driver import BigchainDB

from src.swagger_server.controllers.getter_functions import \
    _get_marks_by_address


@mock.patch('bigchaindb_driver.BigchainDB.assets')
@mock.patch('bigchaindb_driver.BigchainDB.transactions')
def test_get_marks_by_address(mock_transactions, mock_assets):
    mock_assets.get.return_value = get_mark_search_result()
    mock_transactions.get.side_effect = [get_course_asset(), get_mark_asset()]
    assert(_get_marks_by_address('0x04') == [('Econometrics', 'midterm', 85, 0.25)])

def get_mark_search_result():
    return [{
        'data': {
            'mark': {
                'student': '0x04',
                'course': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
                'type': 'midterm'}
                },
        'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]
def get_course_asset():
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
                'corequisite': []},
            'asset': {
                'data': {
                    'course': {
                        'name': 'Econometrics',
                        'description': 'This course is an introductory course in Econometrics',
                        'id': 'Econ104'}}},
            'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}]

def get_mark_asset():
    return [{
            'metadata': {'mark': 85},
            'asset': {'data': {'mark': {'student': '0x03',
            'course': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
            'type': 'midterm'}}},
            'id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0'}]
