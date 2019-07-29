import pytest
import copy
from contextlib import contextmanager


from tracking_plan.errors import ValidationError

@contextmanager
def assert_raises_validation_error(expected_msg=None):
    with pytest.raises(ValidationError) as err_info:
        yield

    if expected_msg:
        assert expected_msg in str(err_info.value)
    return err_info

def remove_key(constructor, yaml_obj, key):
    yaml_obj.pop(key)
    return constructor.from_yaml(yaml_obj)

def assert_required(constructor, yaml_obj, key):
    yaml_obj = copy.deepcopy(yaml_obj)
    with assert_raises_validation_error(f'Field {key} is required on {constructor.__name__}'):
        remove_key(constructor, yaml_obj, key)