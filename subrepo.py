#!/usr/bin/python3

import argparse
import os
import pathlib
import json
from collections import OrderedDict
import jsonschema

# Expected schema for subrepos.json
# see https://json-schema.org/learn/getting-started-step-by-step to edit it
json_schema = {
    'title': 'subrepos.json',
    'type': 'object',
    'properties': {
        'default': {
            'type' : 'object',
            'properties':{
                'revision': { 'type': 'string' },
                'local_path': { 'type': 'string' },
            },
        },
        'list': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'repo_path': { 'type': 'string' },
                    'revision': { 'type': 'string' },
                    'local_path': { 'type': 'string' },
                },
                'required': [
                    'repo_path',
                ],
            },
            'minItems': 0,
            'uniqueItems': True,
        }
    },
    'required': [
        'list',
    ],
}

class Subrepo:
    def __init__(self, repo_path, revision='master', local_path='.'):
        self.repo_path = repo_path
        self.revision = revision
        self.local_path = local_path
        #
        self.repo_name = pathlib.Path(repo_path).stem

def open_json(file_path):
    try:
        data = json.load(open(file_path, 'r'))
    except FileNotFoundError as e:
        print(f'ERROR: Cannot open file {file_path} ({e})')
    except ValueError as e:
        print(f'ERROR: File {file_path} is not a valid json ({e})')

    try:
        jsonschema.validate(instance=data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f'ERROR: File {file_path} format is invalid: {e.message}')

    return data


def parse_subrepo_list(list):
    subrepo_list = []

    for element in list:
        repo_path = element['repo_path']
        revision = element['revision']
        local_path = element['local_path']
        subrepo_list.append(Subrepo(repo_path, revision, local_path))

    return subrepo_list


def fetch_all(base_dir, subrepo_list):
    for subrepo in subrepo_list:
        pathlib.Path(subrepo.local_path).mkdir(parents=True, exist_ok=True)
        os.chdir(subrepo.local_path)
        os.system(f'git clone {subrepo.repo_path}')
        os.chdir(subrepo.repo_name)
        os.system(f'git checkout {subrepo.revision}')
        os.chdir(base_dir)


def command_line_parser():
	parser = argparse.ArgumentParser(description='subrepo')

	parser.add_argument('-u', '--update', required=False, default=False, action='store_true', help='fetch all subrepos')

	args, _ = parser.parse_known_args()

	return args.update


def main():
    update = command_line_parser()

    base_dir = os.path.realpath(os.path.dirname(__file__))

    data = open_json('subrepos.json')
    subrepo_list = parse_subrepo_list(data['list'])

    # TODO: use default json param

    if update:
        print('fetching all subrepos ...')
        fetch_all(base_dir, subrepo_list)


if __name__ == '__main__':
	main()
