.. _cmdusage:

***********************
Commandline Usage
***********************

.. important::
    Before using `NeuroDataPub`, the remote data server should provide at least an installation of `git-annex`. Please see :ref:`remote_setup` for instructions.

    Note also that `NeuroDataPub` takes as principal input the path of your dataset that should be compliant to the Brain Imaging Data Structure (BIDS) format
    by default.
    If you are using a dataset in BIDS format, you should always make sure that your dataset is in *valid BIDS format* before using `NeuroDataPub` using
    the free, online `BIDS Validator <http://bids-standard.github.io/bids-validator/>`_, or its standalone version.
    See :ref:`BIDS standard <bids>` for more information about BIDS.
    If it does not make any sense to adopt the BIDS format for your dataset, `NeuroDataPub` can also handle dataset not necessary in the BIDS format,
    since `v0.4`, with the ``--is_not_bids`` option.


.. _cliparser:

Commandline Arguments
=============================

.. argparse::
        :ref: neurodatapub.parser.get_parser
        :prog: neurodatapub


.. _siblingconfig:

Sibling configuration files
=============================


.. _gitannexconfig:

Git-annex special remote sibling configuration file
----------------------------------------------------

The Git-annex special remote sibling configuration file specified by the input flag ``--git_annex_ssh_special_sibling_config`` adopts the following JSON schema::

    {
        "remote_ssh_login": "user",
        "remote_ssh_url": "ssh://neurodatapub.server.org",
        "remote_sibling_dir": "/remote/path/of/dataset/sibling/.git"
    }

where:
    * ``"remote_ssh_login"`` (mandatory): user's login to the remote

    * ``"remote_ssh_url"`` (mandatory): SSH-URL of the remote in the form `"ssh://..."`

    * ``"remote_sibling_dir"`` (mandatory): Remote .git/ directory of the sibling dataset


.. _githubconfig:

GitHub sibling configuration file
----------------------------------------------------

The GitHub sibling configuration file specified by the input flag ``--github_sibling_config`` adopts the following JSON schema::

    {
        "github_login": "GitHubUserName",
        "github_email": "GitHubUserEmail",
        "github_organization": "NCCR-SYNAPSY",
        "github_token": "Personal github authentication token",
        "github_repo_name": "DatasetName"
    }

where:
    * ``"github_login"`` (mandatory): user's login to GitHub.

    * ``"github_email"`` (mandatory): user's email associated with GitHub account.

    * ``"github_organization"`` (mandatory): GitHub organization the GitHub account has access to.

    * ``"github_token"`` (mandatory): user's github authentication token. Please see `"Creating a personal access token" Github documentation <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_ for more details on how to get one. Make also sure that the `write:org` and `read:org` options are enabled.

    * ``"github_repo_name"`` (mandatory): Dataset repository name on GitHub.


.. _osfconfig:

OSF sibling configuration file
----------------------------------------------------

The OSF sibling configuration file specified by the input flag ``--osf_sibling_config`` adopts the following JSON schema::

    {
        "osf_dataset_title": "DatasetName",
        "osf_token": "Personal OSF authentication token",
    }

where:
    * ``"osf_dataset_title"`` (mandatory): Dataset title on OSF.

    * ``"osf_token"`` (mandatory): user's OSF authentication token. To make a Personal Access Token, please go to the relevant `OSF settings page <https://osf.io/settings/tokens/>`_ and create one. If you do not an OSF account yet, you will need to create one a-priori.


.. _cliusage:

Running `neurodatapub`
=======================

The ``neurodatapub`` command-line interface can be run in
in the `"create-only"`, `"publish-only"`, and `"all"` modes with the ``--mode``
option flag (as described in :ref:`Commandline Arguments <cliparser>`).
For example, an invocation of the interface to create and publish a dataset
(`"all"` mode) to a `ssh` sibling would be as follows:

    .. code-block:: console

       $ neurodatapub --mode "all" \
            --dataset_dir '/local/path/to/input/bids/dataset' \
            --datalad_dir  '/local/path/to/output/datalad/dataset' \
            --git_annex_ssh_special_sibling_config '/local/path/to/special_annex_sibling_config.json' \
            --github_sibling_config '/local/path/to/github_sibling_config.json'

.. note:: When you use directly the command-line interface, you would need to provide the JSON files with the option flags ``--github_sibling_config``, and ``--git_annex_ssh_special_sibling_config``, or ``--git_annex_osf_sibling_config`` to describe the configuration of the GitHub and special remote dataset siblings.


Need more control?
=======================

Since `v0.4`, `NeuroDataPub` can be run with the ``--generate_script`` option to give more control to more advanced users familiar with the Linux shell:

    .. code-block:: console

       $ neurodatapub --mode "all" \
            --generate_script \
            --dataset_dir '/local/path/to/input/bids/dataset' \
            --datalad_dir  '/local/path/to/output/datalad/dataset' \
            --git_annex_ssh_special_sibling_config '/local/path/to/special_annex_sibling_config.json' \
            --github_sibling_config '/local/path/to/github_sibling_config.json'

Using this option, `NeuroDataPub` will run in a "dryrun" mode and will only create a Linux shell script, called ``neurodatapub_%d-%m-%Y_%H-%M-%S.sh`` in the `code/` directory of your input dataset, that records all the underlined commands. If it appears that the `code/` folder does not exist yet, it will be automatically created.


Support, bugs and new feature requests
=======================================

All bugs, concerns and enhancement requests for this software are managed on GitHub and can be submitted at `https://github.com/NCCR-SYNAPSY/neurodatapub/issues <https://github.com/NCCR-SYNAPSY/neurodatapub/issues>`_.
