# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""NeuroDataPub Commandline Parser."""

from neurodatapub.info import __version__
from neurodatapub.info import __release_date__


def get_parser():
    """Create and return the parser object of NeuroDataPub."""

    import argparse

    p = argparse.ArgumentParser(description="Argument parser of NeuroDataPub")

    p.add_argument("--bids_dir", help="The directory with the input dataset "
                                      "formatted according to the BIDS standard.")

    p.add_argument(
        "--output_datalad_dir",
        help="The local directory where the output Datalad "
        "dataset should be stored.",
    )

    p.add_argument(
        "--git-annex-ssh-special-sibling-config",
        help="Path to a JSON file containing configuration "
             "parameters for the git-annex SSH special remote dataset sibling",
        default=None,
        type=str,
    )

    p.add_argument(
            "--github-sibling-config",
            help="Path to a JSON file containing configuration "
                 "parameters for the GitHub dataset repository sibling",
            default=None,
            type=str,
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
        version=f"NeuroDataPub version {__version__} (Released: {__release_date__})",
    )
    return p
