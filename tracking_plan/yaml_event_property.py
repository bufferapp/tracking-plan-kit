class YamlEventProperty(object):
    def __init__(self, property_yaml):
        self._property_yaml = property_yaml

    @property
    def name(self):
        return self._property_yaml.get('name')

    @property
    def description(self):
        return self._property_yaml.get('description')

    @property
    def type(self):
        return self._property_yaml.get('type')

    @property
    def required(self):
        return self._property_yaml.get('required', False)

    @property
    def allow_null(self):
        return self._property_yaml.get('allowNull', False)

    @property
    def pattern(self):
        return self._property_yaml.get('pattern')

    @classmethod
    def from_yaml(cls, property_yaml):
        return cls(property_yaml)

    def to_json(self):
        p_types = [self.type]
        if self.allow_null:
            p_types.append('null')

        output = {
            'description': self.description,
            'type': p_types,
            'id': f"/properties/properties/properties/{self.name}"
        }
        if self.pattern:
            output['pattern'] = self.pattern

        return output