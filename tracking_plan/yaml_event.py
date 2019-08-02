from tracking_plan.yaml_property import YamlProperty
from tracking_plan.errors import ValidationError
from tracking_plan.string_utilities import is_sentence_case
from tracking_plan.validation import check_required

class YamlEvent(object):
    def __init__(self, event_yaml):
        self._event_yaml = event_yaml
        self._properties = [YamlProperty(p) for p in event_yaml['properties']]
        self.validate()

    @property
    def area(self):
        return self._event_yaml.get('area')

    @property
    def description(self):
        return self._event_yaml.get('description')

    @property
    def name(self):
        return self._event_yaml.get('name')

    @property
    def properties(self):
        return self._properties

    @classmethod
    def from_yaml(cls, yaml_obj):
        return cls(yaml_obj)

    def to_json(self):
        event_properties = {p.name: p.to_json() for p in self._properties}
        required_properties = [p.name for p in self._properties if p.required]
        labels = {k:v for (k,v) in self._event_yaml.items() if k in ['area', 'product']}
        return {
            'version': 1,
            'name': self.name,
            'description': self.description,
            'rules': {
                'labels': labels,
                'properties': {
                    'context': {},
                    'traits': {},
                    'properties': {
                        'type': 'object',
                        'properties': event_properties,
                        'required': required_properties
                    }
                },
                'required': ['properties'],
                '$schema': 'http://json-schema.org/draft-07/schema#',
                'type': 'object'
            }
        }

    def _check_valid_name(self):
        if not is_sentence_case(self.name):
            raise ValidationError(f'{self.name} is not a valid event name')

    def validate(self):
        check_required(self, 'area', 'description', 'name', 'properties')
        self._check_valid_name()