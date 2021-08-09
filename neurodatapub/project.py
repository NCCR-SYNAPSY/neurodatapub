# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

import os
import json
from traits.api import HasTraits, File, Directory, Str, Enum, List

import datalad.api

from neurodatapub.info import __version__
from neurodatapub.utils.datalad import (
    create_bids_dataset, create_ssh_sibling, create_github_sibling,
    publish_dataset
)
from neurodatapub.utils.gitannex import init_ssh_special_sibling, enable_ssh_special_sibling
from neurodatapub.utils.io import copy_content_to_datalad_dataset
from neurodatapub.utils.sshconfig import update_ssh_config


class NeuroDataPubProject(HasTraits):

    """Object that represents, manages and executes a NeuroDataPub project.

    Attributes
    ----------
    input_bids_dir : Directory
        Absolute path of the original BIDS dataset directory

    output_datalad_dataset_dir : Directory
        Absolute path of the datalad dataset to be created

    git_annex_special_sibling_config : File
        Absolute path of the Json file that describes configuration of the
        git-annex special sibling

    github_sibling_config : File
        Absolute path of the Json file that describes configuration of the
        github sibling

    github_login : Str
        Token to authenticate in GitHub

    github_repo_name : Str
        Name of the dataset repository published on GitHub

    remote_ssh_login : Str
        User login to the git-annex special sibling

    remote_ssh_url : Str
        SSH URL to the git-annex special sibling
        in the form of `ssh://server.example.org`

    remote_sibling_dir : Directory
        Remote absolute path of the sibling dataset on
        the git-annex special sibling

    remote_sibling_name : Str
        Datalad sibling name of the git-annex special sibling

    mode : {"publish-only","create-only","all"}
        Mode in which neurodatapub operates:
          * `"create-only"`: Only create the Datalad dataset,
            copy the content and save the state.
          * `"publish-only"`: Only configure the publication siblings
            if they do not exist yet and publish the Datalad dataset.
          * `"all"`: Perform all steps of `"create-only"` followed by
            all steps of `"publish-only"`, from Datalad dataset creation
            to publication.
    """

    input_bids_dir = Directory(
        exists=True,
        desc='Absolute path of the original BIDS dataset directory'
    )
    output_datalad_dataset_dir = Directory(
        desc='Absolute path of the datalad dataset to be created'
    )
    git_annex_special_sibling_config = File(
        desc='Absolute path of the Json file that describes '
             'configuration of the git-annex special sibling'
    )
    github_sibling_config = File(
        desc='Absolute path of the Json file that describes '
             'configuration of the github sibling'
    )
    github_login = Str(
        desc='User token to authenticate in GitHub'
    )
    github_repo_name = Str(
        desc='Name of the dataset repository published on GitHub'
    )
    remote_ssh_login = Str(
        desc='User login to the git-annex special sibling'
    )
    remote_ssh_url = Str(
        desc='SSH URL to the git-annex special sibling '
             'in the form of `ssh://server.example.org`'
    )
    remote_sibling_dir = Directory(
        desc='Remote absolute path of the sibling dataset on '
             'the git-annex special sibling'
    )
    remote_sibling_name = Str(
        desc='Datalad sibling name of the git-annex special sibling'
    )
    _modes = List(["all", "create-only", "publish-only"])
    mode = Enum(
        values='_modes',
        desc='Mode in which `neurodatapub` operates'
    )

    def __init__(
        self,
        bids_dir,
        datalad_dataset_dir,
        git_annex_special_sibling_config=None,
        github_sibling_config=None,
        mode=None
    ):
        """Constructor of :class:`NeuroDataPubProject` object."""
        HasTraits.__init__(self)

        if mode is not None:
            print(f'mode: {mode}')
            print("".join(mode))
            if "create-only" in mode:
                self.mode = "create-only"
            if "publish-only" in mode:
                self.mode = "publish-only"
            if "create-only" in mode:
                self.mode = "all"
            print(f'self.mode: {self.mode}')

        if bids_dir:
            self.input_bids_dir = bids_dir

        if datalad_dataset_dir:
            self.output_datalad_dataset_dir = datalad_dataset_dir

        if git_annex_special_sibling_config and os.path.exists(git_annex_special_sibling_config):
            self.git_annex_special_sibling_config = git_annex_special_sibling_config
            # Opening JSON file for the special remote sibling
            with open(git_annex_special_sibling_config, 'r') as f:
                git_annex_special_sibling_config_dict = json.load(f)
                if 'remote_ssh_login' in git_annex_special_sibling_config_dict.keys():
                    self.remote_ssh_login = git_annex_special_sibling_config_dict['remote_ssh_login']
                if 'remote_ssh_url' in git_annex_special_sibling_config_dict.keys():
                    self.remote_ssh_url = git_annex_special_sibling_config_dict['remote_ssh_url']
                if 'remote_sibling_dir' in git_annex_special_sibling_config_dict.keys():
                    self.remote_sibling_dir = git_annex_special_sibling_config_dict['remote_sibling_dir']

        if github_sibling_config and os.path.exists(github_sibling_config):
            self.github_sibling_config = github_sibling_config
            # Opening JSON file for the GitHub sibling
            with open(github_sibling_config, 'r') as f:
                github_sibling_config_dict = json.load(f)

            if 'github_login' in github_sibling_config_dict.keys():
                self.github_login = github_sibling_config_dict['github_login']
            if 'github_repo_name' in github_sibling_config_dict.keys():
                self.github_repo_name = github_sibling_config_dict['github_repo_name']

    def __str__(self):
        """Define how a :class:`NeuroDataPubProject` object is rendered in `print()`."""
        desc = f"""
        NeuroDataPubProject object attribute summary:
        \tinput_bids_dir : {self.input_bids_dir}
        \toutput_datalad_dataset_dir : {self.output_datalad_dataset_dir}
        \tgit_annex_special_sibling_config : {self.git_annex_special_sibling_config}
        \tgithub_sibling_config : {self.github_sibling_config}
        \tgithub_login : {self.github_login}
        \tgithub_repo_name : {self.github_repo_name}
        \tremote_ssh_login : {self.remote_ssh_login}
        \tremote_ssh_url : {self.remote_ssh_url}
        \tremote_sibling_dir : {self.remote_sibling_dir}
        \tremote_sibling_name : {self.remote_sibling_name}
        """
        return desc

    def create_datalad_dataset(self):
        """Create the Datalad dataset."""
        # Create the datalad dataset only if the directory is empty
        # and so the .datalad folder should not exist
        if not os.path.exists(
            os.path.join(self.output_datalad_dataset_dir, '.datalad')
        ):
            print(f'> Initialize the Datalad dataset {self.output_datalad_dataset_dir}')
            proc = create_bids_dataset(
                datalad_dataset_dir=self.output_datalad_dataset_dir
            )
            if proc:
                print(f'{proc}')
            print(
                f'> Copy content of {self.input_bids_dir} to '
                f'{self.output_datalad_dataset_dir}'
            )
            proc, cmd = copy_content_to_datalad_dataset(
                bids_dir=self.input_bids_dir,
                datalad_dataset_dir=self.output_datalad_dataset_dir
            )
            if proc is not None:
                print(proc.stdout)
            print('> Save dataset state...')
            datalad.api.save(
                dataset=self.output_datalad_dataset_dir,
                message=f'Save dataset state after performing the command {cmd} '
                        f'with neurodatapub {__version__}',
                jobs='auto'
            )
        else:
            print(f'> Creation of Datalad dataset {self.output_datalad_dataset_dir} '
                  'skipped as a Datalad dataset is already present!')
        return True

    def configure_siblings(self):
        """Configure the siblings of the Datalad dataset for publication."""
        # Update SSH config file to use self.remote_ssh_login
        # by default when connecting to self.remote_ssh_url
        print('> Update SSH config with special remote entry')
        update_ssh_config(
            sshurl=self.remote_ssh_url,
            user=self.remote_ssh_login
        )
        # Configuration of git-annex special remote sibling to host annexed files
        git_annex_special_sibling_config_dict = dict(
            {
                "remote_ssh_login": self.remote_ssh_login,
                "remote_ssh_url": self.remote_ssh_url,
                "remote_sibling_dir": self.remote_sibling_dir
            }
        )
        print(f'> Create the ssh remote sibling to {self.remote_ssh_url}')
        proc = create_ssh_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_args=git_annex_special_sibling_config_dict
        )
        if proc:
            print(proc)
        print('> Make the ssh remote sibling "special git-annex remote"')
        proc, _ = init_ssh_special_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_args=git_annex_special_sibling_config_dict,
            ssh_special_sibling_name='ssh_remote'
        )
        if proc is not None:
            print(proc.stdout)
        print('> Enable the ssh remote sibling "special git-annex remote"')
        proc, cmd = enable_ssh_special_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_name='ssh_remote'
        )
        if proc is not None:
            print(proc.stdout)
        # Configuration of Github sibling to host dataset repository
        github_sibling_config_dict = dict(
            {
                "github_login": self.github_login,
                "github_repo_name": self.github_repo_name
            }
        )
        print(f'> Create the {self.github_repo_name} github sibling')
        proc = create_github_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            github_sibling_args=github_sibling_config_dict
        )
        if proc:
            print(proc)
        return True

    def publish_datalad_dataset(self):
        """Publish the Datalad dataset."""
        if self.mode == "publish-only":
            print('> Save dataset state ("publish-only" mode)...')
            datalad.api.save(
                    dataset=self.output_datalad_dataset_dir,
                    message=f'Save dataset state before publication '
                            f'with neurodatapub {__version__} ("publish-only" mode)',
                    jobs='auto'
            )
        print(f'> Publish the dataset repo to {self.github_repo_name} and '
              f'the annexed files to {self.remote_ssh_url}:{self.remote_sibling_dir}')
        proc = publish_dataset(
            datalad_dataset_dir=self.output_datalad_dataset_dir
        )
        if proc:
            print(str(proc))
        return True
