import math

from .general_functions import _get_asset_data, _get_asset_metadata
from .global_vars import MDB


def _get_top_x(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    if x < len(averages):
        return averages[:x]
    else:
        return averages

def _get_top_x_percent(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    return _x_percent(x, averages)

def _retrieve_averages(_type, _id):
    assets = list(MDB.assets.find({'data.asset_type': _type + '_average', 'data.' + _type + '_id': _id}))
    return _sort_averages(assets)

def _sort_averages(assets):
    course_averages = list()
    for asset in assets:
        average = _get_asset_metadata(asset['id'])
        average['student_address'] = asset['data']['student_address']
        course_averages.append(average)
    return sorted(course_averages, key=lambda k: k['avg'], reverse=True)

def _x_percent(x, sorted_averages):
    y = math.floor(x/100 * len(sorted_averages))
    return sorted_averages[:y]
