import pytest
import copy
from tracking_plan.errors import ValidationError

def remove_key(constructor, yaml_obj, key):
    yaml_obj.pop(key)
    return constructor.from_yaml(yaml_obj)

def assert_required(constructor, yaml_obj, key):
    yaml_obj = copy.deepcopy(yaml_obj)
    with pytest.raises(ValidationError) as err_info:
        remove_key(constructor, yaml_obj, key)