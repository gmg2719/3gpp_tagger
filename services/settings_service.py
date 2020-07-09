import requests
import json
from utils.path_finder import resolve_path_from_project_dir
from requests.auth import HTTPBasicAuth

from utils.service_utils import get_service_config, get_auth_params


class SettingService:

    def __init__(self, ssl_verify=False, environment=1):
        self.entities_json = resolve_path_from_project_dir('configs/entity_configuration.json')
        self.ssl_verify = ssl_verify
        self.environment = environment

    def get_project_setting(self):
        service = get_service_config('get_project_setting', self.environment)
        service_auth, service_params, service_endpoint = get_auth_params(service)
        result = requests.get(url=service_endpoint, params=service_params,
                              auth=service_auth, verify=self.ssl_verify)

        data = result.json()['entities']
        with open(self.entities_json, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
            f.close()
