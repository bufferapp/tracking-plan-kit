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

IDENTIFY_FILE = """
traits:
  - name: email
    description: email
    type: string
    required: false
    allowNull: true
    pattern: (^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)
  - name: signupAttributionSource
    description: signupAttributionSource
    type: string
    required: false
    allowNull: true
"""

def _create_plan_file(tmpdir):
  p = tmpdir / "plan.yaml"
  p.write(TRACKING_PLAN_FILE)

def _create_events(tmpdir):
    e = tmpdir.mkdir('events').mkdir('experiments').join('experiment-enrolled.yaml')
    e.write(EVENT_FILE)

def _create_identify_file(tmpdir):
  i = tmpdir / "identify_traits.yaml"
  i.write(IDENTIFY_FILE)

def test_loader_tracking_plan(tmpdir):
    _create_plan_file(tmpdir)

    loader = PlanLoader(tmpdir)
    yaml_obj = yaml.safe_load(TRACKING_PLAN_FILE)
    expected = YamlTrackingPlan.from_yaml(yaml_obj)
    actual = loader.plan

    assert expected.name == actual.name
    assert expected.display_name == actual.display_name

def test_loader_events(tmpdir):
    _create_plan_file(tmpdir)
    _create_events(tmpdir)

    loader = PlanLoader(tmpdir)
    yaml_event_obj = yaml.safe_load(EVENT_FILE)
    expected = YamlEvent.from_yaml(yaml_event_obj)
    events = loader.plan.events

    assert len(events) == 1
    actual = events[0]
    assert expected.name == actual.name

def test_loader_identify(tmpdir):
  _create_plan_file(tmpdir)
  _create_identify_file(tmpdir)

  loader = PlanLoader(tmpdir)
  traits = loader.plan.identify_traits

  assert len(traits) == 2