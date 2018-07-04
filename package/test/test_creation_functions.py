import pytest

from src.swagger_server.controllers.creation_functions import _component_weighting_equal_one

def test_component_weighting_equal_one_true():
    metadata = {
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
            'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"}
    assert (_component_weighting_equal_one(metadata) == True)

def test_component_weighting_equal_one_false():
    metadata = {
            'passing': 60,
            'distinction': 90,
            'components': [{
                'type': 'midterm', 
                'weighting': 0.25, 
                'required': True},
                {'type': 'final_exam', 
                'weighting': 0.5, 
                'required': True}],
            'prerequisite': [],
            'corequisite': [],
            'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"}
    assert (_component_weighting_equal_one(metadata) == False)