from tracking_plan.yaml_event import YamlEvent

class YamlTrackingPlan(object):
    def __init__(self, plan_yaml):
        self._plan_yaml = plan_yaml
        self._events = []

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

    def add_event(self, event_yaml):
        event = YamlEvent(event_yaml)
        self._events.append(event)

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

        return json_obj