from .authentication import requires_auth, requires_scope
from .creation_functions import _component_weighting_equal_one, _create
from .getter_functions import (_get_all_assets, _get_asset_by_id,
                               _get_assets_by_key, _get_assets_by_university,
                               _get_course_marks_by_lecturer,
                               _get_courses_by_degree, _get_marks_by_student)
from .global_vars import ADMIN
from .querying_functions import _get_top_x, _get_top_x_percent
from .update_functions import (_course_add_requisite, _course_average_update,
                               _course_delete_requisite,
                               _degree_append_courses, _degree_average_update,
                               _degree_delete_course,
                               _update_metadata_component)


@requires_auth
@requires_scope('registree')
def create_university(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def create_degree(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def create_course(body):
    if not _component_weighting_equal_one(body.get('metadata')):
        return {'ERROR': 'Course component weights do not sum up to one.'}, 409
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def create_mark(body):
    return _create(body.get('asset'), body.get('metadata'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def degree_append_courses(body):
    return _degree_append_courses(body.get('degree_id'), body.get('courses'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def degree_delete_course(body):
    _degree_delete_course(body.get('degree_id'), body.get('course_id'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def get_all_courses(meta_flag):
    return _get_all_assets('course', meta_flag)

@requires_auth
@requires_scope('admin', 'registree')
def get_all_degrees(meta_flag):
    return _get_all_assets('degree', meta_flag)

# @requires_auth
# @requires_scope('admin', 'lecturer', 'student', 'registree')
def get_marks_by_student(student_address):
    return  _get_marks_by_student(student_address)

@requires_auth
@requires_scope('registree')
def get_all_universities(meta_flag):
    return _get_all_assets('university', meta_flag)

@requires_auth
@requires_scope('admin', 'registree')
def course_update_passing(body):
    return _update_metadata_component('passing', body.get('course_id'), body.get('passing'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_update_distinction(body):
    return _update_metadata_component('distinction', body.get('course_id'), body.get('distinction'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_update_components(body):
    return _update_metadata_component('components', body.get('course_id'), body.get('components'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_add_prerequisite(body):
    return _course_add_requisite('prerequisite', body.get('course_id'), body.get('prerequisite_id'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_add_corequisite(body):
    return _course_add_requisite('corequisite', body.get('course_id'), body.get('corequisite_id'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_delete_prerequisite(body):
    return _course_delete_requisite('prerequisite', body.get('course_id'), body.get('prerequisite_id'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def course_delete_corequisite(body):
    return _course_delete_requisite('corequisite', body.get('course_id'), body.get('corequisite_id'), ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def mark_update(body):
    return _update_metadata_component('mark', body.get('mark_id'), body.get('mark'), ADMIN)

@requires_auth
@requires_scope('admin', 'registree')
def university_get_degrees(id, meta_flag):
    return _get_assets_by_university(id, meta_flag, 'degree')

@requires_auth
@requires_scope('admin', 'registree')
def university_get_courses(id, meta_flag):
    return _get_assets_by_university(id, meta_flag, 'course')

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def course_get_by_lecturer(lecturer, meta_flag):
    return _get_assets_by_key('course', 'lecturer', lecturer, meta_flag)

@requires_auth
@requires_scope('admin', 'lecturer', 'student', 'registree')
def university_get_by_id(id, meta_flag):
    return _get_asset_by_id(id, meta_flag)

@requires_auth
@requires_scope('admin', 'lecturer', 'student', 'registree')
def degree_get_by_id(id, meta_flag):
    return _get_asset_by_id(id, meta_flag)

# @requires_auth
# @requires_scope('admin', 'lecturer', 'student', 'registree')
def course_get_by_id(id, meta_flag):
    return _get_asset_by_id(id, meta_flag)

@requires_auth
@requires_scope('admin', 'lecturer', 'student')
def get_marks_by_course_id(id):
    return _get_assets_by_key('mark', 'course_id', id, True)

@requires_auth
@requires_scope('admin', 'lecturer', 'student', 'registree')
def degree_get_courses(id, meta_flag):
    return _get_courses_by_degree(id, meta_flag)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def get_course_marks_by_lecturer(lecturer):
    return _get_course_marks_by_lecturer(lecturer)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def course_average_update_one(body):
    return _course_average_update({'data.asset_type':'mark', 'data.student_address': body.get('student_address'), 'data.course_id': body.get('course_id')}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def course_average_update_course(body):
    return _course_average_update({'data.asset_type':'mark', 'data.course_id': body.get('course_id')}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def course_average_update_all():
    return _course_average_update({'data.asset_type':'mark'}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def query_course_top_x(x, course_id):
    return _get_top_x(x, 'course', course_id)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def query_course_top_x_percent(x, course_id):
    return _get_top_x_percent(x, 'course', course_id)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def degree_average_update_one(body):
    return _degree_average_update({'data.asset_type':'course_average', 'data.student_address': body.get('student_address'), 'data.degree_id': body.get('degree_id')}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def degree_average_update_degree(body):
    return _degree_average_update({'data.asset_type':'course_average', 'data.degree_id': body.get('degree_id')}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def degree_average_update_all():
    return _degree_average_update({'data.asset_type':'course_average'}, ADMIN)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def query_degree_top_x(x, degree_id):
    return _get_top_x(x, 'degree', degree_id)

@requires_auth
@requires_scope('admin', 'lecturer', 'registree')
def query_degree_top_x_percent(x, degree_id):
    return _get_top_x_percent(x, 'degree', degree_id)