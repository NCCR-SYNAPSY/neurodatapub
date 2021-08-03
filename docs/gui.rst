.. _guiusage:

*********************************
NeuroDataPub Assistant User Guide
*********************************

Introduction
============

`NeuroDataPub` comes with a Graphical User Interface
aka the `NeuroDataPub Assistant` to support not only
the configuration of the siblings and the generation of the
corresponding JSON configuration files, but also its
execution in the three different modes.

.. figure:: images/mainWindow.png
    :align: center

    Main window of the `NeuroDataPub Assistant`

Start the Graphical User Interface
====================================

In a terminal, activate the `neurodatapub-env` conda environment::

    $ conda activate neurodatapub-env

Please see Section :ref:`creation-conda-environment` for more details its creation.

After activation, the `NeuroDataPub Assistant` can be launched
via the `neurodatapub` command-line interface with the `--gui` option flag:

    .. code-block:: console

       $ neurodatapub --gui \
            (--bids_dir '/local/path/to/input/bids/dataset' \)
            (--datalad_dir  '/local/path/to/output/datalad/dataset' \)
            (--git_annex_ssh_special_sibling_config '/local/path/to/special_annex_sibling_config.json' \)
            (--github_sibling_config '/local/path/to/github_sibling_config.json')

.. note:: When you run  the `neurodatapub` command-line interface with the `--gui` option, it is not required to
          specify the option flags required for a normal run from the commandline interface.
          However, if provided, the parameters will be used to initialize the configuration of the project.

Configure input and outputs directories
=========================================

You can select or reconfigure your input BIDS directory and the directory of the output
Datalad dataset in the first tab of the `NeuroDataPub Assistant`.

.. figure:: images/ioTab.png
    :align: center

    `Configuration of Directories` tab for the setting of the input BIDS and output datalad dataset directories


Configure the siblings
========================

You can configure or reconfigure the settings for the special
git-annex and GitHub remote siblings.

.. figure:: images/siblingsTab.png
    :align: center

    `Configuration of Siblings` tab for settings of the special git-annex and GitHub remote siblings


Special remote sibling settings
--------------------------------

* ``"remote_ssh_login"`` (mandatory): user login to the remote

* ``"remote_ssh_url"`` (mandatory): SSH-URL of the remote in the form `"ssh://..."`

* ``"remote_sibling_dir"`` (mandatory): Remote .git/ directory of the sibling dataset


GitHub sibling settings
------------------------

* ``"github_login"`` (mandatory): user login to GitHub.

* ``"github_repo_name"`` (mandatory): Dataset repository name on GitHub


Check the configuration and execute `NeuroDataPub`
==================================================

Before being able to initiate the processes of creation and/or publication
of the datalad dataset, you will need to make the `NeuroDataPub Assistant`
checking them out by clicking on the `Check config` button.

.. figure:: images/checkTab.png
    :align: center

    `Check config` button for the inspection of the configuration before execution

If the configuration is completely valid, this will enable the
`Create Dataset`, `Publish Dataset` and `Create and Publish Dataset`
buttons.

.. figure:: images/runTab.png
    :align: center

    `Create Dataset`, `Publish Dataset` and `Create and Publish Dataset` buttons
    for the three execution mode of `NeuroDataPub`


Then, you can execute `NeuroDataPub` in one of the three execution modes by clicking on one of the
buttons: `Create Dataset`, `Publish Dataset` and `Create and Publish Dataset`.

.. note:: You can always see the execution progress by checking the standard outputs in the terminal,
    such as the following:

    .. code-block:: console

        $ neurodatapub --gui

        [...]

        ############################################
        # Check configuration
        ############################################

            * PyBIDS summary:
            BIDS Layout: ...localuser/Data/ds-sample | Subjects: 1 | Sessions: 1 | Runs: 0
            * remote_ssh_login: user
            * remote_ssh_url: ssh://stockage.server.ch
            * remote_sibling_dir: /home/user/Data/ds-sample/.git
            * github_login: user
            * github_repo_name: ds-sample

        Configuration is valid!
        ############################################

        ############################################
        # Creation of Datalad Dataset
        ############################################

        > Initialize the Datalad dataset /home/localuser/Data/ds-sample/derivative/neurodatapub-|vrelease|
        [INFO   ] Creating a new annex repo at /home/localuser/Data/ds-sample/derivative/neurodatapub-|vrelease|
        [INFO   ] Running procedure cfg_text2git
        [INFO   ] == Command start (output follows) =====
        [INFO   ] == Command exit (modification check follows) =====
        [INFO   ] Running procedure cfg_bids
        [INFO   ] == Command start (output follows) =====
        [INFO   ] Running procedure cfg_metadatatypes
        [INFO   ] == Command start (output follows) =====
        [INFO   ] == Command exit (modification check follows) =====
        [INFO   ] == Command exit (modification check follows) =====
        Dataset(/home/localuser/Data/ds-sample/derivative/neurodatapub-|vrelease|)

        [...]
