from tracking_plan.yaml_event import YamlEvent
from tracking_plan.yaml_property import YamlProperty

class YamlTrackingPlan(object):
    def __init__(self, plan_yaml):
        self._plan_yaml = plan_yaml
        self._events = []
        self._traits = []

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
    def traits(self):
        return self._traits

    def add_event(self, event_yaml):
        event = YamlEvent(event_yaml)
        self._events.append(event)

    def add_trait(self, trait_yaml):
        trait_property = YamlProperty(trait_yaml)
        self._traits.append(trait_property)

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

        if len(self.traits) > 0:
            trait_properties = {t.name: t.to_json() for t in self._traits}
            json_obj['rules']['identify'] = {
                'properties' : {
                    'traits' : {
                        'properties' : trait_properties
                    }
                },
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object"
            }

        return json_obj