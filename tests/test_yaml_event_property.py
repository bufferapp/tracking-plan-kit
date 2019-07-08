import pytest
import yaml
from tracking_plan.yaml_event_property import YamlEventProperty
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

def test_parsing_top_level_attrs(property_yaml_obj):
    prop = YamlEventProperty.from_yaml(property_yaml_obj)

    assert prop.name == 'variation'
    assert prop.description == 'What variation of the group'
    assert prop.type == 'string'
    assert prop.required == False
    assert prop.allow_null == True

def test_default_values(property_yaml_obj):
    property_yaml_obj.pop('required')
    property_yaml_obj.pop('allowNull')

    prop = YamlEventProperty.from_yaml(property_yaml_obj)

    assert prop.required == False
    assert prop.allow_null == False

def test_to_json(property_yaml_obj):
    prop = YamlEventProperty.from_yaml(property_yaml_obj)

    expected = {
        'description': 'What variation of the group',
        'pattern': 'experiment|control',
        'type': [
            'string',
            'null'
        ],
        'id': "/properties/properties/properties/variation"
    }

    actual = prop.to_json()

    assert expected == actual

def test_validate_pattern_on_string_type(property_yaml_obj):
    property_yaml_obj['type'] = 'number'
    with pytest.raises(ValidationError) as err_info:
        YamlEventProperty(property_yaml_obj)
    expected_msg = f'Property variation cannot specify a pattern'

    assert expected_msg in str(err_info.value)