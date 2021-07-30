# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

# General imports
import os
import pkg_resources
import json
import re
from bids import BIDSLayout
from traitsui.qt4.extra.qt_view import QtView, View
from traitsui.api import (
    Item, Group, HGroup, VGroup, spring,
    # FileEditor, DirectoryEditor
)
from traits.api import Button, Str, Bool

from pyface.api import FileDialog, OK

# Own imports
from neurodatapub.info import __version__, __license__, __copyright__
from neurodatapub.project import NeuroDataPubProject
from neurodatapub.utils.qt import (
    return_global_style_sheet,
    return_folder_button_style_sheet,
    return_save_json_button_style_sheet
)

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

    save_special_sibling_config_button = Button('')
    save_github_sibling_config_button = Button('')

    config_is_valid = Bool(False)

    version = Str(__version__)
    license = Str(__license__)
    copyright = Str(__copyright__)

    traits_view = QtView(
        VGroup(
            Group(
                VGroup(
                    Item('input_bids_dir',
                         editor=DirectoryEditor(dialog_style='open'),
                         style_sheet=return_folder_button_style_sheet()),
                    Item('output_datalad_dataset_dir',
                         editor=DirectoryEditor(dialog_style='save'),
                         style_sheet=return_folder_button_style_sheet()),
                    label="Configuration of Directories"
                ),
                VGroup(
                    HGroup(
                        VGroup(
                            Item('remote_ssh_login'),
                            Item('remote_ssh_url'),
                            Item('remote_sibling_dir',
                                 editor=DirectoryEditor(dialog_style='open'),
                                 style_sheet=return_folder_button_style_sheet()),
                            # Item('git_annex_special_sibling_config', style_sheet=return_folder_button_style_sheet()),
                            label="Git-annex special SSH remote sibling"
                        ),
                        VGroup(
                            spring,
                            Item('save_special_sibling_config_button',
                                 style_sheet=return_save_json_button_style_sheet(),
                                 show_label=False),
                            spring,
                        ),
                    ),
                    HGroup(
                        VGroup(
                            Item('github_login'),
                            Item('github_repo_name'),
                            # Item('github_sibling_config', style_sheet=return_folder_button_style_sheet()),
                            label="GitHub sibling"
                        ),
                        VGroup(
                            spring,
                            Item('save_github_sibling_config_button',
                                 style_sheet=return_save_json_button_style_sheet(),
                                 show_label=False),
                            spring,
                        ),
                    ),
                    label="Configuration of Siblings"
                ),
                VGroup(
                    VGroup(
                        Item('version', style='readonly', label='Version'),
                        Item('license', style='readonly', label='License'),
                        Item('copyright', style='readonly', show_label=False),
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
        icon=pkg_resources.resource_filename(
            'neurodatapub',
            "resources/neurodatapub_logo_100x100.png"
        ),
        image=pkg_resources.resource_filename(
            'neurodatapub',
            "resources/neurodatapub_logo_100x100.png"
        ),
        width=800,
        height=450,
        style_sheet=return_global_style_sheet()
    )

    def _check_config_fired(self):
        """Executed when button check_config is clicked to check if all config parameters are set."""
        self.config_is_valid = True
        print(
            "############################################\n"
            "# Check configuration\n"
            "############################################\n"
        )
        if not os.path.exists(self.input_bids_dir):
            print(
                f"\t* input_bids_dir ({self.input_bids_dir}) does not exists"
            )
            self.config_is_valid = False

        try:
            layout = BIDSLayout(self.input_bids_dir)
            print(f'\t* PyBIDS summary:\n\t{layout}')
        except Exception as e:
            print(f'\t* BIDS ERROR: {e}')
            self.config_is_valid = False

        if not self.remote_ssh_login:
            print(f'\t* remote_ssh_login: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* remote_ssh_login: {self.remote_ssh_login}')

        if not self.remote_ssh_url:
            print(f'\t* remote_ssh_url: UNDEFINED')
            self.config_is_valid = False
        else:
            if not bool(re.match("^ssh?://+", self.remote_ssh_url)):
                print(f'\t* remote_ssh_url ({self.remote_ssh_url}) is '
                      'not valid (expected format: "^ssh?://+")')
                self.config_is_valid = False
            else:
                print(f'\t* remote_ssh_url: {self.remote_ssh_url}')

        if not self.remote_sibling_dir:
            print(f'\t* remote_sibling_dir: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* remote_sibling_dir: {self.remote_sibling_dir}')

        if not self.github_login:
            print(f'\t* github_login: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* github_login: {self.github_login}')

        if not self.github_repo_name:
            print(f'\t* github_repo_name: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* github_repo_name: {self.github_repo_name}')

        if self.config_is_valid:
            message = "Configuration is valid!"
        else:
            message = 'Sorry to tell you but there is a problem '\
                      + 'with your actual configuration.'
        print(
            f"\n{message}\n"
            "############################################\n"
        )

    def _create_only_button_fired(self):
        """Executed when `create_only_button` is clicked."""
        print(
            "############################################\n"
            "# Creation of Datalad Dataset\n"
            "############################################\n"
        )
        self.create_datalad_dataset()

    def _publish_only_button_fired(self):
        """Executed when `publish_only_button` is clicked."""
        print(
            "############################################\n"
            "# Configuration of the publication siblings\n"
            "############################################\n"
        )
        self.configure_siblings()
        print(
            "############################################\n"
            "# Publication of Datalad Dataset\n"
            "############################################\n"
        )
        self.publish_datalad_dataset()

    def _create_and_publish_button_fired(self):
        """Executed when `create_and_publish_button` is clicked."""
        print(
            "############################################\n"
            "# Creation of Datalad Dataset\n"
            "############################################\n"
        )
        self.create_datalad_dataset()
        print(
            "############################################\n"
            "# Configuration of the publication siblings\n"
            "############################################\n"
        )
        self.configure_siblings()
        print(
            "############################################\n"
            "# Publication of Datalad Dataset\n"
            "############################################\n"
        )
        self.publish_datalad_dataset()

    def _save_special_sibling_config_button_fired(self):
        print(
            "\n############################################\n"
            "# Save special remote sibling configuration\n"
            "############################################\n"
        )
        dlg = FileDialog(action='save as')
        if dlg.open() == OK:
            self.git_annex_special_sibling_config = dlg.path
            print(f'> Saved as {self.git_annex_special_sibling_config}')
        print(
            "\n############################################\n"
        )

    def _save_github_sibling_config_button_fired(self):
        print(
                "\n############################################\n"
                "# Save GitHub sibling configuration\n"
                "############################################\n"
        )
        dlg = FileDialog(action='save as')
        if dlg.open() == OK:
            self.github_sibling_config = dlg.path
            print(f'> Saved as {self.github_sibling_config}')
        print(
            "\n############################################\n"
        )

        save_github_sibling_config_view = View(
            Group(
                Item('github_sibling_config',
                     style='custom',
                     editor=FileEditor(dialog_style='save'),
                     show_label=False),
            ),
            title='Save the configuration of the GitHub sibling '
                  'to a JSON file as...',
            kind='modal',
            resizable=True,
            buttons=['OK', 'Cancel']
        )
        self.configure_traits(view=save_github_sibling_config_view)
