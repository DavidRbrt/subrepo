import argparse
import os
import pathlib

# project imports
from fetch import fetch_all
from version_generators import get_version_generator
from generate_version import generate_version_file


DEFAULT_DEPENDENCIES_FILENAME = "dependencies.json"


def command_line_parser():
    parser = argparse.ArgumentParser(description="subrepo")

    parser.add_argument("-d", "--dependencies-file", help=f"dependencies input file, default={DEFAULT_DEPENDENCIES_FILENAME}", required=False, type=str, default=DEFAULT_DEPENDENCIES_FILENAME)
    parser.add_argument("-u", "--update", help="fetch all subrepos", required=False, default=False, action="store_true")
    parser.add_argument("-g", "--generate-version", help="generate a header version file for target language (available: c, py)", required=False, type=str, default=None)
    parser.add_argument("-r", "--recursive", help="process dependencies too", required=False, default=False, action="store_true")

    args, _ = parser.parse_known_args()

    if not args.update and not args.generate_version:
        parser.print_help()

    return args.dependencies_file, args.update, args.generate_version, args.recursive


def main():
    dependencies_file, update, generate_version, recursive = command_line_parser()

    # compute base directory
    if dependencies_file:
        base_dir = os.path.dirname(pathlib.Path(dependencies_file).resolve())
    else:
        base_dir = os.getcwd()

    # compute dependencies filename
    dependencies_filename = pathlib.Path(dependencies_file).name

    # update
    if update:
        fetch_all(base_dir, base_dir, dependencies_filename, recursive)

    # generate_version
    if generate_version:
        version_generator = get_version_generator(language=generate_version)

        if version_generator == None:
            print(f'ERROR: Language "{generate_version}" is invalid or not handled yet')
        else:
            generate_version_file(base_dir, dependencies_filename, version_generator, recursive)


if __name__ == "__main__":
    main()
