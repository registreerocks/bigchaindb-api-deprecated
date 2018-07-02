from bigchaindb_driver.crypto import generate_keypair

from .creation_functions import _create
from .getter_functions import (_get_all_courses, _get_all_degrees,
                               _get_all_universities, _get_marks_by_address)
from .update_functions import (_course_add_requisite, _course_delete_requisite,
                               _degree_append_courses, _degree_delete_course,
                               _update_metadata_component)

ADMIN = generate_keypair()

def create_university(data, metadata):
    return _create(data, metadata, ADMIN)

def create_degree(data, metadata):
    return _create(data, metadata, ADMIN)

def create_course(data, metadata):
    return _create(data, metadata, ADMIN)

def create_mark(data, metadata):
    return _create(data, metadata, ADMIN)

def degree_append_courses(asset_id, courses):
    return _degree_append_courses(asset_id, courses, ADMIN)

def degree_delete_course(asset_id, course_id):
    _degree_delete_course(asset_id, course_id, ADMIN)

def get_all_courses():
    return _get_all_courses()

def get_all_degrees():
    return _get_all_degrees()

def get_marks_by_address(address):
    return _get_marks_by_address(address)

def get_all_universities():
    return _get_all_universities()

def course_update_passing(course_id, passing):
    _update_metadata_component('passing', course_id, passing, ADMIN)

def course_update_distinction(course_id, distinction):
    _update_metadata_component('distinction', course_id, distinction, ADMIN)

def course_update_components(course_id, components):
    _update_metadata_component('components', course_id, components, ADMIN)

def course_add_prerequisite(course_id, prerequisite_id):
    _course_add_requisite('prerequisite', course_id, prerequisite_id, ADMIN)

def course_add_corequisite(course_id, corequisite_id):
    _course_add_requisite('corequisite', course_id, corequisite_id, ADMIN)

def course_delete_prerequisite(course_id, prerequisite_id):
    _course_delete_requisite('prerequisite', course_id, prerequisite_id, ADMIN)

def course_delete_corequisite(course_id, corequisite_id):
    _course_delete_requisite('corequisite', course_id, corequisite_id, ADMIN)

def mark_update(mark_id, mark):
     _update_metadata_component('mark', mark_id, mark, ADMIN)
