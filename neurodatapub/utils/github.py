# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.github`: utils functions for authentication to Github."""

from .process import run


def authenticate_github_token(
    datalad_dataset_dir,
    github_token,
    dryrun=False
):
    """
    Function that configure Git's `hub.oauthtoken` with the provided token.

    It is used by Datalad/Git for authentication to GitHub [1]_.

    .. [1] `Datalad Handbook "8.3.4 Publish the dataset" <https://handbook.datalad.org/en/latest/basics/101-139-s3.html#publish-the-dataset>`_

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    github_token : string
        GitHub personal access token

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    proc : string
        Output of `subprocess.run()`
    """
    # Create the git config command to add and set hub.oauthtoken
    cmd = 'git config --global --add hub.oauthtoken '
    cmd += f'{github_token}'

    proc = None
    if not dryrun:
        # Execute the git config command in the dataset directory
        try:
            print(f'... cmd: {cmd}')
            proc = run(cmd, cwd=f'{datalad_dataset_dir}')
        except Exception as e:
            print('Failed')
            print(e)
            return None, cmd
    return proc, cmd


def authenticate_github_email(
    datalad_dataset_dir,
    github_email,
    dryrun=False
):
    """
    Function that configure Git's `user.email` with the provided email.

    It is used by GitHub to to associate commits with your GitHub account [2]_.

    .. [2] `GitHub "About commit email addresses" <https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address#about-commit-email-addresses>`_

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    github_email : string
        Email associated to your GitHub account

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    proc : string
        Output of `subprocess.run()`

    cmd : string
        Equivalent output command
    """
    # Create the git config command to set user.email
    cmd = 'git config --global user.email '
    cmd += f'{github_email}'

    proc = None
    if not dryrun:
        # Execute the git config command in the dataset directory
        try:
            print(f'... cmd: {cmd}')
            proc = run(cmd, cwd=f'{datalad_dataset_dir}')
        except Exception as e:
            print('Failed')
            print(e)
            return None, cmd
    return proc, cmd
