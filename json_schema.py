# Expected schema for subrepos.json
# see https://json-schema.org/learn/getting-started-step-by-step for more information
JSON_SCHEMA = {
    "title": "subrepos.json",
    "type": "object",
    "properties": {
        "default": {
            "type": "object",
            "properties": {
                "revision": {"type": "string"},
                "local_path": {"type": "string"},
            },
        },
        "list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "repo_path": {"type": "string"},
                    "revision": {"type": "string"},
                    "local_path": {"type": "string"},
                },
                "required": [
                    "repo_path",
                ],
            },
            "minItems": 0,
            "uniqueItems": True,
        },
    },
    "required": [
        "list",
    ],
}
