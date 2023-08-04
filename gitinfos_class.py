import os
import subprocess

# project imports
import bformat


class GitInfos:
    def __init__(self):
        if not os.path.exists('.git'):
            print(f'[{bformat.ERRORMARK}] not a git repo')
            return

        # get git informations
        self.repo = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.split('\n')[0]
        self.hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.split('\n')[0]
        self.short_hash = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.split('\n')[0]
        self.tag = subprocess.run(['git', 'describe', '--tags'], capture_output=True, text=True).stdout.split('\n')[0]

        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.split('\n')[0]
        
        if status == '':
            self.local_changes='false'
        else:
            self.local_changes='true'
