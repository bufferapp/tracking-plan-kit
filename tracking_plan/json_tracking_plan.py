import os
import shutil
from glob import glob
from pathlib import Path

import json
import yaml

from inflection import underscore, dasherize, camelize

from tracking_plan.json_utils import parse_json_event, parse_json_property

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
        traits_json = self._json_obj. \
            get('rules'). \
            get('identify', {}). \
            get('properties', {}). \
            get('traits', {}). \
            get('properties')
        if traits_json:
            self._dump_identify_file(root_dir, traits_json)

        group_traits_json = self._json_obj. \
            get('rules'). \
            get('group', {}). \
            get('properties', {}). \
            get('traits', {}). \
            get('properties')

        if group_traits_json:
            self._dump_group_file(root_dir, group_traits_json)


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

        event_obj = parse_json_event(event_json)

        event_area = event_obj.get('area')
        event_product = event_obj.get('product')
        event_name = event_obj.get('name')

        inflected_name = dasherize(underscore(event_name.replace(' ', '')))
        area_dir = os.path.join(events_dir, event_area)
        if event_product:
            event_dir = os.path.join(area_dir, event_product)
        else:
            event_dir = area_dir

        if not os.path.exists(event_dir):
            os.makedirs(event_dir)

        event_file = os.path.join(event_dir, f'{inflected_name}.yaml')

        with open(event_file, 'w') as f:
            yaml.dump(event_obj, f, sort_keys=False)

    def _dump_identify_file(self, root_dir, traits_json):
        traits = [parse_json_property(name, prop_json)
            for (name, prop_json) in traits_json.items()]

        traits_obj = {
            'traits': traits
        }
        traits_file = os.path.join(root_dir, 'identify_traits.yaml')

        with open(traits_file, 'w') as f:
            yaml.dump(traits_obj, f, sort_keys=False)

    def _dump_group_file(self, root_dir, group_traits_json):
        traits = [parse_json_property(name, prop_json)
            for (name, prop_json) in group_traits_json.items()]

        traits_obj = {
            'traits': traits
        }
        traits_file = os.path.join(root_dir, 'group_traits.yaml')

        with open(traits_file, 'w') as f:
            yaml.dump(traits_obj, f, sort_keys=False)