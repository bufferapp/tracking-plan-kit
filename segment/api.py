import requests
import json

class SegmentConfigApi:

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://platform.segmentapis.com/v1beta'

    def send_request(self, verb, path, payload={}):
        url = f'{self.base_url}{path}'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.request(verb, url, headers = headers, data = payload)
        response.raise_for_status()
        return response.json()


    def get_tracking_plan(self, workspace_name, tracking_plan_id):
        path = f'/workspaces/{workspace_name}/tracking-plans/{tracking_plan_id}'
        return self.send_request('GET', path)

    def update_tracking_plan(self, workspace_name, tracking_plan_id, data):
        path = f'/workspaces/{workspace_name}/tracking-plans/{tracking_plan_id}'
        payload = {
            "update_mask": {
                "paths": [
                    "tracking_plan.display_name",
                    "tracking_plan.rules"
                ]
            },
            "tracking_plan": data
        }
        return self.send_request('PUT', path, payload=json.dumps(payload))
