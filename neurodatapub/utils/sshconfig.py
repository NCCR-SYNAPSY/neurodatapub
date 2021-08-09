# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.sshconfig`: utils function to edit SSH config."""

import os
from pathlib import Path
from datetime import datetime


def update_ssh_config(sshurl, user):
    """
    Add a new entry to the SSH config file (``~/.ssh/config``).

    It sets the default user login to the SSH special remote.

    Parameters
    -----------
    sshurl : str
        SSH URL of the git-annex special remote in the form
        `ssh://server.example.org`

    user : str
        User login for authentication to the git-annex special remote
    """
    # Remove "ssh://" prefix in SSH URL
    sshurl = sshurl.replace('ssh://', '')

    # Path to ssh config file
    ssh_config_path = os.path.join(
        str(Path.home()),
        '.ssh',
        'config'
    )
    print(f'\t* Add new entry in {ssh_config_path}')

    # Save the current content of an existing ssh config file
    content = None
    if os.path.exists(ssh_config_path):
        with open(ssh_config_path, 'r+') as ssh_config:
            content = ssh_config.read()

    # Add the entry if it does not exist in the existing ssh config file
    with open(ssh_config_path, 'w+') as ssh_config:
        if (content and (f'Host {sshurl}' not in content))\
                or content is None:
            hdr = [
                '## Added by NeuroDataPub ',
                f'({datetime.strftime(datetime.now(), "%d. %B %Y %I:%M%p")}) ##\n',

            ]
            lines = [
                f'Host {sshurl} \n',
                f'\tHostName {sshurl} \n',
                f'\tUser {user} \n\n'
            ]
            try:
                ssh_config.writelines(hdr + lines)
                print(f'\t  - Entry:\n\n{"".join(lines)}')
            except Exception as e:
                print(f'\t  - ERROR:\n\n{e}')
        else:
            print(f'\t  - INFO: Entry for `Host {sshurl}` already existing!\n\n')

    # Append the previous content of the existing ssh config file
    if content:
        with open(ssh_config_path, 'a') as ssh_config:
            ssh_config.write(content)
