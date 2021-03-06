import re
import json

from utils.config_utils import get_index
from utils.path_finder import resolve_path_from_project_dir


def remove_additional_spaces(input_data):
    input_data = re.sub(r'[^\x00-\x7F]+', ' ', input_data)
    input_data = re.sub('\?', ' ', input_data)
    return re.sub('\s+', ' ', input_data)


def lemmatize_domain_data(input_data):
    input_data = remove_additional_spaces(input_data).lower()
    with open(resolve_path_from_project_dir('configs/entities.json'), 'r') as f:
        entity_dict = json.load(f)
        f.close()
    acronym_dict = entity_dict['acronyms']
    for key, value in acronym_dict.items():
        acronym_dict[key] = [remove_additional_spaces(each.strip()).lower() for each in value]
    input_data = input_data.split()
    for key, value in acronym_dict.items():
        for each in value:
            index = get_index(each, input_data)
            if index > -1:
                input_data[index] = key
    return " ".join(input_data)


def pre_process_file(file_name):
    path_of_file = resolve_path_from_project_dir(file_name)
    with open(path_of_file, 'r') as f:
        pre_processed = f.read()
        f.close()
    pre_processed = pre_processed.split('\n')
    post_processed = []
    for val in pre_processed:
        post_processed.append(lemmatize_domain_data(val))
    output_file = path_of_file.replace('.txt', '_processed.txt')
    with open(output_file, 'w') as f:
        f.write("\n".join(post_processed))
        f.close()
    return output_file
