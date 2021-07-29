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
from traitsui.qt4.extra.qt_view import QtView
from traitsui.api import Item, Group, HGroup, VGroup, spring
from traits.api import Button, Str, Bool

# Own imports
from neurodatapub.info import __version__
from neurodatapub.project import NeuroDataPubProject


# global style_sheet
style_sheet = '''
            QLabel {
                font: 12pt "Verdana";
                margin-left: 5px;
                background-color: transparent;
            }
            QPushButton {
                border: 0px solid gray;
                border-radius: 4px;
                background-color: #40E0D0;
                min-width: 20px;
                icon-size: 20px;
                font: 12pt "Verdana";
                font-weight: bold;
                color: #ff0000;
                margin: 10px;
                padding:0px 0px;
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            
            QMainWindow {
                background-color: #dadbde;
            }
            QMainWindow::separator {
                background: #dadbde;
                width: 1px; /* when vertical */
                height: 1px; /* when horizontal */
            }
            QMainWindow::separator:hover {
                background: red;
            }
            QListView::item:selected {
                border: 1px solid #6a6ea9;
            }
            QListView::item:selected:!active {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #ABAFE5, stop: 1 #8588B2);
            }
            QListView::item:selected:active {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #6a6ea9, stop: 1 #888dd9);
            }
            QListView::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #FAFBFE, stop: 1 #DCDEF1);
            }

            '''


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

    config_is_valid = Bool(False)

    version = Str(__version__)

    traits_view = QtView(
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
        height=450,
        style_sheet=style_sheet
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
