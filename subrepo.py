import argparse
import os
# import subprocess
import pathlib
import json
import jsonschema
from pathlib import Path

from json_schema import JSON_SCHEMA
from fetch_all import fetch_all
from generate_version import generate_version_file


class Subrepo:
    def __init__(self, repo_path, revision='master', local_path='.'):
        self.repo_path = repo_path
        self.revision = revision
        self.local_path = local_path
        #
        self.repo_name = pathlib.Path(repo_path).stem


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


def command_line_parser():
    parser = argparse.ArgumentParser(description='subrepo')

    parser.add_argument('-d', '--dependencies-file', help='dependencies input file', required=False, type=str, default=None)
    parser.add_argument('-u', '--update', help='fetch all subrepos', required=False, default=False, action='store_true')
    parser.add_argument('-g', '--generate-version', help='generate a header version file for target language (c)', required=False, type=str, default=None)

    args, _ = parser.parse_known_args()

    return args.dependencies_file, args.update, args.generate_version


def main():
    dependencies_file, update, generate_version = command_line_parser()

    if dependencies_file:
        base_dir = os.path.dirname(Path(dependencies_file).resolve())
    else:
        base_dir = os.getcwd()

    if update:
        if not dependencies_file:
            print("Error: you need to provides a dependencies JSON file")
            return
        json_data = read_json(dependencies_file)
        subrepo_list = parse_subrepo_data(json_data)
        fetch_all(base_dir, subrepo_list)

    if generate_version:
        if dependencies_file:
            json_data = read_json(dependencies_file)
            subrepo_list = parse_subrepo_data(json_data)
        else:
            subrepo_list = None
        generate_version_file(base_dir, generate_version, subrepo_list)


if __name__ == '__main__':
    main()
