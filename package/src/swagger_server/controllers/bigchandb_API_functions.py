from bigchaindb_driver.crypto import generate_keypair

from .creation_functions import _create_course, _create_degree, _create_mark
from .getter_functions import (_get_all_courses, _get_all_degrees,
                               _get_marks_by_address)
from .update_functions import _update_degree_course_list

ADMIN = generate_keypair()

def create_course(data, metadata):
    return _create_course(data, metadata, ADMIN)

def create_degree(data, metadata):
    return _create_degree(data, metadata, ADMIN)

def create_mark(data, metadata):
    return _create_mark(data, metadata, ADMIN)

def update_degree_course_list(asset_id, course_id):
    return _update_degree_course_list(asset_id, course_id, ADMIN)

def get_all_courses():
    return _get_all_courses()

def get_all_degrees():
    return _get_all_degrees()

def get_marks_by_address(address):
    return _get_marks_by_address(address)
