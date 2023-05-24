# Subrepo

## Prerequisites

- install python
- install python packages:
    ```bash
    $ pip install jsonschema
    ```

## Usage

Note that you can run multiple actions in a same command

### Update sub repos

```bash
$ python subrepo.py --update --dependencies-file <file>
```

or

```bash
$ python subrepo.py -u -d <dependencies-file>
```

### Generate version file

This will generate a file directly usable in a project

```bash
$ python subrepo.py --generate-version <language> --dependencies-file <file,optional>
```

or

```bash
$ python subrepo.py -g <language> -j <file,optional>
```
- available languages: c
- without providing dependencies file the version file will only contains base project infos

## Dependencies file format

Example of dependencies file, usually called **dependencies.json**:

```json
{
    "default": {
        "revision": "master",
        "local_path": "whatever-folder"
    },
    "list": [
        {
            "repo_path": "git@github.com:DavidRbrt/awesome-project.git",
            "revision": "v1.0.0",
            "local_path": "."
        },
        {
            "repo_path": "git@github.com:DavidRbrt/even-better-project.git"
        }
    ]
}

```
- revision can be a sha1, a tag or a branch
- local_path can be any path, existing or not

## Tips

You can ease the use of it by creating an alias, in **~/.bashrc**:

```bash
alias subrepo="python ${path_to_this}/subrepo.py"
```
