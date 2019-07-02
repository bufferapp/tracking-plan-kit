import os
from pathlib import Path
import json
import stacklogging
import click
from segment.api import SegmentConfigApi
from tracking_plan.json_tracking_plan import JsonTrackingPlan
from tracking_plan.plan_loader import PlanLoader

logger = stacklogging.getLogger()

ACCESS_TOKEN = os.getenv("SEGMENT_ACCESS_TOKEN")
WORKSPACE = os.getenv('SEGMENT_WORKSPACE')
TRACKING_PLAN_ID = os.getenv('SEGMENT_TRACKING_PLAN_ID')

api = SegmentConfigApi(ACCESS_TOKEN)

@click.group()
def cli():
    pass

@click.command()
def dump_json():
    logger.info('Getting latest tracking plan from the Segment api.')
    data = api.get_tracking_plan(WORKSPACE, TRACKING_PLAN_ID)

    click.echo(json.dumps(data, indent=4))
    logger.info("Done dumping plan.")


@click.command()
@click.argument('output-dir')
def dump(output_dir):
    logger.info('Getting latest tracking plan from the Segment api.')
    data = api.get_tracking_plan(WORKSPACE, TRACKING_PLAN_ID)

    logger.info(f'Got the latest tracking plan, dumping it as yaml to {output_dir}.')
    plan = JsonTrackingPlan(data)
    plan.dump(output_dir)

    logger.info("Done dumping plan.")

@click.command()
@click.argument('input-dir')
def update(input_dir):

    logger.info(f'Loading tracking plan from dir {input_dir}.')
    loader = PlanLoader(Path(input_dir))
    plan = loader.plan

    logger.info('Loaded tracking plan, updating it on the api.')

    data = plan.to_json()
    api.update_tracking_plan(WORKSPACE, TRACKING_PLAN_ID, data)

    logger.info("Done updating plan.")


cli.add_command(dump)
cli.add_command(update)
cli.add_command(dump_json)

if __name__ == "__main__":
    cli()