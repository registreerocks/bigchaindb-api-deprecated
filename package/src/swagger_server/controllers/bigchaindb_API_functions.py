from .creation_functions import _create
from .getter_functions import (_get_all_assets, _get_marks_by_address,
                               _get_assets_by_university)
from .global_vars import ADMIN
from .update_functions import (_course_add_requisite, _course_delete_requisite,
                               _degree_append_courses, _degree_delete_course,
                               _update_metadata_component)


def create_university(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

def create_degree(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

def create_course(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

def create_mark(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

def degree_append_courses(body):
    return _degree_append_courses(body.get('degree_id'), body.get('courses'), ADMIN)

def degree_delete_course(body):
    _degree_delete_course(body.get('degree_id'), body.get('course_id'), ADMIN)

def get_all_courses():
    return _get_all_assets('course')

def get_all_degrees():
    return _get_all_assets('degree')

def get_marks_by_address(student_address):
    return _get_marks_by_address(student_address)

def get_all_universities():
    return _get_all_assets('university')

def course_update_passing(body):
    return _update_metadata_component('passing', body.get('course_id'), body.get('passing'), ADMIN)

def course_update_distinction(body):
    return _update_metadata_component('distinction', body.get('course_id'), body.get('distinction'), ADMIN)

def course_update_components(body):
    return _update_metadata_component('components', body.get('course_id'), body.get('components'), ADMIN)

def course_add_prerequisite(body):
    return _course_add_requisite('prerequisite', body.get('course_id'), body.get('prerequisite_id'), ADMIN)

def course_add_corequisite(body):
    return _course_add_requisite('corequisite', body.get('course_id'), body.get('corequisite_id'), ADMIN)

def course_delete_prerequisite(body):
    return _course_delete_requisite('prerequisite', body.get('course_id'), body.get('prerequisite_id'), ADMIN)

def course_delete_corequisite(body):
    return _course_delete_requisite('corequisite', body.get('course_id'), body.get('corequisite_id'), ADMIN)

def mark_update(body):
    return _update_metadata_component('mark', body.get('mark_id'), body.get('mark'), ADMIN)

def university_get_degrees(university_name):
    return _get_assets_by_university(university_name, 'degree')

def university_get_courses(university_name):
    return _get_assets_by_university(university_name, 'course')
