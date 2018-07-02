import mock
import pytest
from bigchaindb_driver import BigchainDB

from src.swagger_server.controllers.update_functions import (_add_requisite,
                                                             _append_course_list,
                                                             _delete_course_from_list,
                                                             _delete_requisite,
                                                             _update_component)


def test_append_course_list_appends():
    tx = get_degree_transaction()
    courses = [{'course_id': 'eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6', 'weighting': 0.5}]
    expected_output = {'courses': [{'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb',
                                    'weighting': 0.5},
                                    {'course_id': 'eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6',
                                    'weighting': 0.5}]}
    assert (_append_course_list(tx, courses) == expected_output)

def test_append_course_list_doesnt_append():
    tx = get_degree_transaction()
    courses = [{'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 'weighting': 0.5}]
    expected_output = {'courses': [{'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 'weighting': 0.5}]}
    assert (_append_course_list(tx, courses) == expected_output)

def test_delete_course():
    tx = get_degree_transaction()
    course = '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'
    expected_output = {'courses': []}
    assert (_delete_course_from_list(tx, course) == expected_output)

def test_update_component():
    tx = get_course_transaction()
    updatable = 'passing'
    value = 65
    expected_output = {
            'passing': 65,
            'distinction': 90,
            'components': [
                {'name': 'midterm', 'weighting': 0.25, 'required': True},
                {'name': 'final_exam', 'weighting': 0.75, 'required': True}],
            'prerequisite': ['eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6'],
            'corequisite': []}
    assert(_update_component(updatable, tx, value) == expected_output)

def test_add_requisite_appends():
    tx = get_course_transaction()
    requisite = 'prerequisite'
    course = '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'
    expected_output = {
            'passing': 60,
            'distinction': 90,
            'components': [
                {'name': 'midterm', 'weighting': 0.25, 'required': True},
                {'name': 'final_exam', 'weighting': 0.75, 'required': True}],
            'prerequisite': ['eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6', 
                            '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'],
            'corequisite': []}
    assert(_add_requisite(requisite, tx, course) == expected_output)

def test_add_requisite_doesnt_append():
    tx = get_course_transaction()
    requisite = 'prerequisite'
    course = 'eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6'
    expected_output = {
            'passing': 60,
            'distinction': 90,
            'components': [
                {'name': 'midterm', 'weighting': 0.25, 'required': True},
                {'name': 'final_exam', 'weighting': 0.75, 'required': True}],
            'prerequisite': ['eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6'],
            'corequisite': []}
    assert(_add_requisite(requisite, tx, course) == expected_output)

def test_delete_requisite():
    tx = get_course_transaction()
    requisite = 'prerequisite'
    course = 'eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6'
    expected_output = {
            'passing': 60,
            'distinction': 90,
            'components': [
                {'name': 'midterm', 'weighting': 0.25, 'required': True},
                {'name': 'final_exam', 'weighting': 0.75, 'required': True}],
            'prerequisite': [],
            'corequisite': []}
    assert(_delete_requisite(requisite, tx, course) == expected_output)


def get_degree_transaction():
    return {
        'metadata': {
            'courses': [{'course_id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb', 'weighting': 0.5}]},
        'asset': {
            'data': {
                'degree': {
                    'name': 'Financial Technology',
                    'level': 'Master',
                    'description': 'Masters degree in fintech',
                    'id': 'MFinTech'}}},
        'id': 'e8761f021d2f74d8ed683fefec8a74a0841ab91d6fcc3c94ca02780065ff2d83'}

def get_course_transaction():
    return {
        'metadata': {
            'passing': 60,
            'distinction': 90,
            'components': [
                {'name': 'midterm', 'weighting': 0.25, 'required': True},
                {'name': 'final_exam', 'weighting': 0.75, 'required': True}],
            'prerequisite': ['eeb5c64cbd331763b368cbcc922276ff571a3030243a509ba56cbb875f1c65b6'],
            'corequisite': []},
        'asset': {
            'data': {
                'course': {
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104'}}},
        'id': '6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb'}
