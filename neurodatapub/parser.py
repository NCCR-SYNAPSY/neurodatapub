# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""NeuroDataPub Commandline Parser."""

import sys
import argparse
from neurodatapub.info import __version__
from neurodatapub.info import __release_date__


def get_parser():
    """Create and return the parser object of NeuroDataPub."""
    p = argparse.ArgumentParser(
        description=f"Command-line argument parser of `NeuroDataPub` (v{__version__})"
    )

    p.add_argument(
        "--mode",
        help="Mode in which ``neurodatapub`` is run: "
             '``"create-only"`` create the datalad dataset only, '
             '``"publish-only"`` publish the datalad dataset only, '
             '``"all"`` create and publish the datalad dataset.',
        choices=["all", "create-only", "publish-only"],
        required='--gui' not in " ".join(sys.argv),
        type=str
    )
    p.add_argument(
        "--dataset_dir",
        help="The directory with the input dataset "
             "formatted according to the BIDS standard.",
        required='--gui' not in " ".join(sys.argv),
    )
    p.add_argument(
        "--is_not_bids",
        action='store_true',
        help="Specify if the directory with the input dataset "
             "is not formatted according to the BIDS standard."
    )
    p.add_argument(
        "--datalad_dir",
        help="The local directory where the Datalad dataset should be.",
        required='--gui' not in " ".join(sys.argv),
    )
    p.add_argument(
        "--github_sibling_config",
        help="Path to a JSON file containing configuration "
             "parameters for the GitHub dataset repository sibling.",
        required='--gui' not in " ".join(sys.argv),
        type=str
    )
    storage_sibling_config = p.add_mutually_exclusive_group(
        required='--gui' not in " ".join(sys.argv)
    )
    storage_sibling_config.add_argument(
        "--git_annex_ssh_special_sibling_config",
        help="Path to a JSON file containing configuration "
             "parameters for the git-annex SSH special remote dataset sibling.",
        type=str
    )
    storage_sibling_config.add_argument(
        "--osf_sibling_config",
        help="Path to a JSON file containing configuration "
             "parameters for the git-annex OSF special remote dataset sibling.",
        type=str
    )
    p.add_argument(
        "--gui",
        help="Run NeuroDataPub in GUI mode.",
        action="store_true",
        default=False
    )
    p.add_argument(
        "--generate_script",
        help="Dry run that generates a bash script called `neurodatapub_DD-MM-YYYY_hh:mm:ss.sh` "
             "in the `code/` folder of the input dataset that records all commands for later execution.",
        action="store_true",
        default=False
    )
    p.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"``neurodatapub`` version {__version__} (Released: {__release_date__})",
    )
    return p
