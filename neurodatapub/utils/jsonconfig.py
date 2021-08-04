# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.jsonconfig`: utils functions to handle JSON sibling configuration files."""

import json
import jsonschema
from jsonschema import validate

# Describe the kind of json we expect for the configuration
# of the git-annex special remote and github siblings
SPECIAL_REMOTE_SIBLING_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "remote_ssh_login": {
            "type": "string",
            "pattern": "^[A-Za-z0-9]+"
        },
        "remote_ssh_url": {
            "type": "string",
            "pattern": "^ssh?://+"
        },
        "remote_sibling_dir": {
            "type": "string",
            "pattern": "/.git$"
        },

    },
    "required": ["remote_ssh_login", "remote_ssh_url", "remote_sibling_dir"]
}

GITHUB_SIBLING_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "github_login": {
            "type": "string",
            "pattern": "[A-Za-z0-9]+"
        },
        "github_repo_name": {
            "type": "string",
            "pattern": "[A-Za-z0-9]+"
        },
    },
    "required": ["github_login", "github_repo_name"]
}


def validate_json_sibling_config(json_file, sibling_type=None):
    """
    Validate a JSON sibling configuration file.

    Parameters
    ----------
    json_file : str
        Absolute path to JSON sibling configuration file

    sibling_type : ['git-annex-special-sibling','github-sibling']
        Type of sibling configuration file
    """
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    try:
        if sibling_type == 'git-annex-special-sibling':
            validate(instance=json_dict, schema=SPECIAL_REMOTE_SIBLING_CONFIG_SCHEMA)
        elif sibling_type == 'github-sibling':
            validate(instance=json_dict, schema=GITHUB_SIBLING_CONFIG_SCHEMA)
        else:
            return False
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True
