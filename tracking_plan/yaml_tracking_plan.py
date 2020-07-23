from tracking_plan.yaml_event import YamlEvent
from tracking_plan.yaml_property import YamlProperty
from tracking_plan.errors import ValidationError
from tracking_plan.validation import check_required
from collections import Counter

class YamlTrackingPlan(object):
    def __init__(self, plan_yaml):
        self._plan_yaml = plan_yaml
        self._events = []
        self._identify_traits = []
        self._group_traits = []
        self.validate()

    @classmethod
    def from_yaml(cls, plan_yaml):
        plan = cls(plan_yaml)
        return plan

    @property
    def display_name(self):
        return self._plan_yaml.get('display_name')

    @property
    def name(self):
        return self._plan_yaml.get('name')

    @property
    def events(self):
        return self._events

    @property
    def identify_traits(self):
        return self._identify_traits

    @property
    def group_traits(self):
        return self._group_traits


    def add_event(self, event_yaml):
        event = YamlEvent(event_yaml)
        self._events.append(event)
        self.validate()

    def add_identify_trait(self, trait_yaml):
        trait_property = YamlProperty(trait_yaml)
        self._identify_traits.append(trait_property)

    def add_group_trait(self, trait_yaml):
        trait_property = YamlProperty(trait_yaml)
        self._group_traits.append(trait_property)

    def to_json(self):
        json_obj = {
            'name': self.name,
            'display_name': self.display_name,
            'rules': {
                'identify_traits': [],
                'group_traits': [],
                'events': []
            }
        }

        for event in self._events:
            json_obj['rules']['events'].append(event.to_json())

        if len(self.identify_traits) > 0:
            trait_properties = {t.name: t.to_json() for t in self.identify_traits}
            json_obj['rules']['identify'] = {
                'properties' : {
                    'traits' : {
                        'properties' : trait_properties
                    }
                },
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object"
            }

        if len(self.group_traits) > 0:
            trait_properties = {t.name: t.to_json() for t in self.group_traits}
            json_obj['rules']['group'] = {
                'properties' : {
                    'traits' : {
                        'properties' : trait_properties
                    }
                },
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object"
            }

        return json_obj

    def _check_duplicate_events(self):
        event_names = map(lambda e: e.name, self._events)
        counts = Counter(event_names)
        duplicates = {k:v for (k,v) in counts.items() if v > 1}
        if len(duplicates) > 0:
            duplicate_names = ', '.join(duplicates.keys())
            raise ValidationError(f'Duplicate events found. Events: {duplicate_names}')

    def validate(self):
        check_required(self, 'name')
        self._check_duplicate_events()