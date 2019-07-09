from pathlib import Path
import yaml
from tracking_plan.yaml_tracking_plan import YamlTrackingPlan

class PlanLoader(object):
    def __init__(self, root_dir):
        self._load_plan_file(root_dir / "plan.yaml")
        self._load_events(root_dir / "events")
        self._load_traits(root_dir/ "identify_traits.yaml")

    def _load_plan_file(self, path):
        with open(path, 'r') as pf:
            yaml_obj = yaml.safe_load(pf)
            self._plan =  YamlTrackingPlan.from_yaml(yaml_obj)

    def _load_events(self, path):
        for yaml_file in Path(path).glob('**/*.yaml'):
            with open(yaml_file, 'r') as f:
                yaml_event_obj = yaml.safe_load(f)
                self._plan.add_event(yaml_event_obj)

    def _load_traits(self, path):
        if not path.exists():
            return
        with open(path, 'r') as idf:
            yaml_obj = yaml.safe_load(idf)
            for trait in yaml_obj.get('traits', []):
                self._plan.add_trait(trait)


    @property
    def plan(self):
        return self._plan