from tracking_plan.errors import ValidationError
from tracking_plan.string_utilities import is_camel_case
from tracking_plan.validation import check_required

class YamlProperty(object):
    def __init__(self, property_yaml):
        self._property_yaml = property_yaml
        self.validate()

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
        output = {
            'description': self.description,
        }
        if self.type != 'any':
            output['type'] = [self.type]
            if self.allow_null:
                output['type'].append('null')
        if self.pattern:
            output['pattern'] = self.pattern

        return output

    def _check_if_pattern_is_valid(self):
        if self.type != 'string' and self.pattern:
            if self.type is None:
                print(self._property_yaml)
            message = f"Property {self.name} cannot specify a pattern. It's of type {self.type}."
            raise ValidationError(message)

    def _check_if_type_is_valid(self):
        if self.type not in ['any', 'array', 'object', 'boolean', 'integer', 'number', 'string']:
            raise ValidationError(f'Type {self.type} is not a valid property type')

    def _check_valid_name(self):
        if not is_camel_case(self.name):
            raise ValidationError(f'{self.name} is not a valid property name')

    def validate(self):
        check_required(self, 'name', 'description', 'type')
        self._check_if_type_is_valid()
        self._check_if_pattern_is_valid()
        self._check_valid_name()