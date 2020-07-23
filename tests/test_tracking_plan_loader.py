import os
import yaml
from tests.helpers import assert_raises_validation_error

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
    pattern: (^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)
  - name: signupAttributionSource
    description: signupAttributionSource
    type: string
    required: false
    allowNull: true
"""

GROUP_FILE = """
traits:
  - name: organizationID
    description: organizationID
    type: string
    required: false
    allowNull: false
"""
def _create_plan_file(tmpdir):
  p = tmpdir / "plan.yaml"
  p.write(TRACKING_PLAN_FILE)

def _create_events(tmpdir, contents=EVENT_FILE):
    e = tmpdir.mkdir('events').mkdir('experiments').join('experiment-enrolled.yaml')
    e.write(contents)

def _create_identify_file(tmpdir):
  i = tmpdir / "identify_traits.yaml"
  i.write(IDENTIFY_FILE)

def _create_group_file(tmpdir):
  g = tmpdir / "group_traits.yaml"
  g.write(GROUP_FILE)

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

def test_loader_group(tmpdir):
  _create_plan_file(tmpdir)
  _create_group_file(tmpdir)

  loader = PlanLoader(tmpdir)
  traits = loader.plan.group_traits

  assert len(traits) == 1

def test_loader_validation(tmpdir):
  _create_plan_file(tmpdir)

  #mess with file to cause validation errors
  event_yaml = yaml.safe_load(EVENT_FILE)
  event_yaml.pop('name')
  _create_events(tmpdir, contents=event_yaml)
  with assert_raises_validation_error():
    loader = PlanLoader(tmpdir)


def test_loader_collect_validation_errors(tmpdir):
  _create_plan_file(tmpdir)

  #mess with file to cause validation errors
  event_yaml = yaml.safe_load(EVENT_FILE)
  event_yaml.pop('name')
  _create_events(tmpdir, contents=event_yaml)
  loader = PlanLoader(tmpdir, raise_validation_errors=False)
  assert loader.has_validation_errors
  assert len(loader.validation_errors) == 1
