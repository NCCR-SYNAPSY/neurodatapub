# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""NeuroDataPub utils functions for Datalad."""

import os
import datalad.api

DEFAULT_SSH_REMOTE_NAME = 'ssh_remote'
DEFAULT_DATALAD_SSH_SIBLING_NAME = 'datalad_ssh_sibling'


def create_bids_dataset(
    datalad_dataset_dir,
):
    """Function that creates the datalad dataset via `datalad.api.create()`.

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
    """Function that creates a SSH remote dataset sibling via `datalad.api.create_sibling()`..

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
        f'{ssh_special_sibling_args["remote_sibling_dir"]} ',
        name=datalad_sibling_name,
        dataset=datalad_dataset_dir,
    )
    return res


def create_github_sibling(
    datalad_dataset_dir,
    github_sibling_args,
    ssh_special_remote_name=DEFAULT_SSH_REMOTE_NAME
):
    """Function that creates the GitHub dataset repository siblings via `datalad.api.create_sibling_github()`.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    github_sibling_args : dict
        Dictionary of parsed input argument in the form::

            {
                'github_token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXZHJ9...",
                'github_repo_name': "ds-example",
            }

    ssh_special_remote_name : string
        Name of the special remote sibling created with
        `neurodatapub.utils.gitannex.init_ssh_special_sibling()`

    Returns
    -------
    `res` : string
        Output of `datalad.api.create_sibling_github()
    """
    res = datalad.api.create_sibling_github(
        reponame=github_sibling_args["github_reponame"],
        github_login=github_sibling_args["github_token"],
        github_organization='NCCR-SYNAPSY',
        publish_depends=ssh_special_remote_name,
        private=True,
        dataset=datalad_dataset_dir,
    )
    return res


def publish_dataset(
        datalad_dataset_dir
):
    """Function that publishes the dataset repository to GitHub and the annexed files to a SSH special remote.

    Parameters
    ----------
    datalad_dataset_dir : string
        Local path of Datalad dataset to be published

    Returns
    -------
    `res` : string
        Output of `datalad.api.publish()
    """
    res = datalad.api.publish(
        dataset=datalad_dataset_dir,
        to='github',
        jobs='auto'
    )
    return res
