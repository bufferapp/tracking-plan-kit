import pytest
import yaml
from tracking_plan.yaml_tracking_plan import YamlTrackingPlan
from tracking_plan.yaml_event import YamlEvent
from tracking_plan.yaml_property import YamlProperty
from tests.helpers import assert_required, assert_raises_validation_error


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
    description: Test Event
    area: test
    properties: []
    """)

@pytest.fixture
def tracking_plan_trait_yaml():
    return yaml.safe_load("""
        name: email
        description: email
        type: string
        """)

def test_parsing_top_level_attrs(tracking_plan_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)

    assert plan.display_name == 'Test Tracking Plan'
    assert plan.name == 'workspaces/buffer/tracking-plans/rs_1MEdD4BRxkZ6yk4XbJuzsu48V0M'

def test_adding_events(tracking_plan_yaml, tracking_plan_event_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)
    plan.add_event(tracking_plan_event_yaml)

    assert len(plan.events) == 1

def test_adding_identify_traits(tracking_plan_yaml, tracking_plan_trait_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)

    plan.add_identify_trait(tracking_plan_trait_yaml)

    assert len(plan.identify_traits) == 1

def test_adding_group_traits(tracking_plan_yaml, tracking_plan_trait_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)

    plan.add_group_trait(tracking_plan_trait_yaml)

    assert len(plan.group_traits) == 1

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

    expected = YamlEvent.from_yaml(tracking_plan_event_yaml).to_json()
    actual = json_plan['rules']['events'][0]
    assert actual == expected

def test_to_json_traits(tracking_plan_yaml, tracking_plan_trait_yaml):
    plan = YamlTrackingPlan(tracking_plan_yaml)
    plan.add_identify_trait(tracking_plan_trait_yaml)

    json_plan = plan.to_json()

    json_traits = json_plan['rules']['identify']['properties']['traits']['properties']

    assert len(json_traits) == 1
    expected = YamlProperty(tracking_plan_trait_yaml).to_json()
    actual = json_traits['email']
    assert actual == expected

def test_to_json_group_traits(tracking_plan_yaml, tracking_plan_trait_yaml):
    plan = YamlTrackingPlan(tracking_plan_yaml)
    plan.add_group_trait(tracking_plan_trait_yaml)

    json_plan = plan.to_json()

    json_traits = json_plan['rules']['group']['properties']['traits']['properties']

    assert len(json_traits) == 1
    expected = YamlProperty(tracking_plan_trait_yaml).to_json()
    actual = json_traits['email']
    assert actual == expected

def test_required_fields(tracking_plan_yaml):
    assert_required(YamlTrackingPlan, tracking_plan_yaml, 'name')

def test_duplicate_events(tracking_plan_yaml, tracking_plan_event_yaml):
    plan = YamlTrackingPlan.from_yaml(tracking_plan_yaml)
    plan.add_event(tracking_plan_event_yaml)

    with assert_raises_validation_error(expected_msg='Duplicate events found. Events: Test Event'):
        plan.add_event(tracking_plan_event_yaml)