# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.sshconfig`: utils function to edit SSH config."""


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
        User login for authentification the git-annex special remote

    Returns
    -------
    lines : string
        Entry added to SSH config
    """
    sshurl = sshurl.replace('ssh://', '')

    lines = None
    ssh_config_path = '~/.ssh/config'
    with open(ssh_config_path, 'a') as ssh_config:
        # Add the entry if it does not exist
        if f'Host {sshurl}' not in ssh_config.read():
            lines = [
                f'\nHost {sshurl} \n',
                f'\tHostName {sshurl} \n',
                f'\tUser {user} \n\n'
            ]
            ssh_config.writelines(lines)

    return lines
