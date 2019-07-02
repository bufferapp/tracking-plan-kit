import pytest
import yaml
from tracking_plan.yaml_tracking_plan import YamlTrackingPlan
from tracking_plan.yaml_event import YamlEvent


@pytest.fixture
def tracking_plan_yaml():
    return yaml.safe_load("""
    display_name: Test Tracking Plan
    name: workspaces/buffer/tracking-plans/rs_1MEdD4BRxkZ6yk4XbJuzsu48V0M
    """)

@pytest.fixture
def tracking_plan_event_yaml():
    return yaml.safe_load("""
    name: Test Event
    properties: []
    """)

def test_parsing_top_level_attrs(tracking_plan_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)

    assert plan.display_name == 'Test Tracking Plan'
    assert plan.name == 'workspaces/buffer/tracking-plans/rs_1MEdD4BRxkZ6yk4XbJuzsu48V0M'

def test_adding_events(tracking_plan_yaml, tracking_plan_event_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)
    plan.add_event(tracking_plan_event_yaml)

    assert len(plan.events) == 1

def test_to_json_top_level_attrs(tracking_plan_yaml, tracking_plan_event_yaml):
    plan = YamlTrackingPlan(tracking_plan_yaml)

    json_plan = plan.to_json()

    assert json_plan['display_name'] == plan.display_name
    assert json_plan['name'] == plan.name

def test_to_json_events(tracking_plan_yaml, tracking_plan_event_yaml):
    plan = YamlTrackingPlan(tracking_plan_yaml)
    plan.add_event(tracking_plan_event_yaml)

    json_plan = plan.to_json()

    assert len(json_plan['rules']['events']) == 1

    expected = YamlEvent.parse_yaml(tracking_plan_event_yaml).to_json()
    actual = json_plan['rules']['events'][0]
    assert actual == expected


