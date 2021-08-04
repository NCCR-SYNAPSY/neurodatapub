# NeuroDataPub

This tool is developed by the [Connectomics
Lab](https://wp.unil.ch/connectomics/) at the University Hospital of
Lausanne (CHUV) for use within the lab and within the [National Centre
of Competence in Research (NCCR) "SYNAPSY – Synaptic Bases of Mental
Diseases" NCCR-SYNAPSY](https://nccr-synapsy.ch/), as well as for
open-source software distribution.

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/NCCR-SYNAPSY/neurodatapub?include_prereleases)
[![CircleCI](https://circleci.com/gh/NCCR-SYNAPSY/neurodatapub/tree/main.svg?style=svg)](https://circleci.com/gh/NCCR-SYNAPSY/neurodatapub/tree/main)
!["Github All Contributors"](https://img.shields.io/github/all-contributors/NCCR-SYNAPSY/neurodatapub)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e10b50b91e0f49b5866e527d3defd5ad)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NCCR-SYNAPSY/neurodatapub&amp;utm_campaign=Badge_Grade)


## Overview

NeuroDataPub is a neuroimaging dataset publishing tool built on top of
Datalad and git-annex, developed for the NCCR-SYNAPSY members to lower
the barriers in adopting Datalad to manage and publish privately or
publicly their dataset repository on GitHub and the annexed files on
their SSH data server.

![](./docs/images/neurodatapub_illustration.png%0A%20:align:%20center%0A%20:width:%20600)

NeuroDataPub comes with its graphical user interface, aka the
NeuroDataPub Assistant, created to facilitate:

*   the configuration of the siblings,
*   the creation of the JSON configuration files, as well as
*   the execution of NeuroDataPub in the three different modes.

NeuroDataPub is a Python 3.8 that can be easily installed with `pip` as follows:

```bash
pip install "git+https://github.com/NCCR-SYNAPSY/neurodatapub.git"
```


## Documentation

*   TO BE UPDATED


## Usage

`NeuroDataPub` has the following commandline arguments:

```output
usage: neurodatapub [-h] --mode {all,create-only,publish-only} --bids_dir
                    BIDS_DIR --datalad_dir DATALAD_DIR
                    --git_annex_ssh_special_sibling_config
                    GIT_ANNEX_SSH_SPECIAL_SIBLING_CONFIG
                    --github_sibling_config GITHUB_SIBLING_CONFIG [--gui] [-v]

Command-line argument parser of NeuroDataPub (v0.1)

optional arguments:
  -h, --help            show this help message and exit
  --mode {all,create-only,publish-only}
                        Mode in which ``neurodatapub`` is run: ``"create-
                        only"`` creates the datalad dataset only, ``"publish-
                        only"`` creates the datalad dataset only, ``"all"``
                        creates the datalad dataset only,
  --bids_dir BIDS_DIR   The directory with the input dataset formatted
                        according to the BIDS standard.
  --datalad_dir DATALAD_DIR
                        The local directory where the Datalad dataset should
                        be.
  --git_annex_ssh_special_sibling_config GIT_ANNEX_SSH_SPECIAL_SIBLING_CONFIG
                        Path to a JSON file containing configuration
                        parameters for the git-annex SSH special remote
                        dataset sibling
  --github_sibling_config GITHUB_SIBLING_CONFIG
                        Path to a JSON file containing configuration
                        parameters for the GitHub dataset repository sibling
  --gui                 Run NeuroDataPub in GUI mode
  -v, --version         show program's version number and exit
```


## Aknowledgment

If your are using NeuroDataPub in your work, please acknowledge this
software and its dependencies:

1.  Tourbier S, Hagmann P., (2021). NCCR-SYNAPSY/neurodatapub: NCCR-SYNAPSY Neuroimaging Dataset Publishing Tool (Version 0.1). Zenodo.

2.  Halchenko et al., (2021). DataLad: distributed system for joint management of code, data, and their relationship. Journal of Open Source Software, 6(63), 3262, https://doi.org/10.21105/joss.03262.


## License information

This software is distributed under the open-source Apache 2.0 license.
See [license](LICENSE) for more details.

All trademarks referenced herein are property of their respective
holders.


## Help/Questions

If you run into any problems or have any code bugs or questions, please
create a new [GitHub Issue](https://github.com/NCCR-SYNAPSY/neurodatapub/issues).


##Funding

Supported by the National Centre of Competence in Research (NCCR)
"SYNAPSY – Synaptic Bases of Mental Diseases" [NCCR-SYNAPSY](https://nccr-synapsy.ch/)
(grant TO BE UPDATED).
