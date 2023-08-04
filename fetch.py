import os
import subprocess
import pathlib

# project imports
import bformat
from parse_dependencies_file import read_json, parse_subrepo_data


def fetch_list(base_dir, dir, subrepo_list, depth):

    repo_prefix = ''

    for i in range(depth):
        repo_prefix += f'{bformat.NESTEDMARK}'

    for subrepo in subrepo_list:
        os.chdir(dir)

        print(f'{bformat.BOLD}{repo_prefix}{subrepo.repo_name}{bformat.DEFAULT}')

        # create local folder and go in
        pathlib.Path(subrepo.local_path).mkdir(parents=True, exist_ok=True)
        os.chdir(subrepo.local_path)

        complete_subrepo_local_path = os.path.realpath(os.path.join(dir, subrepo.local_path, subrepo.repo_name)).replace(base_dir, '.')

        # clone project if it doesn't exist
        if not os.path.exists(subrepo.repo_name + '/.git'):
            result = subprocess.run(['git', 'clone', f'{subrepo.repo_path}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] clone {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] cloned ({complete_subrepo_local_path})')
        else:
            os.chdir(subrepo.repo_name)
            remote_url = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.split('\n')[0]
            if remote_url== subrepo.repo_path:
                print(f'[{bformat.SUCCESSMARK}] already cloned ({complete_subrepo_local_path})')
            else:
                print(f'[{bformat.ERRORMARK}] already cloned ({complete_subrepo_local_path}) from a different url ({remote_url})')
            os.chdir('..')
        
        # go in project folder and checkout revision if there is no local changes
        os.chdir(subrepo.repo_name)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        if not result.stdout:
            result = subprocess.run(['git', 'checkout', f'{subrepo.revision}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] checkout to {subrepo.revision} {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            result = subprocess.run(['git', 'pull', 'origin', f'{subrepo.revision}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] pull origin {subrepo.revision} {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] checked out to {subrepo.revision}')
        else:
            print(f'[{bformat.ERRORMARK}] checkout to {subrepo.revision} {bformat.ERROR}\nThere are local changes{bformat.DEFAULT}')

    os.chdir(dir)


def fetch_all(base_dir, dir, dependencies_filename, recursive, depth=0):
    dependencies_file = os.path.join(dir, dependencies_filename)
    
    if not os.path.exists(dependencies_file):
        print(f'{bformat.CYAN}no nested dependencies found here{bformat.DEFAULT}')
        return

    json_data = read_json(dependencies_file)
    subrepo_list = parse_subrepo_data(json_data)

    fetch_list(base_dir, dir, subrepo_list, depth)

    if recursive:
        depth += 1
        for subrepo in subrepo_list:
            subrepo_dir = os.path.realpath(os.path.join(dir, subrepo.local_path, subrepo.repo_name))
            fetch_all(base_dir, subrepo_dir, dependencies_filename, recursive, depth)