import os
import subprocess
import pathlib

# project imports
import bformat

def fetch_all(base_dir, subrepo_list):
    for subrepo in subrepo_list:
        os.chdir(base_dir)

        print(f'{bformat.BOLD}{subrepo.repo_name}{bformat.DEFAULT}')

        # create local folder and go in
        pathlib.Path(subrepo.local_path).mkdir(parents=True, exist_ok=True)
        os.chdir(subrepo.local_path)

        # clone project if it doesn't exist
        if not os.path.exists(subrepo.repo_name + '/.git'):
            result = subprocess.run(['git', 'clone', f'{subrepo.repo_path}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] clone {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] cloned ({subrepo.local_path}/{subrepo.repo_name})')
        else:
            os.chdir(subrepo.repo_name)
            remote_url = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.split('\n')[0]
            if remote_url== subrepo.repo_path:
                print(f'[{bformat.SUCCESSMARK}] already cloned ({subrepo.local_path}/{subrepo.repo_name})')
            else:
                print(f'[{bformat.ERRORMARK}] already cloned ({subrepo.local_path}/{subrepo.repo_name}) from a different url ({remote_url})')
            os.chdir('..')
        
        # go in project folder and checkout revision if there is no local changes
        os.chdir(subrepo.repo_name)
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        if not result.stdout:
            result = subprocess.run(['git', 'checkout', f'{subrepo.revision}'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f'[{bformat.ERRORMARK}] checkout to {subrepo.revision} {bformat.ERROR}\n{result.stderr}{bformat.DEFAULT}')
                continue
            print(f'[{bformat.SUCCESSMARK}] checked out to {subrepo.revision}')
        else:
            print(f'[{bformat.ERRORMARK}] checkout to {subrepo.revision} {bformat.ERROR}\nThere are local changes{bformat.DEFAULT}')

    os.chdir(base_dir)