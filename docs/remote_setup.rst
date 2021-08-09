.. _remote_setup:

*********************************
Special remote setup to host data
*********************************

In this section, you will see how to setup your special remote server to store Datalad-managed data.
As one normal user usually does not have root/admin privileges to the server, this prevents her/him to install them via `apt-get`.

In this case, there exist two user-based installation solutions, depending on the accessibility of your remote data server to internet:

1. Internet access: :ref:`remote_setup_conda`
2. No internet access: :ref:`remote_setup_gitannex`


.. _remote_setup_conda:

Installation with Conda
=========================

From `solutions <http://handbook.datalad.org/en/latest/intro/installation.html#linux-machines-with-no-root-access-e-g-hpc-systems>`_ of the DataLad handbook, installation with `Conda` is the most convenient user-based installation but it requires an internet access from the remote data server.

In this situation, with `Conda` or `Miniconda` installed (If not, please check :ref:`manual-install-miniconda3` for instructions), the DataLad package can be installed from the `conda-forge` channel as follows::

    $ conda install -c conda-forge datalad

In general, all software dependencies of DataLad (including git-annex) are automatically installed too.

.. note::This approach has the advantage that dataset could be directly managed with the Datalad command on the remote server.


.. _remote_setup_gitannex:

Installation of standalone `git-annex`
========================================
The remote data server might not be connected to internet for security reasons and so, it would be impossible to install DataLad via `conda` or `pip`. But do not worry! One can still use a Linux standalone distribution of `git-annex`. It consists of the following steps:

1. Download from the official website the Linux standalone for git-annex: `git-annex-standalone-amd64.tar.gz <https://downloads.kitenet.net/git-annex/linux/current/git-annex-standalone-amd64.tar.gz>`_.

2. Create a folder called for instance `Softwares` in your `/home` directory with the `mkdir` command via `ssh`:

    .. code-block:: console

        $ ssh user@stockage.server.ch \
        "mkdir -p /home/user/Softwares"

3. Copy the downloaded archive to the created folder on the remote server. This can be achieved with the `scp` command:

    .. code-block:: console

        $ scp /local/path/to/git-annex-standalone-amd64.tar.gz \
        user@stockage.server.ch:/home/user/Softwares/git-annex-standalone-amd64.tar.gz

4. Extract the content of the archive to a folder `git-annex-standalone` with the `tar` command and remove it via `ssh`:

    .. code-block:: console

        $ ssh <user>@stockage-horus.chuv.ch \
        "tar xzvf /home/<user>/Softwares/git-annex-standalone-amd64.tar.gz -C git-annex-standalone \
        && rm /home/<user>/Softwares/git-annex-standalone-amd64.tar.gz"

5. Connect to the remote data server via `ssh`:

    .. code-block:: console

        $ ssh <user>@stockage-horus.chuv.ch

    and install the binaries and libraries by opening the `.bashrc` with `vim` and adding the following lines to update system `PATH` and `LD_LIBRARY_PATH`:

    .. code-block:: console

        export LD_LIBRARY_PATH="/home/<user>/Softwares/git-annex-standalone/bin:$LD_LIBRARY_PATH"
        export PATH="/home/<user>/Softwares/git-annex-standalone:$PATH"

    .. tip::
        In `vim`, the key `i` goes into edition mode. When you are done, press the key `esc` and then `:wq` to tell vim to save your change (`w`) and quit (`q`).

.. note::
    In this approach, only git-annex is installed on the remote server, it would not be possible to directly manage Datalad datasets with Datalad directly on the server but would require the installation of the dataset on a host machine where Datalad could be installed.
