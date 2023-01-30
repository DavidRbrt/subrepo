#!/usr/bin/python3

import argparse
import os
import subprocess
import pathlib
import json
import jsonschema

DEFAULT_JSONFILE = 'subrepos.json'

# Expected schema for subrepos.json
# see https://json-schema.org/learn/getting-started-step-by-step to edit it
JSON_SCHEMA = {
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


class bformat:
    # colors
    DEFAULT   = '\033[00m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    #
    SUCCESS = GREEN + BOLD
    ERROR   = RED

    # symbols
    CHECKMARK = '\u2713'
    CROSSMARK = '\u2a2f'
    #
    SUCCESSMARK = GREEN + CHECKMARK + DEFAULT
    ERRORMARK = RED + CROSSMARK + DEFAULT


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


def fetch_all(base_dir, subrepo_list):
    for subrepo in subrepo_list:
        os.chdir(base_dir)

        # create local folder and go in
        pathlib.Path(subrepo.local_path).mkdir(parents=True, exist_ok=True)
        os.chdir(subrepo.local_path)

        # clone project if it doesn't exist
        if not os.path.exists(subrepo.repo_name + '/.git'):
            result = subprocess.run(['git', 'clone', f'{subrepo.repo_path}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] {subrepo.repo_name}: clone {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] {subrepo.repo_name}: cloned ({subrepo.local_path}/{subrepo.repo_name})')
        else:
            os.chdir(subrepo.repo_name)
            remote_url = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.split('\n')[0]
            if remote_url== subrepo.repo_path:
                print(f'[{bformat.SUCCESSMARK}] {subrepo.repo_name}: already cloned ({subrepo.local_path}/{subrepo.repo_name})')
            else:
                print(f'[{bformat.ERRORMARK}] {subrepo.repo_name}: already cloned ({subrepo.local_path}/{subrepo.repo_name}) from a different url ({remote_url})')
            os.chdir('..')
        
        # go in project folder and checkout revision if there is no local changes
        os.chdir(subrepo.repo_name)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        if not result.stdout:
            result = subprocess.run(['git', 'checkout', f'{subrepo.revision}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] {subrepo.repo_name}: checkout to {subrepo.revision} {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] {subrepo.repo_name}: checked out to {subrepo.revision}')
        else:
            print(f'[{bformat.ERRORMARK}] {subrepo.repo_name}: checkout to {subrepo.revision} {bformat.ERROR}\nThere are local changes{bformat.DEFAULT}')

    os.chdir(base_dir)


def command_line_parser():
    parser = argparse.ArgumentParser(description='subrepo')

    parser.add_argument('-u', '--update', help='fetch all subrepos', required=False, default=False, action='store_true')
    parser.add_argument('-j', '--jsonfile', help='json input file', required=False , type=str, default=DEFAULT_JSONFILE)

    args, _ = parser.parse_known_args()

    return args.update, args.jsonfile


def main():
    update, jsonfile = command_line_parser()

    base_dir = os.path.realpath(os.path.dirname(__file__))

    if update:
        data = open_json(jsonfile)
        subrepo_list = parse_subrepo_data(data)
        fetch_all(base_dir, subrepo_list)


if __name__ == '__main__':
    main()
