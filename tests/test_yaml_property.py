import pytest
from tests.helpers import assert_required, assert_raises_validation_error

import yaml
from tracking_plan.yaml_property import YamlProperty
from tracking_plan.errors import ValidationError

@pytest.fixture
def property_yaml_obj():
    return  yaml.safe_load("""
    name: variation
    description: What variation of the group
    type: string
    required: false
    allowNull: true
    pattern: "experiment|control"
""")

@pytest.fixture
def property_type_any_yaml_obj():
    return  yaml.safe_load("""
    name: version
    description: This could be a string or integer
    type: any
""")

def test_parsing_top_level_attrs(property_yaml_obj):
    prop = YamlProperty.from_yaml(property_yaml_obj)

    assert prop.name == 'variation'
    assert prop.description == 'What variation of the group'
    assert prop.type == 'string'
    assert prop.required == False
    assert prop.allow_null == True

def test_default_values(property_yaml_obj):
    property_yaml_obj.pop('required')
    property_yaml_obj.pop('allowNull')

    prop = YamlProperty.from_yaml(property_yaml_obj)

    assert prop.required == False
    assert prop.allow_null == False

def test_to_json(property_yaml_obj):
    prop = YamlProperty.from_yaml(property_yaml_obj)

    expected = {
        'description': 'What variation of the group',
        'pattern': 'experiment|control',
        'type': [
            'string',
            'null'
        ]
    }

    actual = prop.to_json()

    assert expected == actual

def test_validate_pattern_on_string_type(property_yaml_obj):
    property_yaml_obj['type'] = 'number'

    with assert_raises_validation_error(expected_msg=f'Property variation cannot specify a pattern'):
        YamlProperty(property_yaml_obj)

def test_required_fields(property_yaml_obj):
    assert_required(YamlProperty, property_yaml_obj, 'name')
    assert_required(YamlProperty, property_yaml_obj, 'description')
    assert_required(YamlProperty, property_yaml_obj, 'type')

def test_valid_type(property_yaml_obj):
    property_yaml_obj['type'] = 'foo'
    property_yaml_obj.pop('pattern')
    with assert_raises_validation_error(expected_msg="Type foo is not a valid property type"):
        YamlProperty(property_yaml_obj)

def test_valid_name(property_yaml_obj):
    property_yaml_obj['name'] = 'FooBar'

    with assert_raises_validation_error(expected_msg="FooBar is not a valid property name"):
        YamlProperty(property_yaml_obj)

def test_type_any_to_json(property_type_any_yaml_obj):
    prop = YamlProperty.from_yaml(property_type_any_yaml_obj)

    actual = prop.to_json()

    assert 'type' not in actual
