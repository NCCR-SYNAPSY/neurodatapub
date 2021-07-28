#!/usr/bin/env python
#
# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""This module defines the entrypoint script of the commandline interface of `neurodatapub`."""

# General imports
import os
import sys

from bids import BIDSLayout

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

    #####################
    # Input sanity check
    #####################

    # 1. Check if the BIDS directory exists
    if not os.path.exists(args.bids_dir):
        print(
            f"The provided BIDS directory ({args.bids_dir}) does not exists"
        )
        exit_code = 1
        return exit_code
    # 2. Check if the BIDS dataset is successfully loaded by pybids
    try:
        layout = BIDSLayout(args.bids_dir)
        print(f'PyBIDS summary of input dataset:\n{layout}')
    except Exception as e:
        print(f'{e}')
        exit_code = 1
        return exit_code

    # 3. Validate sibling configuration files if given
    #    Exit if the json schema of the file is invalid
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

    ############################
    # Execution of the two modes
    ############################

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

        if args.mode == "create-only" or args.mode == "all":
            print(
                "######################################\n"
                "# Creation of Datalad Dataset\n"
                "######################################\n"
            )
            res = neurodatapub_project.create_datalad_dataset()
        if args.mode == "publish-only" or args.mode == "all":
            print(
                "######################################\n"
                "# Publication of Datalad Dataset\n"
                "######################################\n"
            )
            neurodatapub_project.configure_siblings()
            neurodatapub_project.publish_datalad_dataset()

        if res:
            exit_code = 0
            print('Success')
        else:
            exit_code = 1
            print('An error occurred during the creation of the Datalad dataset')
    else:
        # GUI mode
        print('GUI')
        exit_code = 0
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
