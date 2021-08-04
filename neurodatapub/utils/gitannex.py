# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.gitannex`: utils functions for Git-annex."""

from .datalad import DEFAULT_SSH_REMOTE_NAME
from .process import run


def init_ssh_special_sibling(
    datalad_dataset_dir,
    ssh_special_sibling_args,
    ssh_special_sibling_name=DEFAULT_SSH_REMOTE_NAME
):
    """
    Function that creates and returns the git annex initremote run command.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    ssh_special_sibling_args : dict
        Dictionary of parsed input argument in the form::

            {
                'remote_ssh_login': "bob",
                'remote_ssh_url': "ssh://server.example.org",
                'remote_sibling_dir': "/path/to/remote/sibling/directory/.git"
            }

    ssh_special_sibling_name : string
        Name of the created special remote sibling

    Returns
    -------
    proc : string
        Output of `subprocess.run()`
    """
    # Create the git annex command
    cmd = 'git annex initremote '
    cmd += f'{ssh_special_sibling_name} '
    cmd += 'type=git '
    cmd += f'location={ssh_special_sibling_args["remote_ssh_url"]}'
    cmd += f'{ssh_special_sibling_args["remote_sibling_dir"]} '
    cmd += 'autoenable=true'

    # Execute the git annex initremote command in the dataset directory
    try:
        print(f'... cmd: {cmd}')
        proc = run(cmd, cwd=f'{datalad_dataset_dir}')
        return proc, cmd
    except Exception as e:
        print('Failed')
        print(e)
        return None, cmd


def enable_ssh_special_sibling(
    datalad_dataset_dir,
    ssh_special_sibling_name=DEFAULT_SSH_REMOTE_NAME
):
    """
    Function that enables the git annex  special remote.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    ssh_special_sibling_name : string
        Name of the created special remote sibling

    Returns
    -------
    proc : string
        Output of `subprocess.run()`
    """
    # Create the git annex command
    cmd = 'git annex enableremote '
    cmd += f'{ssh_special_sibling_name}'

    # Execute the git annex enableremote command in the dataset directory
    try:
        print(f'... cmd: {cmd}')
        proc = run(cmd, cwd=f'{datalad_dataset_dir}')
        return proc, cmd
    except Exception as e:
        print('Failed')
        print(e)
        return None, cmd
