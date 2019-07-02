from tracking_plan.yaml_event_property import YamlEventProperty

class YamlEvent(object):
    def __init__(self, event_yaml):
        self._event_yaml = event_yaml
        for attr in ['area', 'description', 'name']:
            setattr(self, f'_{attr}', event_yaml.get(attr))

        self._properties = [YamlEventProperty(p) for p in event_yaml['properties']]

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
    def parse_yaml(cls, yaml_obj):
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
