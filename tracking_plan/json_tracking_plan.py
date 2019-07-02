import os
import shutil
from glob import glob
from pathlib import Path

import json
import yaml

from inflection import underscore, dasherize, camelize

class JsonTrackingPlan(object):
    def __init__(self, json_obj):
        self._json_obj = json_obj

    @classmethod
    def parse_string(cls, json_string):
        parsed_json = json.loads(json_string)
        plan = cls(parsed_json)

        return plan

    @classmethod
    def parse_file(cls, json_file_path):
        with open(json_file_path, 'r') as f:
            contents = f.read()
            return cls.parse_string(contents)

    @property
    def display_name(self):
        return self._json_obj.get('display_name')

    @property
    def name(self):
        return self._json_obj.get('name')

    def dump(self, path):
        # create the folder structure
        inflected_name = dasherize(underscore(
            self.display_name.replace(' ', '')))
        root_dir = os.path.join(path, inflected_name)
        events_dir = os.path.join(root_dir, 'events')
        if os.path.isdir(root_dir):
            shutil.rmtree(root_dir)  # first drop everything before recreating

        for d in [root_dir, events_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

        self._dump_plan_file(root_dir)

        # dump the events
        for event_json in self._json_obj.get('rules', {}).get('events', []):
            self._dump_event_file(events_dir, event_json)

    def _dump_plan_file(self, root_dir):
        plan_file = os.path.join(root_dir, 'plan.yaml')

        plan_obj = {
            'name': self.name,
            'display_name': self.display_name
        }

        with open(plan_file, 'w') as f:
            yaml.dump(plan_obj, f)

    def _dump_event_file(self, events_dir, event_json):
        event_labels = event_json.get('rules').get('labels')
        event_area = event_labels.get('area')
        event_product = event_labels.get('product')

        event_name = event_json.get('name')
        inflected_name = dasherize(underscore(event_name.replace(' ', '')))
        area_dir = os.path.join(events_dir, event_area)
        if event_product:
            event_dir = os.path.join(area_dir, event_product)
        else:
            event_dir = area_dir

        if not os.path.exists(event_dir):
            os.makedirs(event_dir)

        event_file = os.path.join(event_dir, f'{inflected_name}.yaml')

        event_obj = {
            'name': event_json.get('name'),
            'description': event_json.get('description'),
            'area': event_area
        }
        if event_product:
            event_obj['product'] = event_product

        properties = (event_json.get('rules')
                      .get('properties')
                      .get('properties')
                      .get('properties'))

        required = (event_json.get('rules')
                    .get('properties')
                    .get('properties')
                    .get('required', []))

        event_obj_properties = []
        for name, prop in properties.items():
            p_types = prop.get('type')
            if not isinstance(p_types, (list,)):
                p_types = [p_types] #sometimes this is not a list, just make it one
            p = {
                'name': name,
                'description': prop.get('description'),
                'type': p_types[0],
                'allowNull': len(p_types) < 2 or p_types[1] != 'null'
            }
            if name in required:
                p['required'] = True
            event_obj_properties.append(p)

        event_obj['properties'] = event_obj_properties

        with open(event_file, 'w') as f:
            yaml.dump(event_obj, f, sort_keys=False)
