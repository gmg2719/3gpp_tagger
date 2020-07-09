import requests
from utils.path_finder import resolve_path_from_project_dir
from utils.service_utils import get_auth_params, get_service_config
from utils.file_utils import get_text_from_file


class DocumentService:
    def __init__(self, ssl_verify=False, environment=1):
        self.ssl_verify = ssl_verify
        self.environment = environment

    def push_annotated_text(self, annotation_file, text_file):
        annotation_file = resolve_path_from_project_dir(annotation_file)
        text_file = resolve_path_from_project_dir(text_file)
        service = get_service_config('push_annotated_text',self.environment)
        service_auth, service_params, service_endpoint = get_auth_params(service)
        with open(annotation_file, 'r') as f:
            annotation_text = f.read()

        files = {
            'ann': ('charan.ann.json', annotation_text),
            'plain': ('charan.txt', open(text_file))
        }

        result = requests.post(url=service_endpoint, params=service_params,
                               auth=service_auth, files=files, verify=self.ssl_verify)
        print(result.json())

    def push_verbatim_text(self, verbatim_text_file):
        service = get_service_config('push_verbatim_text',self.environment)
        service_auth, service_params, service_endpoint = get_auth_params(service)
        content = get_text_from_file(resolve_path_from_project_dir(verbatim_text_file))
        payload = {
            "text": content
        }
        response = requests.post(service_endpoint, params=service_params, auth=service_auth, data=payload,
                                 verify=self.ssl_verify)
        print(response.text)

    def push_annotated_verbatim_text(self, annotation_file, text_file):
        service = get_service_config('push_annotated_text_verbatim',self.environment)
        service_auth, service_params, service_endpoint = get_auth_params(service)
        files = [
            ("plain", open(text_file)),
            ("ann.json", open(annotation_file))
        ]
        response = requests.post(service_endpoint, params=service_params, auth=service_auth, files=files,
                                 verify=self.ssl_verify)
        print(response.text)
