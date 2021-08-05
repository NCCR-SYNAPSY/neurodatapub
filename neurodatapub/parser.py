# Copyright © 2021 Connectomics Lab
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
             '``"create-only"`` creates the datalad dataset only, '
             '``"publish-only"`` creates the datalad dataset only, '
             '``"all"`` creates the datalad dataset only, ',
        choices=["all", "create-only", "publish-only"],
        required='--gui' not in " ".join(sys.argv),
        type=str
    )
    p.add_argument(
        "--bids_dir",
        help="The directory with the input dataset "
             "formatted according to the BIDS standard.",
        required='--gui' not in " ".join(sys.argv),
    )
    p.add_argument(
        "--datalad_dir",
        help="The local directory where the Datalad dataset should be.",
        required='--gui' not in " ".join(sys.argv),
    )
    p.add_argument(
        "--git_annex_ssh_special_sibling_config",
        help="Path to a JSON file containing configuration "
             "parameters for the git-annex SSH special remote dataset sibling",
        required='--gui' not in " ".join(sys.argv),
        type=str
    )
    p.add_argument(
        "--github_sibling_config",
        help="Path to a JSON file containing configuration "
             "parameters for the GitHub dataset repository sibling",
        required='--gui' not in " ".join(sys.argv),
        type=str
    )
    p.add_argument(
        "--gui",
        help="Run NeuroDataPub in GUI mode",
        action="store_true",
        default=False,
    )
    p.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"``neurodatapub`` version {__version__} (Released: {__release_date__})",
    )
    return p
