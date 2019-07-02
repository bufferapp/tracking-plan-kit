from pathlib import Path
import yaml
from tracking_plan.yaml_tracking_plan import YamlTrackingPlan

class PlanLoader(object):
    def __init__(self, root_dir):
        # load plan.yaml
        with open(root_dir / "plan.yaml", 'r') as pf:
            yaml_obj = yaml.safe_load(pf)
            self._plan =  YamlTrackingPlan.from_yaml(yaml_obj)

        # load events
        for yaml_file in Path(root_dir / 'events').glob('**/*.yaml'):
            with open(yaml_file, 'r') as f:
                yaml_event_obj = yaml.safe_load(f)
                self._plan.add_event(yaml_event_obj)

    @property
    def plan(self):
        return self._plan