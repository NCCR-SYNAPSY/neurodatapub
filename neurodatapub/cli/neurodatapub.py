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
from neurodatapub.info import __version__
from neurodatapub.parser import get_parser
from neurodatapub.project import NeuroDataPubProject


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

    # Create a NeuroDataPubProject
    neurodatapub_project = NeuroDataPubProject(
        bids_dir=args['bids_dir'],
        datalad_dataset_dir=args['output_datalad_dir'],
        git_annex_special_sibling_config=args['git-annex-ssh-special-sibling-config'],
        github_sibling_config=args['github-sibling-config']
    )

    # Execute the command
    try:
        exit_code = 0
    except Exception as e:
        exit_code = 1

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
