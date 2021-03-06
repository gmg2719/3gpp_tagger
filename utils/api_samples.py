import requests

from utils.config_utils import get_index
from utils.file_utils import get_text_from_file
from utils.path_finder import resolve_path_from_project_dir
import torch
import torch.nn as nn
import spacy


def upload_verbatim_text():
    tagtogAPIUrl = "https://www.tagtog.net/-api/documents/v1"

    content = get_text_from_file(resolve_path_from_project_dir('configs/input_data.txt'))

    auth = requests.auth.HTTPBasicAuth(username="charantej", password="Password*01")
    params = {"project": "tagging_project", "owner": "charantej", "format": "verbatim", "output": "null"}
    payload = {
        "text": content
    }
    response = requests.post(tagtogAPIUrl, params=params, auth=auth, data=payload)


def verbatim_annotate():
    tagtogAPIUrl = "https://www.tagtog.net/-api/documents/v1"

    auth = requests.auth.HTTPBasicAuth(username="charantej", password="Password*01")
    params = {"project": "tagging_project", "owner": "charantej", "format": "verbatim-plus-annjson",
              "output": "null"}

    files = [
        ("plain", open(resolve_path_from_project_dir('configs/input_data.txt'))),
        ("ann.json", open(resolve_path_from_project_dir('configs/input_data.ann.json')))
    ]
    response = requests.post(tagtogAPIUrl, params=params, auth=auth, files=files)
    print(response.text)


def test_string_structure(input_string):
    start = 0
    end = 0
    for each in input_string.split('.'):
        end = start + len(each)
        print(f'{start} , {end} - {each}')
        start = 1 + end


def word_find_word():
    word = 'geeks for Geeks'.lower()
    # returns first occurrence of Substring
    result = word.find('charans')
    print("Substring 'geeks' found at index:", result)


def spacy_token():
    torch.manual_seed(1)
    word_to_ix = {"hello": 0, "world": 1}
    embeds = nn.Embedding(2, 5)  # 2 words in vocab, 5 dimensional embeddings
    lookup_tensor = torch.tensor([word_to_ix["hello"]], dtype=torch.long)
    hello_embed = embeds(lookup_tensor)
    print(hello_embed)


def word_embeddings(sentence):
    en = spacy.load('en')
    return en(sentence)


def check_dict():
    import re
    p = re.compile("ts \d{2}\.\d{3} \[(\d+)\]")
    for m in p.finditer('adfadf ts 36.300 [5]).sdfsd'):
        print(m.start(), m.group())


if __name__ == '__main__':
    check_dict()
