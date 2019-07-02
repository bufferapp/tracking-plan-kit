import pytest
import yaml
from tracking_plan.yaml_event import YamlEvent
from tracking_plan.yaml_event_property import YamlEventProperty

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
    - name: variation
      description: What variation of the group (i.e. ""control"" ""experiment"")
      type: string
      required: false
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

def test_parsing_top_level_attrs(experiments_yaml_obj):
    event = YamlEvent.parse_yaml(experiments_yaml_obj)

    assert event.area == 'experiments'
    assert event.description == 'Track whom has been added to an A/B Test Experiment'
    assert event.name == 'Experiment Enrolled'

def test_parsing_properties(experiments_yaml_obj):
    event = YamlEvent.parse_yaml(experiments_yaml_obj)

    assert len(event.properties) == 2
    experiment_property = event.properties[0]

    assert type(experiment_property) == YamlEventProperty
    assert experiment_property.name == 'experiment'

def test_parsing_tags(tag_created_yaml_obj):
    event = YamlEvent.parse_yaml(tag_created_yaml_obj)
    actual = event.to_json()['rules']['labels']

    assert actual['area'] == 'product'
    assert actual['product'] == 'reply'

def test_to_json(experiments_yaml_obj):
  event = YamlEvent.parse_yaml(experiments_yaml_obj)
  event_properties = {}
  for p in experiments_yaml_obj['properties']:
    event_properties[p['name']] = YamlEventProperty.from_yaml(p).to_json()

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