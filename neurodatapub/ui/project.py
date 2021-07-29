# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

# General imports
import os
import json
from traitsui.api import View, Item, Group, HGroup, VGroup
from traits.api import Button

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
    create_only_button = Button('Create dataset')
    publish_only_button = Button('Publish dataset')
    create_and_publish_button = Button('Create and publish dataset')

    traits_view = View(
        VGroup(
            Group(
                VGroup(
                    Item('input_bids_dir'),
                    Item('output_datalad_dataset_dir'),
                    label="Configuration of Directories"
                ),
                HGroup(
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
                # Group option to layout the subgroups as tabs
                layout='tabbed'
            ),
            HGroup(
                Item('create_and_publish_button'),
                Item('create_only_button'),
                Item('publish_only_button'),
            )
        ),
        resizable=True,
        title=f'NeuroDataPub GUI (Version:{__version__})',
        icon=None,
        image=None,
        width=800,
        height=600
    )
