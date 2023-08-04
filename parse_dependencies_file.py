import json
import jsonschema

# project imports
from json_schema import JSON_SCHEMA
from subrepo_class import Subrepo


def read_json(file_path):
    try:
        data = json.load(open(file_path, 'r'))
    except FileNotFoundError as e:
        print(f'ERROR: Cannot open file {file_path} ({e})')
    except ValueError as e:
        print(f'ERROR: File {file_path} is not a valid json ({e})')

    try:
        jsonschema.validate(instance=data, schema=JSON_SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print(f'ERROR: File {file_path} format is invalid: {e.message}')

    return data


def parse_subrepo_data(data):
    subrepo_list = []

    for element in data['list']:

        repo_path = element['repo_path']

        if 'local_path' in element:
            local_path = element['local_path']
        else:
            local_path = data['default']['local_path']

        if 'revision' in element:
            revision = element['revision']
        else:
            revision = data['default']['revision']

        subrepo_list.append(Subrepo(repo_path, revision, local_path))

    return subrepo_list
