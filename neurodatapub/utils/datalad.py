# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.datalad`: utils functions for Datalad."""

import os
from importlib import reload
import datalad.api

GITHUB_ORGANIZATION='NCCR-SYNAPSY'
DEFAULT_SSH_REMOTE_NAME = 'ssh_remote'
DEFAULT_OSF_REMOTE_NAME = 'osf-storage'
DEFAULT_DATALAD_SSH_SIBLING_NAME = 'datalad_ssh_sibling'


def create_bids_dataset(
    datalad_dataset_dir,
):
    """
    Function that creates the datalad dataset via `datalad.api.create()`.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    Returns
    -------
    res : string
        Output of `datalad.api.create()`
    """
    # Create parent directories if they do not exist
    if not os.path.exists(os.path.dirname(datalad_dataset_dir)):
        os.makedirs(os.path.dirname(datalad_dataset_dir))

    res = datalad.api.create(
        dataset=datalad_dataset_dir,
        cfg_proc=['text2git', 'bids'],
    )
    return res


def create_ssh_sibling(
    datalad_dataset_dir,
    ssh_special_sibling_args,
    datalad_sibling_name=DEFAULT_DATALAD_SSH_SIBLING_NAME
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

    Returns
    -------
    res : string
        Output of `datalad.api.create_sibling()`
    """
    res = datalad.api.create_sibling(
        sshurl=f'{ssh_special_sibling_args["remote_ssh_url"]}:' +
        f'{ssh_special_sibling_args["remote_sibling_dir"]}',
        name=datalad_sibling_name,
        dataset=datalad_dataset_dir,
        existing='skip'
    )
    return res


def create_github_sibling(
    datalad_dataset_dir,
    github_sibling_args,
    gitannex_remote_name=DEFAULT_SSH_REMOTE_NAME
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

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling_github()
    """
    res = datalad.api.create_sibling_github(
        reponame=github_sibling_args["github_repo_name"],
        github_login=github_sibling_args["github_login"],
        github_organization=github_sibling_args["github_organization"],
        publish_depends=gitannex_remote_name,
        private=True,
        dataset=datalad_dataset_dir,
        existing='skip'
    )
    return res


def authenticate_osf(
    osf_token
):
    """
    Function that initialize the authentication to OSF using a personnal OSF TOKEN.

    Parameters
    ----------
    osf_token : string
        Personal OSF access token.
        It can be generated under your user account
        at `osf.io/settings/tokens <https://osf.io/settings/tokens>`_.

    Returns
    -------
    `res` : string
        Output of ` datalad.api.osf_credentials()`
    """
    # Set OSF_TOKEN and reload datalad.api module
    os.environ['OSF_TOKEN'] = osf_token
    reload(datalad.api)
    # OSF credentials
    res = datalad.api.osf_credentials(
        method='token',
        reset=True
    )
    return res


def create_osf_sibling(
    datalad_dataset_dir,
    osf_dataset_title
):
    """
    Function that creates the OSF dataset repository sibling via `datalad.api.create_sibling_osf()` of the `datalad-osf` extension.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    osf_dataset_title : string
        Title of the dataset on OSF

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling_osf()
    """
    # Use the contents of the README file of the BIDS dataset
    # as description of the dataset published to OSF
    readme_file = os.path.join(datalad_dataset_dir, 'README')
    if os.path.exists(readme_file):
        with open(readme_file, encoding='utf-8') as f:
            dataset_description = f.read()
    else:
        dataset_description = None

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
    return res


def publish_dataset(
    datalad_dataset_dir
):
    """
    Function that publishes the dataset repository to GitHub and the annexed files to a SSH special remote.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    Returns
    -------
    `res` : string
        Output of `datalad.api.publish()
    """
    res = datalad.api.push(
        dataset=datalad_dataset_dir,
        to='github'
    )
    return res
