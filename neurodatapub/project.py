# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

import os
import json
from traits.api import (
    HasTraits, File, Directory, Str, Enum,
    List, Password, Bool
)

import datalad.api

from neurodatapub.info import __version__
from neurodatapub.utils.datalad import (
    create_dataset, create_bids_dataset,
    create_ssh_sibling, create_github_sibling,
    authenticate_osf, create_osf_sibling, publish_dataset,
    DEFAULT_SSH_REMOTE_NAME, DEFAULT_OSF_REMOTE_NAME
)
from neurodatapub.utils.gitannex import init_ssh_special_sibling, enable_ssh_special_sibling
from neurodatapub.utils.io import copy_content_to_datalad_dataset
from neurodatapub.utils.sshconfig import update_ssh_config
from neurodatapub.utils.github import authenticate_github_email, authenticate_github_token


class NeuroDataPubProject(HasTraits):

    """Object that represents, manages and executes a NeuroDataPub project.

    Attributes
    ----------
    input_dataset_dir : Directory
        Absolute path of the original BIDS dataset directory

    dataset_is_bids : Bool
        Indicate if the dataset is organized following the
        Brain Imaging Data Structure (BIDS) standard [1]_
        (Default: `True`)

    output_datalad_dataset_dir : Directory
        Absolute path of the datalad dataset to be created

    git_annex_special_sibling_config : File
        Absolute path of the Json file that describes configuration of the
        git-annex special sibling

    sibling_type : `"ssh"` or `"osf"`
        Type of git-annex special sibling
        (It can be a SSH-accessible server (`"ssh"`) or on the cloud to OSF (`"osf"`))

    github_sibling_config : File
        Absolute path of the Json file that describes configuration of the
        github sibling

    github_login : Str
        GitHub account login

    github_email : Str
        Email associated with GitHub account

    github_organization : Str
        Github organization used for publication

    github_token : Password
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

    osf_token : Password
        Personal OSF token for authentication

    osf_dataset_title : Str
        Dataset title published on OSF

    mode : {"publish-only","create-only","all"}
        Mode in which neurodatapub operates:
          * `"create-only"`: Only create the Datalad dataset,
            copy the content and save the state.
          * `"publish-only"`: Only configure the publication siblings
            if they do not exist yet and publish the Datalad dataset.
          * `"all"`: Perform all steps of `"create-only"` followed by
            all steps of `"publish-only"`, from Datalad dataset creation
            to publication.

    generate_script : Bool
        Dry run that generates a bash script called
        `neurodatapub_DD-MM-YYYY_hh:mm:ss.sh` in the
        `code/` folder of the input dataset that records
        all commands for later execution"
        (Default: `False`)

    References
    ----------
    .. [1] https://bids-specification.readthedocs.io/en/stable/
    """

    input_dataset_dir = Directory(
        exists=True,
        desc='the absolute path of the original BIDS dataset directory'
    )
    dataset_is_bids = Bool(
        True,
        desc='if the dataset is organized following the '
             'Brain Imaging Data Structure (BIDS) standard'
    )
    output_datalad_dataset_dir = Directory(
        desc='the absolute path of the datalad dataset to be created'
    )
    git_annex_special_sibling_config = File(
        desc='the absolute path of the Json file that describes '
             'configuration of the git-annex special sibling'
    )
    _types = List(["ssh", "osf"])
    sibling_type = Enum(
        values='_types',
        desc='the type of git-annex special sibling '
             '(It can be a SSH-accessible server (`"ssh"`) '
             'or on the cloud to OSF (`"osf"`))'
    )
    github_sibling_config = File(
        desc='the absolute path of the Json file that describes '
             'configuration of the github sibling'
    )
    github_login = Str(
        desc='the GitHub account login'
    )
    github_email = Str(
        desc='the email associated with GitHub account'
    )
    github_organization = Str(
        desc='the Github organization used for publication'
    )
    github_token = Password(
        desc='the token to authenticate in GitHub'
    )
    github_repo_name = Str(
        desc='the name of the dataset repository published on GitHub'
    )
    remote_ssh_login = Str(
        desc='the user login to the git-annex special sibling'
    )
    remote_ssh_url = Str(
        desc='the SSH URL to the git-annex special sibling '
             'in the form of `ssh://server.example.org`'
    )
    remote_sibling_dir = Directory(
        desc='the remote absolute path of the sibling dataset on '
             'the git-annex special sibling'
    )
    remote_sibling_name = Str(
        desc='the Datalad sibling name of the git-annex special sibling'
    )
    osf_token = Password(
        desc='Personal OSF token for authentication'
    )
    osf_dataset_title = Str(
        desc='the dataset title published on OSF'
    )
    _modes = List(["all", "create-only", "publish-only"])
    mode = Enum(
        values='_modes',
        desc='the mode in which `neurodatapub` operates'
    )
    generate_script = Bool(
        False,
        desc='to not execute the commands but record them in a bash script called '
             '`neurodatapub_DD-MM-YYYY_hh:mm:ss.sh` in the `code/` '
             'folder of the input dataset '
             'for later execution'
    )

    def __init__(
        self,
        dataset_dir=None,
        dataset_is_bids=True,
        datalad_dataset_dir=None,
        git_annex_special_sibling_config=None,
        sibling_type=None,
        github_sibling_config=None,
        mode=None,
        generate_script=False
    ):
        """Constructor of :class:`NeuroDataPubProject` object."""
        HasTraits.__init__(self)

        self.generate_script = generate_script

        if sibling_type is not None:
            self.sibling_type = sibling_type

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

        if dataset_dir is not None:
            self.input_dataset_dir = dataset_dir

        self.dataset_is_bids = dataset_is_bids

        if datalad_dataset_dir is not None:
            self.output_datalad_dataset_dir = datalad_dataset_dir

        if git_annex_special_sibling_config is not None and os.path.exists(git_annex_special_sibling_config):
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
                if 'osf_token' in git_annex_special_sibling_config_dict.keys():
                    self.osf_token = git_annex_special_sibling_config_dict['osf_token']
                if 'osf_dataset_title' in git_annex_special_sibling_config_dict.keys():
                    self.osf_dataset_title = git_annex_special_sibling_config_dict['osf_dataset_title']

        if github_sibling_config is not None and os.path.exists(github_sibling_config):
            self.github_sibling_config = github_sibling_config
            # Opening JSON file for the GitHub sibling
            with open(github_sibling_config, 'r') as f:
                github_sibling_config_dict = json.load(f)
                if 'github_login' in github_sibling_config_dict.keys():
                    self.github_login = github_sibling_config_dict['github_login']
                if 'github_email' in github_sibling_config_dict.keys():
                    self.github_email = github_sibling_config_dict['github_email']
                if 'github_organization' in github_sibling_config_dict.keys():
                    self.github_organization = github_sibling_config_dict['github_organization']
                if 'github_token' in github_sibling_config_dict.keys():
                    self.github_token = github_sibling_config_dict['github_token']
                if 'github_repo_name' in github_sibling_config_dict.keys():
                    self.github_repo_name = github_sibling_config_dict['github_repo_name']

    def __str__(self):
        """Define how a :class:`NeuroDataPubProject` object is rendered in `print()`."""
        nb_char_shown = 10
        encrypted_github_token = '*' * (len(self.github_token) - nb_char_shown) + self.github_token[-nb_char_shown:]
        encrypted_osf_token = '*' * (len(self.osf_token) - nb_char_shown) + self.osf_token[-nb_char_shown:]
        desc = f"""
NeuroDataPubProject object attribute summary:
\tgenerate_script : {self.generate_script}
\tinput_dataset_dir : {self.input_dataset_dir}
\tdataset_is_bids : {self.dataset_is_bids}
\toutput_datalad_dataset_dir : {self.output_datalad_dataset_dir}
\tgit_annex_special_sibling_config : {self.git_annex_special_sibling_config}
\tgithub_sibling_config : {self.github_sibling_config}
\tgithub_email : {self.github_email}
\tgithub_login : {self.github_login}
\tgithub_organization : {self.github_organization}
\tgithub_token : {encrypted_github_token}
\tgithub_repo_name : {self.github_repo_name}"""
        if self.sibling_type == 'ssh':
            desc += f"""
\tremote_ssh_login : {self.remote_ssh_login}
\tremote_ssh_url : {self.remote_ssh_url}
\tremote_sibling_dir : {self.remote_sibling_dir}
\tremote_sibling_name : {self.remote_sibling_name}"""
        elif self.sibling_type == 'osf':
            desc += f"""
\tosf_dataset_title : {self.osf_dataset_title}
\tosf_token : {encrypted_osf_token}"""
        return desc

    def create_datalad_dataset(self):
        """Create the Datalad dataset."""
        # Initialize the command log of the method
        cmd_fun_log = ''
        # Create the datalad dataset only if the directory is empty
        # and so the .datalad folder should not exist
        if not os.path.exists(
            os.path.join(self.output_datalad_dataset_dir, '.datalad')
        ):
            if self.dataset_is_bids:
                msg = f'Initialize the BIDS Datalad dataset {self.output_datalad_dataset_dir}'
                print(f'> {msg}')
                proc, cmd = create_bids_dataset(
                    datalad_dataset_dir=self.output_datalad_dataset_dir,
                    dryrun=self.generate_script
                )
                if proc:
                    print(f'{proc}')
            else:
                msg = f'Initialize the Datalad dataset {self.output_datalad_dataset_dir}'
                print(f'> {msg}')
                proc, cmd = create_dataset(
                    datalad_dataset_dir=self.output_datalad_dataset_dir,
                    dryrun=self.generate_script
                )
                if proc:
                    print(f'{proc}')
            cmd_fun_log += f'# {msg}\n{cmd}\n\n'

            msg = (f'Copy content of {self.input_dataset_dir} to '
                   f'{self.output_datalad_dataset_dir}')
            print(f'> {msg}')
            proc, cmd = copy_content_to_datalad_dataset(
                bids_dir=self.input_dataset_dir,
                datalad_dataset_dir=self.output_datalad_dataset_dir,
                dryrun=self.generate_script
            )
            cmd_fun_log += f'# {msg}\n{cmd}\n\n'

            if proc is not None:
                print(proc.stdout)
            msg = 'Save dataset state...'
            print(f'> {msg}')
            save_msg = (f'Save dataset state after performing the rsync command '
                        f'with neurodatapub {__version__}')
            if not self.generate_script:
                datalad.api.save(
                    dataset=self.output_datalad_dataset_dir,
                    message=save_msg,
                    jobs='auto'
                )
            cmd = f'datalad save -d "{self.output_datalad_dataset_dir}" -m "{save_msg}" -J "auto"'
            cmd_fun_log += f'# {msg}\n{cmd}\n'
        else:
            print(f'> Creation of Datalad dataset {self.output_datalad_dataset_dir} '
                  'skipped as a Datalad dataset is already present!')
        return True, cmd_fun_log

    def configure_ssh_sibling(self):
        """Configure a ssh sibling of the Datalad dataset for publication of annexed files."""
        # Initialize the command log of the method
        cmd_fun_log = ''

        # Update SSH config file to use self.remote_ssh_login
        # by default when connecting to self.remote_ssh_url
        msg = 'Update SSH config with special remote entry'
        print('> {msg}')
        cmd = update_ssh_config(
            sshurl=self.remote_ssh_url,
            user=self.remote_ssh_login,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        # Configuration of git-annex special remote sibling to host annexed files
        git_annex_special_sibling_config_dict = dict(
            {
                "remote_ssh_login": self.remote_ssh_login,
                "remote_ssh_url": self.remote_ssh_url,
                "remote_sibling_dir": self.remote_sibling_dir
            }
        )
        msg = f'Create the ssh remote sibling to {self.remote_ssh_url}'
        print(f'> {msg}')
        proc, cmd = create_ssh_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_args=git_annex_special_sibling_config_dict,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        if proc:
            print(proc)
        msg = 'Make the ssh remote sibling "special git-annex remote"'
        print(f'> {msg}')
        proc, cmd = init_ssh_special_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_args=git_annex_special_sibling_config_dict,
            ssh_special_sibling_name='ssh_remote',
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        if proc is not None:
            print(proc.stdout)
        msg = 'Enable the ssh remote sibling "special git-annex remote"'
        print(f'> {msg}')
        proc, cmd = enable_ssh_special_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            ssh_special_sibling_name='ssh_remote',
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n'
        if proc is not None:
            print(proc.stdout)

        return cmd_fun_log

    def configure_osf_sibling(self):
        """Configure the osf sibling of the Datalad dataset for publication of annexed files."""
        # Initialize the command log of the method
        cmd_fun_log = ''

        # Authentication to OSF
        msg = 'Authentication to OSF...'
        print(f'> {msg}')
        proc, cmd = authenticate_osf(
            osf_token=self.osf_token,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        if proc:
            print(proc)
        # Creation of OSF dataset sibling
        msg = f'Create the {self.osf_dataset_title} OSF sibling'
        print(f'> {msg}')
        proc, cmd = create_osf_sibling(
            dataset_dir=self.input_dataset_dir,
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            osf_dataset_title=self.osf_dataset_title,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n'
        if proc:
            print(proc)

        return cmd_fun_log

    def configure_github_sibling(self):
        """Configure Git and the github sibling of the Datalad dataset for publication of repository (no-annex)."""
        # Initialize the command log of the method
        cmd_fun_log = ''

        # Authentication to GitHub
        msg = 'Set Git user.email associated with GitHub account'
        print(f'> {msg}')
        proc, cmd = authenticate_github_email(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            github_email=self.github_email,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        if proc is not None:
            print(proc.stdout)
        msg = 'Set Git hub.oauthtoken with the associated GitHub token'
        print(f'> {msg}')
        proc, cmd = authenticate_github_token(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            github_token=self.github_token,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n\n'
        if proc is not None:
            print(proc.stdout)

        # Creation of GitHub dataset sibling
        github_sibling_config_dict = dict(
            {
                "github_login": self.github_login,
                "github_organization": self.github_organization,
                "github_repo_name": self.github_repo_name
            }
        )
        msg = f'Create the {self.github_repo_name} github sibling'
        print(f'> {msg}')
        if self.sibling_type == "ssh":
            gitannex_remote_name = DEFAULT_SSH_REMOTE_NAME
        else:
            gitannex_remote_name = DEFAULT_OSF_REMOTE_NAME
        proc, cmd = create_github_sibling(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            github_sibling_args=github_sibling_config_dict,
            gitannex_remote_name=gitannex_remote_name,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n'
        if proc:
            print(proc)

        return cmd_fun_log

    def configure_siblings(self):
        """Configure the siblings of the Datalad dataset for publication."""
        # Initialize the command log of the method
        cmd_fun_log = ''
        # Configuration of the git annex special remote sibling
        if self.sibling_type is None or self.sibling_type == 'ssh':
            cmd_fun_log1 = self.configure_ssh_sibling()
        elif self.sibling_type == 'osf':
            cmd_fun_log1 = self.configure_osf_sibling()
        # Configuration of Github sibling to host dataset repository
        cmd_fun_log2 = self.configure_github_sibling()
        cmd_fun_log += f'{cmd_fun_log1}\n{cmd_fun_log2}'
        return True, cmd_fun_log

    def publish_datalad_dataset(self):
        """Publish the Datalad dataset."""
        # Initialize the command log of the method
        cmd_fun_log = ''
        if self.mode == "publish-only":
            msg = 'Save dataset state ("publish-only" mode)...'
            print(f'> {msg}')
            save_msg = ('Save dataset state before publication '
                        f'with neurodatapub {__version__} ("publish-only" mode)')
            if not self.generate_script:
                datalad.api.save(
                        dataset=self.output_datalad_dataset_dir,
                        message=save_msg,
                        jobs='auto'
                )
            cmd = f'datalad save -d "{self.output_datalad_dataset_dir}" '
            cmd += f'-m "{save_msg}" -J "auto"'
            cmd_fun_log += f'# {msg}\n{cmd}\n\n'

        msg = (f'Publish the dataset repo to {self.github_repo_name} and '
               f'the annexed files to {self.remote_ssh_url}:{self.remote_sibling_dir}')
        print(f'> {msg}')
        proc, cmd = publish_dataset(
            datalad_dataset_dir=self.output_datalad_dataset_dir,
            dryrun=self.generate_script
        )
        cmd_fun_log += f'# {msg}\n{cmd}\n'
        if proc:
            print(str(proc))
        return True, cmd_fun_log
