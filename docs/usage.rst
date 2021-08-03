.. _cmdusage:

***********************
Commandline Usage
***********************

.. important::
    `NeuroDataPub` takes as principal input the path of your dataset. The input dataset is required to be in *valid BIDS format*. See :ref:`BIDS standard <bids>` for more information about BIDS.

    Before using `NeuroDataPub`, your dataset should be validated with the free, online `BIDS Validator <http://bids-standard.github.io/bids-validator/>`_,
    or its standalone version.


.. _cliparser:

Commandline Arguments
=============================

.. argparse::
        :ref: neurodatapub.parser.get_parser
        :prog: neurodatapub


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
    * ``"remote_ssh_login"`` (mandatory): user login to the remote

    * ``"remote_ssh_url"`` (mandatory): SSH-URL of the remote in the form `"ssh://..."`

    * ``"remote_sibling_dir"`` (mandatory): Remote .git/ directory of the sibling dataset


.. _githubconfig:

GitHub sibling configuration file
----------------------------------------------------

The GitHub sibling configuration file specified by the input flag ``--github_sibling_config`` adopts the following JSON schema::

    {
        "github_login": "GitHubUserName",
        "github_repo_name": "DatasetName"
    }

where:
    * ``"github_login"`` (mandatory): user login to GitHub.

    * ``"github_repo_name"`` (mandatory): Dataset repository name on GitHub

.. note:: You will be asked to enter a token for authentication to create and publish the repository on GitHub. Please see `"Creating a personal access token" Github documentation <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_ for more details on how to get one. Make also sure that the `write:org` and `read:org` options are enabled.


.. _cliusage:

Running `neurodatapub`
=======================

The ``neurodatapub`` command-line interface can be run in
in the `"create-only"`, `"publish-only"`, and `"all"` modes with the ``--mode``
option flag (as described in :ref:`Commandline Arguments <cliparser>`).
For example, an invocation of the interface to create and publish a dataset
(`"all"` mode) would be as follows:

    .. code-block:: console

       $ neurodatapub --mode "all" \
            --bids_dir '/local/path/to/input/bids/dataset' \
            --datalad_dir  '/local/path/to/output/datalad/dataset' \
            --git_annex_ssh_special_sibling_config '/local/path/to/special_annex_sibling_config.json' \
            --github_sibling_config '/local/path/to/github_sibling_config.json'

.. note:: When you use directly the command-line interface, you would need to provide the JSON files with the option flags ``--git_annex_ssh_special_sibling_config`` and ``--github_sibling_config`` to describe the configuration of the special remote and GitHub dataset siblings.


Support, bugs and new feature requests
=======================================

All bugs, concerns and enhancement requests for this software are managed on GitHub and can be submitted at `https://github.com/NCCR-SYNAPSY/neurodatapub/issues <https://github.com/NCCR-SYNAPSY/neurodatapub/issues>`_.
