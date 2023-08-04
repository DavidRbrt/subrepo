import os
import pathlib

# project imports
import bformat
from parse_dependencies_file import read_json, parse_subrepo_data
from gitinfos_class import GitInfos


def print_header(dir, parent_repos):
    infos_header = ""
    if not parent_repos:
        infos_header = "project"
    else:
        # for parent_repo in parent_repos:
        for i, parent_repo in enumerate(parent_repos):
            if i > 0:
                infos_header += pathlib.Path(parent_repo).stem + f" {bformat.NESTEDMARK}"
        infos_header += pathlib.Path(dir).stem

    print(f"{bformat.BOLD}{infos_header}{bformat.DEFAULT}")


def get_prefix(dir, parent_repos):
    prefix = ""

    if not parent_repos:
        prefix = ""
    else:
        # for parent_repo in parent_repos:
        for i, parent_repo in enumerate(parent_repos):
            if i > 0:
                prefix += pathlib.Path(parent_repo).stem.upper().replace("-", "_") + "_"
        prefix += pathlib.Path(dir).stem.upper().replace("-", "_")
        prefix += "_"

    return prefix


def write_versions(file, dir, parent_repos, dependencies_filename, version_generator, recursive):
    print_header(dir, parent_repos)

    # got to dir
    if not os.path.exists(dir):
        print(f"[{bformat.ERRORMARK}] needs to be fetched")
        return

    os.chdir(dir)

    # get git infos
    git_infos = GitInfos()

    # set prefix
    prefix = get_prefix(dir, parent_repos)

    # write version
    file.write(version_generator.generate_line(f"{prefix}GIT_REPO", git_infos.repo))
    file.write(version_generator.generate_line(f"{prefix}GIT_HASH", git_infos.hash))
    file.write(version_generator.generate_line(f"{prefix}GIT_SHORT_HASH", git_infos.short_hash))
    file.write(version_generator.generate_line(f"{prefix}GIT_TAG", git_infos.tag))
    file.write(version_generator.generate_line(f"{prefix}GIT_LOCAL_CHANGES", git_infos.local_changes))

    print(f"[{bformat.SUCCESSMARK}] version generated")

    # handle recursivity
    if recursive:
        # generate subrepo list
        dependencies_file = os.path.join(dir, dependencies_filename)

        if not os.path.exists(dependencies_file):
            print(f"{bformat.CYAN}no nested dependencies found here{bformat.DEFAULT}")
            return

        json_data = read_json(dependencies_file)
        subrepo_list = parse_subrepo_data(json_data)

        if not parent_repos:
            parent_repos = []
        parent_repos.append(git_infos.repo)

        for subrepo in subrepo_list:
            write_versions(file, os.path.realpath(os.path.join(dir, subrepo.local_path, subrepo.repo_name)), parent_repos, dependencies_filename, version_generator, recursive)


def generate_version_file(base_dir, dependencies_filename, version_generator, recursive):
    os.chdir(base_dir)

    with open(version_generator.FILENAME, "w") as file:
        # append header
        file.write(version_generator.HEADER)

        # append project and subrepo versions
        write_versions(file, base_dir, None, dependencies_filename, version_generator, recursive)

        # append footer
        file.write(version_generator.FOOTER)
