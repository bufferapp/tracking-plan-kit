import os
import yaml

from tracking_plan.yaml_tracking_plan import YamlTrackingPlan
from tracking_plan.yaml_event import YamlEvent
from tracking_plan.plan_loader import PlanLoader

TRACKING_PLAN_FILE = """
display_name: Test Tracking Plan
name: workspaces/buffer/tracking-plans/rs_1MEdD4BRxkZ6yk4XbJuzsu48V0M
"""

EVENT_FILE = """
  area: experiments
  description: Track whom has been added to an A/B Test Experiment
  name: Experiment Enrolled
  properties:
    - name: experiment
      description: The name of the experiment
      type: string
    - name: variation
      description: What variation of the group (i.e. ""control"" ""experiment"")
      type: string
      required: false
"""


def test_loader_tracking_plan(tmpdir):
    p = tmpdir / "plan.yaml"
    p.write(TRACKING_PLAN_FILE)

    loader = PlanLoader(tmpdir)
    yaml_obj = yaml.safe_load(TRACKING_PLAN_FILE)
    expected = YamlTrackingPlan.from_yaml(yaml_obj)
    actual = loader.plan

    assert expected.name == actual.name
    assert expected.display_name == actual.display_name

def test_loader_events(tmpdir):
    p = tmpdir / "plan.yaml"
    p.write(TRACKING_PLAN_FILE)

    e = tmpdir.mkdir('events').mkdir('experiments').join('experiment-enrolled.yaml')
    e.write(EVENT_FILE)

    loader = PlanLoader(tmpdir)
    yaml_event_obj = yaml.safe_load(EVENT_FILE)
    expected = YamlEvent.parse_yaml(yaml_event_obj)
    events = loader.plan.events

    assert len(events) == 1
    actual = events[0]
    assert expected.name == actual.name