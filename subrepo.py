#!/usr/bin/python3

import argparse
import os
import pathlib

class Subrepo:
    """Subrepo object"""
    def __init__(self, repo_path, rev='master', local_path='.'):
        self.repo_path = repo_path
        self.rev = rev
        self.local_path = local_path
        #
        self.repo_name = pathlib.Path(repo_path).stem


def parse_subrepo_list():
    subrepo_list = []

    repo_path = 'git@github.com:DavidRbrt/dev-tools.git'
    rev = 'f303925686fc87ab2547bfee691d1d8be00f4b71'
    local_path = 'subrepos/yoyoyo'
    subrepo_list.append(Subrepo(repo_path, rev, local_path))

    repo_path = 'git@github.com:DavidRbrt/lookup-table-generator.git'
    rev = '798a91585f3ad29a9c28cad8a3c35ee725538aed'
    local_path = 'subrepos'
    subrepo_list.append(Subrepo(repo_path, rev, local_path))

    return subrepo_list


def fetch_all(base_dir, subrepo_list):
    for subrepo in subrepo_list:
        pathlib.Path(subrepo.local_path).mkdir(parents=True, exist_ok=True)
        os.chdir(subrepo.local_path)
        os.system(f'git clone {subrepo.repo_path}')
        os.chdir(subrepo.repo_name)
        os.system(f'git checkout {subrepo.rev}')
        os.chdir(base_dir)


def command_line_parser():
	parser = argparse.ArgumentParser(description="subrepo")

	parser.add_argument('-u', '--update', required=False, default=False, action='store_true', help="fetch all subrepos")

	args, _ = parser.parse_known_args()

	return args.update


def main():
    update = command_line_parser()

    base_dir = os.path.realpath(os.path.dirname(__file__))

    subrepo_list = parse_subrepo_list()

    if update:
        print("fetching all subrepos ...")
        fetch_all(base_dir, subrepo_list)


if __name__ == "__main__":
	main()
