#!/usr/bin/env python
#
# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""This module defines the entrypoint script of the commandline interface of `neurodatapub`."""

# General imports
import os
import sys
import datetime

# Configuration of the graphical backend of traitsui
# Note: Should be at the very beginning before any
# import of traits
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt'  # noqa: E402
os.environ['QT_API'] = 'pyqt5'  # noqa: E402

# Suppress QXcbConnection: XCB error
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'  # noqa: E402

from bids import BIDSLayout

# Own imports
from neurodatapub.parser import get_parser
from neurodatapub.project import NeuroDataPubProject
from neurodatapub.ui.project import NeuroDataPubProjectUI
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
    if args.dataset_dir and not os.path.exists(args.dataset_dir):
        print(
            f"The provided input dataset directory ({args.dataset_dir}) does not exists"
        )
        exit_code = 1
        return exit_code
    elif args.dataset_dir and os.path.exists(args.dataset_dir) and not args.is_not_bids:
        # 2. Check if the BIDS dataset is successfully loaded by pybids
        try:
            layout = BIDSLayout(args.dataset_dir)
            print(f'PyBIDS summary of input dataset:\n{layout}')
        except Exception as e:
            print(f'{e}')
            exit_code = 1
            return exit_code

    # 3. Validate sibling configuration files if given
    #    Exit if the json schema of the file is invalid
    if args.github_sibling_config:
        if not validate_json_sibling_config(
            json_file=args.github_sibling_config,
            sibling_type='github-sibling'
        ):
            exit_code = 1
            return exit_code

    if args.git_annex_ssh_special_sibling_config:
        if not validate_json_sibling_config(
            json_file=args.git_annex_ssh_special_sibling_config,
            sibling_type='git-annex-special-sibling'
        ):
            exit_code = 1
            return exit_code

    if args.osf_sibling_config:
        if not validate_json_sibling_config(
            json_file=args.osf_sibling_config,
            sibling_type='osf-sibling'
        ):
            exit_code = 1
            return exit_code

    ############################
    # Execution of the two modes
    ############################

    # Commandline mode
    if not args.gui:

        # Handle the type of sibling for annexing data
        if args.git_annex_ssh_special_sibling_config:
            git_annex_special_sibling_config = args.git_annex_ssh_special_sibling_config
            sibling_type = 'ssh'
        else:
            git_annex_special_sibling_config = args.osf_sibling_config
            sibling_type = 'osf'
        # Create a NeuroDataPubProject
        neurodatapub_project = NeuroDataPubProject(
            dataset_dir=args.dataset_dir,
            dataset_is_bids=not args.is_not_bids,
            datalad_dataset_dir=args.datalad_dir,
            git_annex_special_sibling_config=git_annex_special_sibling_config,
            sibling_type=sibling_type,
            github_sibling_config=args.github_sibling_config,
            mode=args.mode,
            generate_script=args.generate_script
        )
        print(neurodatapub_project)

        # Initialize the script that will log all commands generated
        cmd_log = '#!/bin/sh\n\n'

        if args.mode == "create-only" or args.mode == "all":
            print(
                "\n############################################\n"
                "# Creation of Datalad Dataset\n"
                "############################################\n"
            )
            res, cmd_fun_log = neurodatapub_project.create_datalad_dataset()
            if res:
                exit_code = 0
                print('Success')
                cmd_log += f'{cmd_fun_log}\n'
            else:
                exit_code = 1
                print('An error occurred during the creation of the Datalad dataset')
                return exit_code
        if args.mode == "publish-only" or args.mode == "all":
            print(
                "\n############################################\n"
                "# Configuration of the publication siblings\n"
                "############################################\n"
            )
            res, cmd_fun_log = neurodatapub_project.configure_siblings()
            if not res:
                exit_code = 1
                print('An error occurred during the configuration of the publication siblings')
                return exit_code
            print(
                "\n############################################\n"
                "# Publication of Datalad Dataset\n"
                "############################################\n"
            )
            cmd_log += f'{cmd_fun_log}\n'
            res, cmd_fun_log = neurodatapub_project.publish_datalad_dataset()
            if res:
                exit_code = 0
                print('Success')
                cmd_log += f'{cmd_fun_log}\n'
            else:
                exit_code = 1
                print('An error occurred during the publication of the Datalad dataset')
        if args.generate_script:
            # Create name of script with time stamp
            now = datetime.datetime.now()
            script_basename = f'neurodatapub_{now.strftime("%d-%m-%Y_%H-%M-%S")}.sh'
            # Create the code folder if it does not exist
            if not os.path.exists(os.path.join(args.dataset_dir, 'code')):
                os.makedirs(os.path.join(args.dataset_dir, 'code'), exist_ok=True)
            script_path = os.path.join(args.dataset_dir, 'code', script_basename)
            print(
                "\n############################################\n"
                f"# Generation of script {script_path}\n"
                "############################################\n"
            )
            with open(script_path, 'w') as f:
                f.writelines(cmd_log)

    else:
        # GUI mode
        print(
            "\n*********************************************\n"
            "# Launch NeuroDataPub Assistant\n"
            "*********************************************\n"
        )
        # Handle the type of sibling for annexing data
        if args.git_annex_ssh_special_sibling_config:
            git_annex_special_sibling_config = args.git_annex_ssh_special_sibling_config
            sibling_type = 'ssh'
        elif args.osf_sibling_config:
            git_annex_special_sibling_config = args.osf_sibling_config
            sibling_type = 'osf'
        else:
            git_annex_special_sibling_config = None
            sibling_type = 'ssh'
        # Create a NeuroDataPubProjectUI
        neurodatapub_project_gui = NeuroDataPubProjectUI(
                dataset_dir=args.dataset_dir,
                dataset_is_bids=not args.is_not_bids,
                datalad_dataset_dir=args.datalad_dir,
                git_annex_special_sibling_config=git_annex_special_sibling_config,
                sibling_type=sibling_type,
                github_sibling_config=args.github_sibling_config,
                mode=args.mode,
                generate_script=args.generate_script
        )
        print(neurodatapub_project_gui)

        # Launch the GUI
        neurodatapub_project_gui.configure_traits()
        print('GUI exited!')
        exit_code = 0
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
