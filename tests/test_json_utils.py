import pytest
import yaml
from tracking_plan.json_utils import parse_json_event

@pytest.fixture
def product_signup_json_obj():
  return {
    'version': 1,
    'name': 'Product Signup',
    'description': 'A user signs up for a given product',
    'rules': {
        'labels': {
          'area': 'product',
          'product': 'fakeproduct'
        },
        'properties': {
            'context': {},
            'traits': {},
            'properties': {
                'type': 'object',
                 'properties': {
                    'cta': {
                        'description': 'Where did the user come from the start the trial',
                        'type': [
                            'string',
                            'null'
                        ]
                    },
                    'product': {
                        'description': 'What product did this event occur in or for?',
                        'type': 'string'
                    }
                },
                'required': [
                    'product'
                ]
            }
        },
        'required': ['properties'],
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'type': 'object'
    }
  }


def test_parse_json_event(product_signup_json_obj):
    event = parse_json_event(product_signup_json_obj)

    assert event['name'] == 'Product Signup'
    assert event['area'] == 'product'
    assert event['product'] == 'fakeproduct'
    assert event['description'] == 'A user signs up for a given product'
    assert len(event['properties']) == 2

    cta_property = next(p for p in event['properties'] if p['name'] == 'cta')
    product_property = next(p for p in event['properties'] if p['name'] == 'product')

    assert cta_property['name'] == 'cta'
    assert cta_property['description'] == 'Where did the user come from the start the trial'
    assert cta_property['allowNull'] == True
    assert ('required' not in cta_property)
    assert product_property['name'] == 'product'
    assert product_property['description'] == 'What product did this event occur in or for?'
    assert ('allowNull' not in product_property)
    assert product_property['required'] == True

