from pathlib import Path
import yaml
from tracking_plan.errors import ValidationError
from tracking_plan.yaml_tracking_plan import YamlTrackingPlan

class PlanLoader(object):
    def __init__(self, root_dir, raise_validation_errors=True):
        self._validation_errors = []
        try:
            self._load_plan_file(root_dir / "plan.yaml")
            self._load_events(root_dir / "events")
            self._load_identify_traits(root_dir / "identify_traits.yaml")
            self._load_group_traits(root_dir / "group_traits.yaml")
        except ValidationError as error:
            if raise_validation_errors:
                raise error
            else:
                self._validation_errors.append(error)

    def _load_plan_file(self, path):
        with open(path, 'r') as pf:
            yaml_obj = yaml.safe_load(pf)
            self._plan =  YamlTrackingPlan.from_yaml(yaml_obj)

    def _load_events(self, path):
        for yaml_file in Path(path).glob('**/*.yaml'):
            with open(yaml_file, 'r') as f:
                yaml_event_obj = yaml.safe_load(f)
                self._plan.add_event(yaml_event_obj)

    def _load_identify_traits(self, path):
        if not path.exists():
            return
        with open(path, 'r') as idf:
            yaml_obj = yaml.safe_load(idf)
            for trait in yaml_obj.get('traits', []):
                self._plan.add_identify_trait(trait)

    def _load_group_traits(self, path):
        if not path.exists():
            return
        with open(path, 'r') as grp:
            yaml_obj = yaml.safe_load(grp)
            for trait in yaml_obj.get('traits', []):
                self._plan.add_group_trait(trait)



    @property
    def plan(self):
        return self._plan

    @property
    def has_validation_errors(self):
        return len(self._validation_errors) > 0

    @property
    def validation_errors(self):
        return self._validation_errors