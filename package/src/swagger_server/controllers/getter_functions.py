import os

from bigchaindb_driver import BigchainDB

BDB = BigchainDB(os.getenv("BDB_ROOT_URL"))

def _get_all_courses():
    return BDB.assets.get(search='course')

def _get_all_degrees():
    return BDB.assets.get(search='degree')

def _get_marks_by_address(address):
    course_marks = dict()
    marks = BDB.assets.get(search=address)
    for mark in marks:
        course_id = mark.get('data').get('mark').get('course')
        course_transaction = BDB.transactions.get(asset_id=course_id)
        course = course_transaction[0].get('asset').get('data').get('course').get('name')
        mark_id =  mark.get('id')
        mark_transaction = BDB.transactions.get(asset_id=mark_id)
        mark = mark_transaction[-1].get('metadata').get('mark')
        course_marks[course] = mark
    return course_marks
