import requests
from utils.path_finder import resolve_path_from_project_dir
from utils.service_utils import get_auth_params, get_service_config
from utils.file_utils import get_text_from_file


class DocumentService:

    def push_annotated_text(self, annotation_file, text_file, verbatim=False):
        annotation_file = resolve_path_from_project_dir(annotation_file)
        text_file = resolve_path_from_project_dir(text_file)

        if not verbatim:
            service = get_service_config('push_annotated_text')
        else:
            service = get_service_config('push_annotated_text_verbatim')
        service_auth, service_params, service_endpoint = get_auth_params(service)
        with open(annotation_file, 'r') as f:
            annotation_text = f.read()
        if not verbatim:

            files = {
                'ann': ('charan.ann.json', annotation_text),
                'plain': ('charan.txt', open(text_file))
            }
        else:
            files = {
                'ann': ('plain', annotation_text),
                'plain': ('ann.json', open(annotation_file))
            }

        result = requests.post(url=service_endpoint, params=service_params,
                               auth=service_auth, files=files)
        print(result.json())

    def push_verbatim_text(self, verbatim_text_file):
        service = get_service_config('push_verbatim_text')
        service_auth, service_params, service_endpoint = get_auth_params(service)
        content = get_text_from_file(resolve_path_from_project_dir(verbatim_text_file))
        payload = {
            "text": content
        }
        response = requests.post(service_endpoint, params=service_params, auth=service_auth, data=payload)
        print(response.text)


if __name__ == '__main__':
    doc_service = DocumentService()
    doc_service.push_verbatim_text('configs/input_data.txt')