.. _installation:

************************************
Installation Instructions for Users
************************************


.. _prerequisites:

Prerequisites
==============

Installation of the `NeuroDataPub` has been facilitated through its distribution to the Python Package Index and the use of a `conda` Python 3.8 environment
to install its dependencies, so in order to run `NeuroDataPub`, we would need to install `Miniconda 3` (Instructions in :ref:`manual-install-miniconda3`).

Once `Miniconda 3` is installed, the recommended way to run `NeuroDataPub` is to use the `NeuroDataPub Assistant`. Usage instructions can be found in :ref:`guiusage`.
However, if you are not afraid by the creation of JSON files, or you feel more comfortable with the command-line interface, usage instructions for the `neurodatapub` command-line interface can be found in :ref:`cliusage`.


.. _manual-install-miniconda3:

Installation of Miniconda 3
------------------------------

* Download the installer of `Miniconda 3` corresponding to your 32/64bits MacOSX/Linux/Win system from https://conda.io/miniconda.html.

* Execute the downloaded script to install it.

.. note:: `NeuroDataPub` has been tested only on Ubuntu and MacOSX.


.. _creation-conda-environment:

Creation of `neurodatapub-env` conda environment
-------------------------------------------------

* Download the conda `environment.yml <https://github.com/NCCR-SYNAPSY/neurodatapub/raw/main/conda/environment.yml>`_

* Create the `neurodatapub-env` conda environment:

  .. parsed-literal::

     $ conda env create -f /path/to/downloaded/environment.yml

  This will create a Python 3.8 environment with all dependencies installed.


Installation of `NeuroDataPub`
------------------------------

Once the `neurodatapub-env` conda environment, ``NeuroDataPub`` can be installed in the `neurodatapub-env` conda environment via `pip`:

  .. code-block:: console

     $ pip install "git+https://github.com/NCCR-SYNAPSY/neurodatapub.git"

* You are ready to use ``NeuroDataPub``!

Help/Questions
--------------

Code bugs can be reported by creating a new `GitHub Issue <https://github.com/NCCR-SYNAPSY/neurodatapub/issues>`_.