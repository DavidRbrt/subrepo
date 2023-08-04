# Subrepo

## Prerequisites

- install python
- install python packages:
    ```bash
    $ pip install jsonschema
    ```

## Usage

Use help to see how to use this

```bash
$ python subrepo.py --help
```

Plase note that:
- you can run multiple actions in a same command
- default dependencies file is **dependencies.json**

### Usage examples 

Update sub repos

```bash
$ python subrepo.py --update --dependencies-file <file>
```

```bash
$ python subrepo.py -u
```

Generate version file

```bash
$ python subrepo.py --generate-version <language> --dependencies-file <file>
```

```bash
$ python subrepo.py -g <language>
```

Update sub repos and nested sub repos then generate c version file

```bash
$ python subrepo.py -r -u -g c
```

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
