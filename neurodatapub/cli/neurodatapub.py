#!/usr/bin/env python
#
# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""This module defines the entrypoint script of the commandline interface of `neurodatapub`."""

# General imports
import sys

# Own imports
from neurodatapub.parser import get_parser
from neurodatapub.project import NeuroDataPubProject
from neurodatapub.utils.jsonconfig import validate_json_sibling_config


def main():
    """Main function that creates and executes a NeuroDataPubProject object.

    Returns
    -------
    exit_code : {0, 1}
        An exit code given to `sys.exit()` that can be:

            * '0' in case of successful completion

            * '1' in case of an error
    """
    # Create and parse arguments
    parser = get_parser()
    args = parser.parse_args()

    # Validate sibling configuration files if given
    # Exit if the json schema of the file is invalid
    if args.git_annex_ssh_special_sibling_config:
        if not validate_json_sibling_config(
            json_file=args.git_annex_ssh_special_sibling_config,
            sibling_type='git-annex-special-sibling'
        ):
            exit_code = 1
            return exit_code

    if args.github_sibling_config:
        if not validate_json_sibling_config(
            json_file=args.github_sibling_config,
            sibling_type='github-sibling'
        ):
            exit_code = 1
            return exit_code

    # Commandline mode
    if not args.gui:
        # Create a NeuroDataPubProject
        neurodatapub_project = NeuroDataPubProject(
            bids_dir=args.bids_dir,
            datalad_dataset_dir=args.datalad_dir,
            git_annex_special_sibling_config=args.git_annex_ssh_special_sibling_config,
            github_sibling_config=args.github_sibling_config
        )
        print(neurodatapub_project)
        exit_code = 0
        print('Success')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
