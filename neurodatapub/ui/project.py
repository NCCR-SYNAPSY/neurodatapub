# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

# General imports
import datetime
import os
import pkg_resources
import json
import re
from bids import BIDSLayout
from traitsui.qt4.extra.qt_view import QtView
from traitsui.api import (
    Item, Group, HGroup, VGroup, spring,
    DirectoryEditor  # FileEditor
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

    """Object that extends a `NeuroDataPubProject` object with a QtView.

    Attributes
    ----------
    check_config : Button
        Button to check the configuration

    create_only_button : Button
        Button to create a dataset (mode: `"create-only"`)

    publish_only_button : Button
        Button to publish a dataset (mode: `"publish-only"`)

    create_and_publish_button : Button
        Button to create and publish a dataset (mode: `"all"`)

    save_special_sibling_config_button : Button
        Button to save the special remote sibling settings
        in a JSON configuration file

    save_github_sibling_config_button = Button
        Button to save the GitHub sibling settings
        in a JSON configuration file

    config_is_valid : Bool
        Boolean that is updated by the `Check Config` button
        (Default: False)

    version : Str(__version__)
        Version of `NeuroDataPub` for the About tab.

    license : Str(__license__)
        License of `NeuroDataPub` for the About tab.

    copyright : Str(__copyright__)
        Copyright of `NeuroDataPub` for the About tab.

    traits_view : QtView
        QtView of the `NeuroDataPub Assistant`
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
                    Item('input_dataset_dir',
                         editor=DirectoryEditor(dialog_style='open'),
                         style_sheet=return_folder_button_style_sheet()),
                    Item('dataset_is_bids'),
                    Item('output_datalad_dataset_dir',
                         editor=DirectoryEditor(dialog_style='save'),
                         style_sheet=return_folder_button_style_sheet()),
                    label="Configuration of Directories"
                ),
                VGroup(
                    VGroup(
                        Item('sibling_type'),
                        HGroup(
                            VGroup(
                                Item('remote_ssh_login', visible_when='sibling_type == "ssh"'),
                                Item('remote_ssh_url', visible_when='sibling_type == "ssh"'),
                                Item('remote_sibling_dir',
                                     editor=DirectoryEditor(dialog_style='open'),
                                     style_sheet=return_folder_button_style_sheet(),
                                     visible_when='sibling_type == "ssh"'),
                                Item('osf_dataset_title', visible_when='sibling_type == "osf"'),
                                Item('osf_token', visible_when='sibling_type == "osf"'),
                            ),
                            VGroup(
                                spring,
                                Item('save_special_sibling_config_button',
                                     style_sheet=return_save_json_button_style_sheet(),
                                     show_label=False),
                                spring,
                            ),
                        ),
                        label="Git-annex special SSH remote sibling"
                    ),
                    VGroup(
                        HGroup(
                            VGroup(
                                Item('github_login'),
                                Item('github_email'),
                                Item('github_organization'),
                                Item('github_token'),
                                Item('github_repo_name')
                            ),
                            VGroup(
                                spring,
                                Item('save_github_sibling_config_button',
                                     style_sheet=return_save_json_button_style_sheet(),
                                     show_label=False),
                                spring,
                            ),
                        ),
                        label="GitHub sibling"
                    ),
                    label="Configuration of Siblings"
                ),
                VGroup(
                    VGroup(
                        Item('version', style='readonly', label='Version'),
                        Item('license', style='readonly', label='License'),
                        spring,
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
                Item('check_config', width=90, show_label=False), spring,
                Item('create_and_publish_button', width=90, enabled_when='config_is_valid', show_label=False), spring,
                Item('create_only_button', width=90, enabled_when='config_is_valid', show_label=False), spring,
                Item('publish_only_button', width=90, enabled_when='config_is_valid', show_label=False),
                Item('generate_script', enabled_when='config_is_valid', label='Generate script only'),
                spring
            )
        ),
        resizable=True,
        title='NeuroDataPub Assistant',
        icon=pkg_resources.resource_filename(
            'neurodatapub',
            "resources/neurodatapub_logo_100x100.png"
        ),
        image=pkg_resources.resource_filename(
            'neurodatapub',
            "resources/neurodatapub_logo_100x100.png"
        ),
        width=1024,
        height=600,
        style_sheet=return_global_style_sheet()
    )

    def _check_config_fired(self):
        """Executed when button check_config is clicked to check if all config parameters are set."""
        self.config_is_valid = True
        print(
            "\n############################################\n"
            "# Check configuration\n"
            "############################################\n"
        )
        if not os.path.exists(self.input_dataset_dir):
            print(
                f"\t* input_dataset_dir ({self.input_dataset_dir}) does not exists"
            )
            self.config_is_valid = False

        if self.dataset_is_bids:
            try:
                layout = BIDSLayout(self.input_dataset_dir)
                print(f'\t* PyBIDS summary:\n\t{layout}')
            except Exception as e:
                print(f'\t* BIDS ERROR: {e}')
                self.config_is_valid = False
            
        print(f'\t* git-annex special remote sibling type: {self.sibling_type}')

        if self.sibling_type == "ssh":
            if not self.remote_ssh_login:
                print('\t* remote_ssh_login: UNDEFINED')
                self.config_is_valid = False
            else:
                print(f'\t* remote_ssh_login: {self.remote_ssh_login}')
    
            if not self.remote_ssh_url:
                print('\t* remote_ssh_url: UNDEFINED')
                self.config_is_valid = False
            else:
                if not bool(re.match("^ssh?://+", self.remote_ssh_url)):
                    print(f'\t* remote_ssh_url ({self.remote_ssh_url}) is '
                          'not valid (expected format: "^ssh?://+")')
                    self.config_is_valid = False
                else:
                    print(f'\t* remote_ssh_url: {self.remote_ssh_url}')
    
            if not self.remote_sibling_dir:
                print('\t* remote_sibling_dir: UNDEFINED')
                self.config_is_valid = False
            else:
                print(f'\t* remote_sibling_dir: {self.remote_sibling_dir}')

        if self.sibling_type == "osf":
            if not self.osf_token:
                print('\t* osf_token: UNDEFINED')
                self.config_is_valid = False
            else:
                masked_token = "*" * (len(self.osf_token) - 6)
                masked_token += f'{self.osf_token[-6:]}'
                print(f'\t* osf_token: {self.osf_token}')
    
            if not self.osf_dataset_title:
                print('\t* osf_dataset_title: UNDEFINED')
                self.config_is_valid = False
            else:
                print(f'\t* osf_dataset_title: {self.osf_dataset_title}')

        if not self.github_login:
            print('\t* github_login: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* github_login: {self.github_login}')

        if not self.github_email:
            print('\t* github_email: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* github_email: {self.github_email}')

        if not self.github_organization:
            print('\t* github_organization: UNDEFINED')
            self.config_is_valid = False
        else:
            print(f'\t* github_organization: {self.github_organization}')

        if not self.github_token:
            print('\t* github_token: UNDEFINED')
            self.config_is_valid = False
        else:
            masked_token = "*" * (len(self.github_token) - 6)
            masked_token += f'{self.github_token[-6:]}'
            print(f'\t* github_token: {masked_token}')

        if not self.github_repo_name:
            print('\t* github_repo_name: UNDEFINED')
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
            "\n############################################\n"
            "# Creation of Datalad Dataset\n"
            "############################################\n"
        )
        # Initialize the script that will log all commands generated
        cmd_log = '#!/bin/sh\n\n'
        _, cmd_fun_log = self.create_datalad_dataset()
        if self.generate_script:
            # Create name of script with time stamp
            now = datetime.datetime.now()
            script_basename = f'neurodatapub_{now.strftime("%d-%m-%Y_%H-%M-%S")}.sh'
            # Create the code folder if it does not exist
            if not os.path.exists(os.path.join(self.input_dataset_dir, 'code')):
                os.makedirs(os.path.join(self.input_dataset_dir, 'code'), exist_ok=True)
            script_path = os.path.join(self.input_dataset_dir, 'code', script_basename)
            print(
                "\n############################################\n"
                f"# Generation of script {script_path}\n"
                "############################################\n"
            )
            cmd_log += f'{cmd_fun_log}\n'
            with open(script_path, 'w') as f:
                f.writelines(cmd_log)

    def _publish_only_button_fired(self):
        """Executed when `publish_only_button` is clicked."""
        # Initialize the script that will log all commands generated
        cmd_log = '#!/bin/sh\n\n'
        print(
            "\n############################################\n"
            "# Configuration of the publication siblings\n"
            "############################################\n"
        )
        _, cmd_fun_log = self.configure_siblings()
        cmd_log += f'{cmd_fun_log}\n'
        print(
            "\n############################################\n"
            "# Publication of Datalad Dataset\n"
            "############################################\n"
        )
        _, cmd_fun_log = self.publish_datalad_dataset()
        cmd_log += f'{cmd_fun_log}'
        if self.generate_script:
            # Create name of script with time stamp
            now = datetime.datetime.now()
            script_basename = f'neurodatapub_{now.strftime("%d-%m-%Y_%H-%M-%S")}.sh'
            # Create the code folder if it does not exist
            if not os.path.exists(os.path.join(self.input_dataset_dir, 'code')):
                os.makedirs(os.path.join(self.input_dataset_dir, 'code'), exist_ok=True)
            script_path = os.path.join(self.input_dataset_dir, 'code', script_basename)
            print(
                "\n############################################\n"
                f"# Generation of script {script_path}\n"
                "############################################\n"
            )
            with open(script_path, 'w') as f:
                f.writelines(cmd_log)

    def _create_and_publish_button_fired(self):
        """Executed when `create_and_publish_button` is clicked."""
        # Initialize the script that will log all commands generated
        cmd_log = '#!/bin/sh\n\n'
        print(
            "\n############################################\n"
            "# Creation of Datalad Dataset\n"
            "############################################\n"
        )
        _, cmd_fun_log = self.create_datalad_dataset()
        cmd_log += f'{cmd_fun_log}\n'
        print(
            "\n############################################\n"
            "# Configuration of the publication siblings\n"
            "############################################\n"
        )
        _, cmd_fun_log = self.configure_siblings()
        cmd_log += f'{cmd_fun_log}\n'
        print(
            "\n############################################\n"
            "# Publication of Datalad Dataset\n"
            "############################################\n"
        )
        _, cmd_fun_log = self.publish_datalad_dataset()
        cmd_log += f'{cmd_fun_log}'
        if self.generate_script:
            # Create name of script with time stamp
            now = datetime.datetime.now()
            script_basename = f'neurodatapub_{now.strftime("%d-%m-%Y_%H-%M-%S")}.sh'
            # Create the code folder if it does not exist
            if not os.path.exists(os.path.join(self.input_dataset_dir, 'code')):
                os.makedirs(os.path.join(self.input_dataset_dir, 'code'), exist_ok=True)
            script_path = os.path.join(self.input_dataset_dir, 'code', script_basename)
            print(
                "\n############################################\n"
                f"# Generation of script {script_path}\n"
                "############################################\n"
            )
            with open(script_path, 'w') as f:
                f.writelines(cmd_log)

    def _save_special_sibling_config_button_fired(self):
        """Executed when `save_special_sibling_config_button` is clicked."""
        print(
            "\n############################################\n"
            "# Save special remote sibling configuration\n"
            "############################################\n"
        )
        if self.git_annex_special_sibling_config:
            dlg = FileDialog(
                action='save as',
                style='modal',
                default_filename=self.git_annex_special_sibling_config,
                title='Save special remote sibling configuration as...'
            )
        else:
            dlg = FileDialog(
                action='save as',
                style='modal',
                default_directory=self.input_dataset_dir,
                title='Save special remote sibling configuration as...'
            )
        if dlg.open() == OK:
            self.git_annex_special_sibling_config = dlg.path
            # Save configuration of git-annex special remote sibling
            # to host annexed files.
            # Make sure that leading and trailing whitespaces are removed.
            if self.sibling_type == 'ssh':
                git_annex_special_sibling_config_dict = dict(
                    {
                        "remote_ssh_login": self.remote_ssh_login.strip(),
                        "remote_ssh_url": self.remote_ssh_url.strip(),
                        "remote_sibling_dir": self.remote_sibling_dir.strip()
                    }
                )
            else:
                git_annex_special_sibling_config_dict = dict(
                    {
                        "osf_token": self.osf_token.strip(),
                        "osf_dataset_title": self.osf_dataset_title.strip()
                    }
                )
            with open(self.git_annex_special_sibling_config, 'w+') as outfile:
                json.dump(git_annex_special_sibling_config_dict, outfile, indent=4)
            print(f'> Saved as {self.git_annex_special_sibling_config}')
        else:
            print('> Operation was cancelled!')
        print(
            "\n############################################\n"
        )

    def _save_github_sibling_config_button_fired(self):
        """Executed when `save_github_sibling_config_button` is clicked."""
        print(
            "\n############################################\n"
            "# Save GitHub sibling configuration\n"
            "############################################\n"
        )
        if self.github_sibling_config:
            dlg = FileDialog(
                action='save as',
                style='modal',
                default_filename=self.github_sibling_config,
                title='Save GitHub sibling configuration as...'
            )
        else:
            dlg = FileDialog(
                action='save as',
                style='modal',
                default_directory=self.input_dataset_dir,
                title='Save GitHub sibling configuration as...'
            )
        if dlg.open() == OK:
            self.github_sibling_config = dlg.path
            # Save configuration of Github sibling to
            # host dataset repository
            github_sibling_config_dict = dict(
                {
                    "github_login": self.github_login.strip(),
                    "github_email": self.github_email.strip(),
                    "github_organization": self.github_organization.strip(),
                    "github_token": self.github_token.strip(),
                    "github_repo_name": self.github_repo_name.strip()
                }
            )
            with open(self.github_sibling_config, 'w+') as outfile:
                json.dump(github_sibling_config_dict, outfile, indent=4)
            print(f'> Saved as {self.github_sibling_config}')
        else:
            print('> Operation was cancelled!')
        print(
            "\n############################################\n"
        )
