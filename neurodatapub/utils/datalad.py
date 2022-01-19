# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.datalad`: utils functions for Datalad."""

import os
import datalad.api

GITHUB_ORGANIZATION='NCCR-SYNAPSY'
DEFAULT_SSH_REMOTE_NAME = 'ssh_remote'
DEFAULT_OSF_REMOTE_NAME = 'osf-storage'
DEFAULT_DATALAD_SSH_SIBLING_NAME = 'datalad_ssh_sibling'


def create_bids_dataset(
    datalad_dataset_dir,
    dryrun=False
):
    """
    Function that creates the datalad dataset of a BIDS dataset via `datalad.api.create()`.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.create()`

    `cmd` : string
        Equivalent bash command
    """
    # Create parent directories if they do not exist
    if not os.path.exists(os.path.dirname(datalad_dataset_dir)):
        os.makedirs(os.path.dirname(datalad_dataset_dir))

    res = None
    if not dryrun:
        res = datalad.api.create(
            dataset=datalad_dataset_dir,
            cfg_proc=['text2git', 'bids'],
        )
    cmd = f'datalad create -c text2git -c bids "{datalad_dataset_dir}"'
    return res, cmd


def create_dataset(
    datalad_dataset_dir,
    dryrun=False
):
    """
    Function that creates the datalad dataset via `datalad.api.create()`.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.create()`

    `cmd` : string
        Equivalent bash command
    """
    # Create parent directories if they do not exist
    if not os.path.exists(os.path.dirname(datalad_dataset_dir)):
        os.makedirs(os.path.dirname(datalad_dataset_dir))

    res = None
    if not dryrun:
        res = datalad.api.create(
            dataset=datalad_dataset_dir,
            cfg_proc=['text2git'],
        )
    cmd = f'datalad create -c text2git "{datalad_dataset_dir}"'
    return res, cmd


def create_ssh_sibling(
    datalad_dataset_dir,
    ssh_special_sibling_args,
    datalad_sibling_name=DEFAULT_DATALAD_SSH_SIBLING_NAME,
    dryrun=False
):
    """
    Function that creates a SSH remote dataset sibling via `datalad.api.create_sibling()`..

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

    datalad_sibling_name : string
        Name of the remote sibling created by Datalad

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling()`

    `cmd` : string
        Equivalent bash command
    """
    res = None
    if not dryrun:
        res = datalad.api.create_sibling(
            sshurl=f'{ssh_special_sibling_args["remote_ssh_url"]}:' +
            f'{ssh_special_sibling_args["remote_sibling_dir"]}',
            name=datalad_sibling_name,
            dataset=datalad_dataset_dir,
            existing='skip'
        )
    cmd = f'datalad create-sibling -s {datalad_sibling_name} \\\n\t'
    cmd += f'--dataset "{datalad_dataset_dir}" \\\n\t'
    cmd += f'{ssh_special_sibling_args["remote_ssh_url"]}:{ssh_special_sibling_args["remote_sibling_dir"]}'
    return res, cmd


def create_github_sibling(
    datalad_dataset_dir,
    github_sibling_args,
    gitannex_remote_name=DEFAULT_SSH_REMOTE_NAME,
    dryrun=False
):
    """
    Function that creates the GitHub dataset repository siblings via `datalad.api.create_sibling_github()`.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    github_sibling_args : dict
        Dictionary of parsed input argument in the form::

            {
                'github_login': "my-github-login",
                'github_organization': "NCCR-SYNAPSY",
                'github_repo_name': "ds-example",
            }

    gitannex_remote_name : string
        Name of the special remote sibling created with either
        `neurodatapub.utils.gitannex.init_ssh_special_sibling()` or
        with `datalad.api.create_osf_sibling()`.

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling_github()

    `cmd` : string
        Equivalent bash command
    """
    res = None
    if not dryrun:
        res = datalad.api.create_sibling_github(
            reponame=github_sibling_args["github_repo_name"],
            github_login=github_sibling_args["github_login"],
            github_organization=github_sibling_args["github_organization"],
            publish_depends=gitannex_remote_name,
            private=True,
            dataset=datalad_dataset_dir,
            existing='skip'
        )
    cmd = 'datalad create-sibling-github \\\n\t'
    cmd += f'--dataset "{datalad_dataset_dir}" \\\n\t'
    cmd += f'--publish-depends {gitannex_remote_name} \\\n\t'
    cmd += f'--github-login {github_sibling_args["github_login"]} \\\n\t'
    cmd += f'--github-organization {github_sibling_args["github_organization"]} \\\n\t'
    cmd += f'--private {github_sibling_args["github_repo_name"]}'
    return res, cmd


def authenticate_osf(
    osf_token,
    dryrun=False
):
    """
    Function that initialize the authentication to OSF using a personnal OSF TOKEN.

    Parameters
    ----------
    osf_token : string
        Personal OSF access token.
        It can be generated under your user account
        at `osf.io/settings/tokens <https://osf.io/settings/tokens>`_.

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of ` datalad.api.osf_credentials()`

    `cmd` : string
        Equivalent bash command
    """
    # Set OSF_TOKEN and reload datalad.api module
    os.environ['OSF_TOKEN'] = osf_token
    res = None
    if not dryrun:
        # OSF credentials
        res = datalad.api.osf_credentials(
            method='token',
            reset=False
        )
    cmd = f'export OSF_TOKEN="{osf_token}"\n'
    cmd += 'datalad osf-credentials --method token  --reset'
    return res, cmd


def create_osf_sibling(
    dataset_dir,
    datalad_dataset_dir,
    osf_dataset_title,
    dryrun=False
):
    """
    Function that creates the OSF dataset repository sibling via `datalad.api.create_sibling_osf()` of the `datalad-osf` extension.

    Parameters
    ----------
    dataset_dir : string
        Local path to input BIDS dataset

    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    osf_dataset_title : string
        Title of the dataset on OSF

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling_osf()

    `cmd` : string
        Equivalent bash command
    """
    # Use the contents of the README file of the BIDS dataset
    # as description of the dataset published to OSF
    readme_file = os.path.join(dataset_dir, 'README')
    if os.path.exists(readme_file):
        with open(readme_file, encoding='utf-8') as f:
            dataset_description = f.read()
    else:
        dataset_description = None

    res = None
    if not dryrun:
        # Create the OSF sibling.
        # If the sibling is existing, this will be skipped.
        res = datalad.api.create_sibling_osf(
            title=osf_dataset_title,
            name='osf',
            dataset=datalad_dataset_dir,
            mode='annex',
            existing='skip',
            trust_level=None,
            tags='neuroimaging',
            public=False,
            category='data',
            description=dataset_description
        )
    cmd = 'datalad create-sibling-osf \\\n\t'
    cmd += f'--dataset "{datalad_dataset_dir}" \\\n\t'
    cmd += f'--title "{osf_dataset_title}" \\\n\t'
    cmd += '-s osf \\\n\t'
    cmd += '--mode annex \\\n\t'
    cmd += '--existing skip \\\n\t'
    cmd += '--tag neuroimaging \\\n\t'
    cmd += '--category data \\\n\t'
    cmd += f'--description "{dataset_description}"\n\t'
    return res, cmd


def publish_dataset(
    datalad_dataset_dir,
    dryrun=False
):
    """
    Function that publishes the dataset repository to GitHub and the annexed files to a SSH special remote.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    dryrun : bool
        If `True`, only generates the commands and
        do not execute them
        (Default: `False`)

    Returns
    -------
    `res` : string
        Output of `datalad.api.publish()

    `cmd` : string
        Equivalent bash command
    """
    res = None
    if not dryrun:
        res = datalad.api.push(
            dataset=datalad_dataset_dir,
            to='github'
        )
    cmd = f'datalad push --dataset "{datalad_dataset_dir}" --to github'
    return res, cmd
