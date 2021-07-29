# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

# General imports
import os
import json
import re
from bids import BIDSLayout
from traitsui.api import View, Item, Group, HGroup, VGroup, spring
from traits.api import Button, Str

# Own imports
from neurodatapub.info import __version__
from neurodatapub.project import NeuroDataPubProject


class NeuroDataPubProjectUI(NeuroDataPubProject):
    """Object that extends a `NeuroDataPubProject` object with a graphical component.

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
        Login to authenticate in GitHub

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
    check_config = Button('Check config')
    create_only_button = Button('Create dataset')
    publish_only_button = Button('Publish dataset')
    create_and_publish_button = Button('Create and publish dataset')

    config_is_valid = False

    version = Str(__version__)

    traits_view = View(
        VGroup(
            Group(
                VGroup(
                    Item('input_bids_dir'),
                    Item('output_datalad_dataset_dir'),
                    label="Configuration of Directories"
                ),
                VGroup(
                    VGroup(
                        Item('remote_ssh_login'),
                        Item('remote_ssh_url'),
                        Item('remote_sibling_dir'),
                        Item('git_annex_special_sibling_config'),
                        label="Git-annex special SSH remote sibling"
                    ),
                    VGroup(
                        Item('github_login'),
                        Item('github_repo_name'),
                        Item('github_sibling_config'),
                        label="GitHub sibling"
                    ),
                    label="Configuration of Siblings"
                ),
                VGroup(
                    VGroup(
                        Item('version', style='readonly', label='Version'),
                        label="About NeuroDataPub"
                    ),
                    label="About"
                ),
                # Group option to layout the subgroups as tabs
                layout='tabbed'
            ),
            spring,
            HGroup(
                spring,
                Item('check_config', width=90), spring,
                Item('create_and_publish_button', width=90, enabled_when='config_is_valid'), spring,
                Item('create_only_button', width=90, enabled_when='config_is_valid'), spring,
                Item('publish_only_button', width=90, enabled_when='config_is_valid'),
                spring,
                show_labels=False,
            )
        ),
        resizable=True,
        title=f'NeuroDataPub Assistant',
        icon=None,
        image=None,
        width=800,
        height=450
    )

    def _check_config_fired(self):
        """Executed when button check_config is clicked to check if all config parameters are set."""
        self.config_is_valid = True

        if not os.path.exists(self.input_bids_dir):
            print(
                    f"\tinput_bids_dir ({self.input_bids_dir}) does not exists"
            )
            self.config_is_valid = False

        try:
            layout = BIDSLayout(self.input_bids_dir)
            print(f'\tPyBIDS summary of input dataset:\n{layout}')
        except Exception as e:
            print(f'{e}')
            self.config_is_valid = False

        if not self.remote_ssh_login:
            print(f'\tremote_ssh_login: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\tremote_ssh_login: {self.remote_ssh_login}')

        if not self.remote_ssh_url:
            print(f'\tremote_ssh_url: UNDEFINED')
            self.config_is_valid = False
        else:
            if not bool(re.match("^ssh?://+", self.remote_ssh_url)):
                print(f'\tremote_ssh_url ({self.remote_ssh_url}) is '
                      'not valid (expected format: "^ssh?://+")')
                self.config_is_valid = False
            else:
                print(f'\tremote_ssh_url: {self.remote_ssh_url}')

        if not self.remote_sibling_dir:
            print(f'\tremote_sibling_dir: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\tremote_sibling_dir: {self.remote_sibling_dir}')

        if not self.github_login:
            print(f'\tgithub_login: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\tgithub_login: {self.github_login}')

        if not self.github_repo_name:
            print(f'\tgithub_repo_name: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\tgithub_repo_name: {self.github_repo_name}')
