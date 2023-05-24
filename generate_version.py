import os
import subprocess

# project imports
import bformat


C_HEADER=\
"""\
#ifndef VERSION_H_
#define VERSION_H_

/* 
 * This file has been generated by Subrepo python tool:
 * https://github.com/DavidRbrt/subrepo
 */

"""


C_FOOTER=\
"""\
#endif
"""


def c_write_project_version(file, subrepo=None):

    if subrepo:
        print(f'{bformat.BOLD}{subrepo.repo_name}{bformat.DEFAULT}')
        # check path exists and is a git repo
        if not os.path.exists(os.path.join(subrepo.local_path, subrepo.repo_name)):
            print(f'[{bformat.ERRORMARK}] needs to be fetched')
            return
        os.chdir(os.path.join(subrepo.local_path, subrepo.repo_name))
    else:
        print(f'{bformat.BOLD}project{bformat.DEFAULT}')

    if not os.path.exists('.git'):
        print(f'[{bformat.ERRORMARK}] not a git repo')
        return

    # get git informations
    git_repo = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.split('\n')[0]
    git_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.split('\n')[0]
    git_short_hash = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.split('\n')[0]
    git_tag = subprocess.run(['git', 'describe', '--tags'], capture_output=True, text=True).stdout.split('\n')[0]

    git_status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.split('\n')[0]
    
    if git_status == '':
        git_local_changes='false'
    else:
        git_local_changes='true'

    # write to file
    if subrepo:
        project_prefix = subrepo.repo_name.replace('-','_').upper() + '_'
    else:
        project_prefix = ''

    if subrepo:
        file.write(f'/* subrepo {subrepo.repo_name} ({os.path.join(subrepo.local_path, subrepo.repo_name)}) */\n')

    file.write(f'#define {project_prefix}GIT_REPO "{git_repo}"\n')
    file.write(f'#define {project_prefix}GIT_HASH "{git_hash}"\n')
    file.write(f'#define {project_prefix}GIT_SHORT_HASH "{git_short_hash}"\n')
    file.write(f'#define {project_prefix}GIT_TAG "{git_tag}"\n')
    file.write(f'#define {project_prefix}GIT_LOCAL_CHANGES {git_local_changes}\n')
    file.write(f'\n')

    print(f'[{bformat.SUCCESSMARK}] version generated')


def generate_c_version_file(base_dir, subrepo_list=None):
    os.chdir(base_dir)

    with open('version.h', 'w') as file:
        # append header
        file.write(C_HEADER)

        # append base project version
        c_write_project_version(file)

        # append project version for each subrepo
        if subrepo_list:
            for subrepo in subrepo_list:
                c_write_project_version(file, subrepo)

        # append footer
        file.write(C_FOOTER)


def generate_version_file(base_dir, language, subrepo_list=None):
    match language:
        case "c":
            generate_c_version_file(base_dir, subrepo_list)
        case _:
            return
    