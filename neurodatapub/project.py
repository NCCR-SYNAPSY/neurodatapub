# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

import os
import json
from traits.api import File, Directory, Str, HasTraits


class NeuroDataPubProject(HasTraits):
    """Object that represents, manages and executes a NeuroDataPub project.

    Attributes
    ----------
    git_annex_special_sibling_config : File
        Path of Json file that describes configuration of the
        git-annex special sibling

    github_sibling_config : File
        Path of Json file that describes configuration of the
        github sibling

    github_token : Str
        Token to authenticate in GitHub

    github_repo_name : Str
        Name of the dataset repository published on GitHub

    remote_ssh_login : Str
        User login to the git-annex special sibling

    remote_ssh_url : Str
        SSH URL to the git-annex special sibling
        in the form of `ssh://server.example.org`

    remote_sibling_dir : Directory
        Remote path of the sibling dataset on the git-annex special sibling

    remote_sibling_name : Str
        Datalad sibling name of the git-annex special sibling
    """

    input_bids_dir = Directory(exists=True)
    output_datalad_dataset_dir = Directory
    git_annex_special_sibling_config = File
    github_sibling_config = File
    github_token = Str
    github_repo_name = Str
    remote_ssh_login = Str
    remote_ssh_url = Str
    remote_sibling_dir = Directory
    remote_sibling_name = Str

    def __init__(
        self,
        bids_dir,
        datalad_dataset_dir,
        git_annex_special_sibling_config=None,
        github_sibling_config=None
    ):
        """Constructor of :class:`NeuroDataPubProject` object"""
        self.input_bids_dir = bids_dir
        self.output_datalad_dataset_dir = datalad_dataset_dir

        if os.path.exists(git_annex_special_sibling_config):
            # Opening JSON file for the special remote sibling
            with open(git_annex_special_sibling_config, 'r') as f:
                git_annex_special_sibling_config_dict = json.load(f)
                if 'remote_ssh_login' in git_annex_special_sibling_config_dict.keys():
                    self.remote_ssh_login = git_annex_special_sibling_config_dict['remote_ssh_login']
                if 'remote_ssh_url' in git_annex_special_sibling_config_dict.keys():
                    self.remote_ssh_url = git_annex_special_sibling_config_dict['remote_ssh_url']
                if 'remote_sibling_dir' in git_annex_special_sibling_config_dict.keys():
                    self.remote_sibling_dir = git_annex_special_sibling_config_dict['remote_sibling_dir']

        if os.path.exists(github_sibling_config):
            # Opening JSON file for the GitHub sibling
            with open(github_sibling_config, 'r') as f:
                github_sibling_config_dict = json.load(f)

            if 'github_token' in github_sibling_config_dict.keys():
                self.github_token = github_sibling_config_dict['github_token']
            if 'github_repo_name' in github_sibling_config_dict.keys():
                self.github_repo_name = github_sibling_config_dict['github_repo_name']
