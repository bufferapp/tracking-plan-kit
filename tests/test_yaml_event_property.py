import pytest
import yaml
from tracking_plan.yaml_event_property import YamlEventProperty


@pytest.fixture
def property_yaml_obj():
    return  yaml.safe_load("""
    name: variation
    description: What variation of the group
    type: string
    required: false
    allowNull: true
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

    assert prop.required == True
    assert prop.allow_null == False

def test_to_json(property_yaml_obj):
    prop = YamlEventProperty.from_yaml(property_yaml_obj)

    expected = {
        'description': 'What variation of the group',
        'type': [
            'string',
            'null'
        ],
        'id': "/properties/properties/properties/variation"
    }

    actual = prop.to_json()

    assert expected == actual