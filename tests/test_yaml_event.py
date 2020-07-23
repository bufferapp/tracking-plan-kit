import pytest
from tests.helpers import assert_required, assert_raises_validation_error
import yaml
from tracking_plan.yaml_event import YamlEvent
from tracking_plan.yaml_property import YamlProperty
from tracking_plan.errors import ValidationError

@pytest.fixture
def experiments_yaml_obj():
  return yaml.safe_load("""
  area: experiments
  description: Track whom has been added to an A/B Test Experiment
  name: Experiment Enrolled
  properties:
    - name: experiment
      description: The name of the experiment
      type: string
      required: true
    - name: variation
      description: What variation of the group (i.e. ""control"" ""experiment"")
      type: string
  """)

@pytest.fixture
def tag_created_yaml_obj():
  return yaml.safe_load("""
    name: Tag Created
    description: A conversation tag was created
    area: product
    product: reply
    properties: []
  """)

@pytest.fixture
def dup_properties_yaml_obj():
  return yaml.safe_load("""
  name: Foo Created
  description: foo
  area: product
  properties:
    - name: foo
      description: foo
      type: string
      required: true
    - name: foo
      description: foo
      type: string
  """)

def test_parsing_top_level_attrs(experiments_yaml_obj):
    event = YamlEvent.from_yaml(experiments_yaml_obj)

    assert event.area == 'experiments'
    assert event.description == 'Track whom has been added to an A/B Test Experiment'
    assert event.name == 'Experiment Enrolled'

def test_parsing_properties(experiments_yaml_obj):
    event = YamlEvent.from_yaml(experiments_yaml_obj)

    assert len(event.properties) == 2
    experiment_property = event.properties[0]

    assert type(experiment_property) == YamlProperty
    assert experiment_property.name == 'experiment'

def test_parsing_tags(tag_created_yaml_obj):
    event = YamlEvent.from_yaml(tag_created_yaml_obj)
    actual = event.to_json()['rules']['labels']

    assert actual['area'] == 'product'
    assert actual['product'] == 'reply'

def test_to_json(experiments_yaml_obj):
  event = YamlEvent.from_yaml(experiments_yaml_obj)
  event_properties = {}
  for p in experiments_yaml_obj['properties']:
    event_properties[p['name']] = YamlProperty.from_yaml(p).to_json()

  expected = {
    'version': 1,
    'name': 'Experiment Enrolled',
    'description': 'Track whom has been added to an A/B Test Experiment',
    'rules': {
        'labels': {
          'area': 'experiments'
        },
        'properties': {
            'context': {},
            'traits': {},
            'properties': {
                'type': 'object',
                'properties': event_properties,
                'required': ['experiment']
            }
        },
        'required': ['properties'],
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'type': 'object'
    }
  }

  actual = event.to_json()
  assert expected == actual

def test_required_fields(tag_created_yaml_obj):
  assert_required(YamlEvent, tag_created_yaml_obj, 'name')
  assert_required(YamlEvent, tag_created_yaml_obj, 'description')
  assert_required(YamlEvent, tag_created_yaml_obj, 'area')

def test_duplicate_properties(dup_properties_yaml_obj):
  with assert_raises_validation_error(f'Duplicate properties found on event Foo Created. Properties: foo'):
      YamlEvent.from_yaml(dup_properties_yaml_obj)

def test_valid_name(tag_created_yaml_obj):
  tag_created_yaml_obj['name'] = 'Foo bar'

  with assert_raises_validation_error('Foo bar is not a valid event name'):
    YamlEvent(tag_created_yaml_obj)