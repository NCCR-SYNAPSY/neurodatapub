**************
Changes
**************


Version 0.1
--------------

Date: August 05, 2021

Beta release which provides a first working prototype of `NeuroDataPub`.


Features
=============

* Provide a commandline interface (CLI) to create and publish neuroimaging datasets
  to GitHub NCCR-SYNAPSY, with files annexed in a host institution, accessible
  via `ssh`.

* Adopt a `traits/traitsui` model that extends the CLI with a graphical user interface,
  aka the `NeuroDataPub Assistant`, to improve its accessibility by non IT experts.

* Provide a Conda `environment.yml` to support the installation of
  Python with all dependencies.

* Provide a `setup.py` to make installation of the `neurodatapub` package easy with `pip install`.

* Adopt CircleCI for continuous integration testing.
  CircleCI project page: https://app.circleci.com/pipelines/github/NCCR-SYNAPSY/neurodatapub

* Use `Codacy <https://www.codacy.com/>`_ to support code reviews and monitor code quality over time.
  Codacy project page: https://app.codacy.com/gh/NCCR-SYNAPSY/neurodatapub/dashboard


More...
========

For more change details and development discussions, please check:

* `pull request 1 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/1>`_:
  Main PR with the core API.

* `pull request 7 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/7>`_,
  `pull request 16 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/16>`_,
  `pull request 17 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/17>`_,
  `pull request 18 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/18>`_,
  `pull request 19 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/19>`_:
  PRs that adds the read-the-docs documentation source code and images.

* `pull request 8 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/8>`_:
  PR that adds the use of CircleCI for testing the installation and deploying
  the package to PyPI.

* `pull request 9 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/9>`_:
  PR that adopts Codacy, correct code style issues, and update the README.

* `pull request 12 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/12>`_:
  PR that refines the `setup.py` (project status set to BETA) before
  deployment to PyPI .

* `pull request 13 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/13>`_,
  `pull request 21 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/13>`_:
  PRs that refines `changes.rst`. PR#21 updates tool intro in `index.rst` and `README.md`
  before deployment to PyPI.

* `pull request 20 <https://github.com/NCCR-SYNAPSY/neurodatapub/pull/20>`_:
  PR that makes all options not required when executing with ``--gui``.
