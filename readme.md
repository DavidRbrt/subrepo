# Subrepo

## Prerequisites

- install python
- install python packages:
    ```bash
    $ pip install jsonschema
    ```

## Usage

Update sub repos

```bash
$ python subrepo.py --update --jsonfile <subrepo-file>
```

or

```bash
$ python subrepo.py -u -j <subrepo-file>
```

Example of subrepo file (json), usually called **dependencies.json**:

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

You can ease the use of it by creating an alias, in **~/.bashrc**:

```bash
alias subrepo="python ${path_to_this}/subrepo.py"
```
