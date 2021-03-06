# NeuroDataPub: NCCR-SYNAPSY Neuroimaging Dataset Publishing Tool

This tool is developed by the [Connectomics
Lab](https://wp.unil.ch/connectomics/) at the University Hospital of
Lausanne (CHUV) for use within the lab and within the [National Centre
of Competence in Research (NCCR) "SYNAPSY – Synaptic Bases of Mental
Diseases" NCCR-SYNAPSY](https://nccr-synapsy.ch/), as well as for
open-source software distribution.

[![PyPI](https://img.shields.io/pypi/v/neurodatapub)](https://pypi.org/project/neurodatapub/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5163950.svg)](https://doi.org/10.5281/zenodo.5163950)
[![Documentation Status](https://readthedocs.org/projects/neurodatapub/badge/?version=latest)](https://neurodatapub.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/NCCR-SYNAPSY/neurodatapub/tree/main.svg?style=shield)](https://circleci.com/gh/NCCR-SYNAPSY/neurodatapub/tree/main)
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e10b50b91e0f49b5866e527d3defd5ad)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NCCR-SYNAPSY/neurodatapub&amp;utm_campaign=Badge_Grade)

## Overview

`NeuroDataPub` is an open-source neuroimaging dataset publishing tool written in Python and built on top of
Datalad and git-annex. It aims to lower the barriers, for the NCCR-SYNAPSY members,
to manage and publish, privately or publicly, their dataset repositories on GitHub and the annexed files on
their SSH data server, in order to fully fulfill the implemented Neuroimaging Data Management Plan.

Since ``v0.3``, you can use either (1) a server accessible via `ssh` or (2) the Open Science Foundation (OSF)
platform, as a git-annex special remote, to host your annexed files.

Since `v0.4`, `NeuroDataPub` can handle datasets that do and do not follow the
  [Brain Imaging Data Structure](https://bids-specification.readthedocs.io) standard.

![](https://github.com/NCCR-SYNAPSY/neurodatapub/raw/main/docs/images/neurodatapub_illustration.png)

`NeuroDataPub` comes with its graphical user interface, aka the `NeuroDataPub Assistant`,
created to facilitate:

*   the configuration of the siblings,

*   the creation of the JSON configuration files, as well as

*   the execution of NeuroDataPub in three different modes:
    1.  creation and publication of a datalad dataset,
    2.  creation of a datalad dataset only,
    3.  publication of an existing datalad dataset only,

*   the creation of a Linux shell script for later execution where all commands are recorded.

`NeuroDataPub` is a Python 3.8 package that can be easily installed with `pip` as follows:

```bash
pip install neurodatapub
```

## Documentation

*   https://neurodatapub.readthedocs.io/

## Usage

`NeuroDataPub` has the following commandline arguments:

```output
usage: neurodatapub [-h] --mode {all,create-only,publish-only}
                    --dataset_dir DATASET_DIR [--is_not_bids]
                    --datalad_dir DATALAD_DIR
                    --github_sibling_config GITHUB_SIBLING_CONFIG
                    (--git_annex_ssh_special_sibling_config GIT_ANNEX_SSH_SPECIAL_SIBLING_CONFIG | --osf_sibling_config OSF_SIBLING_CONFIG)
                    [--gui] [--generate_script] [-v]

Command-line argument parser of `NeuroDataPub` (v0.4)

optional arguments:
  -h, --help            show this help message and exit.
  --mode {all,create-only,publish-only}
                        Mode in which ``neurodatapub`` is run: ``"create-only"`` create
                        the datalad dataset only, ``"publish-only"`` publish the datalad
                        dataset only, ``"all"` create and publish the datalad dataset.
  --dataset_dir DATASET_DIR
                        The directory with the input dataset formatted according
                        to the BIDS standard. Specify if the directory with the input
                        dataset is not formatted according to the BIDS standard.
  --is_not_bids         Specify if the directory with the input dataset is not formatted
                        according to the BIDS standard.
  --datalad_dir DATALAD_DIR
                        The local directory where the Datalad dataset should be.
  --github_sibling_config GITHUB_SIBLING_CONFIG
                        Path to a JSON file containing configuration parameters for
                        the GitHub dataset repository sibling.
  --git_annex_ssh_special_sibling_config GIT_ANNEX_SSH_SPECIAL_SIBLING_CONFIG
                        Path to a JSON file containing configuration parameters for
                        the git-annex SSH special remote dataset sibling.
  --osf_sibling_config OSF_SIBLING_CONFIG
                        Path to a JSON file containing configuration parameters for
                        the git-annex OSF special remote dataset sibling.
  --gui                 Run NeuroDataPub in GUI mode.
  --generate_script     Dry run that generates a bash script called
                        `neurodatapub_DD-MM-YYYY_hh:mm:ss.sh` in the `code/` folder
                        of the input dataset that records all commands for later execution.
  -v, --version         show program's version number and exit.

```

## Acknowledgment

If your are using `NeuroDataPub` in your work, please acknowledge this
software and its dependencies:

*   Tourbier S, Hagmann P., (2021). NCCR-SYNAPSY/neurodatapub: NCCR-SYNAPSY Neuroimaging Dataset Publishing Tool (Version 0.1). Zenodo.

*   Halchenko et al., (2021). DataLad: distributed system for joint management of code, data, and their relationship. Journal of Open Source Software, 6(63), 3262, https://doi.org/10.21105/joss.03262.

## License information

This software is distributed under the open-source Apache 2.0 license.
See [license](LICENSE) for more details.

All trademarks referenced herein are property of their respective
holders.

## Help/Questions

If you run into any problems or have any code bugs or questions, please
create a new [GitHub Issue](https://github.com/NCCR-SYNAPSY/neurodatapub/issues).

## Funding

Supported by the National Centre of Competence in Research (NCCR)
"SYNAPSY – Synaptic Bases of Mental Diseases"
([NCCR-SYNAPSY website](https://nccr-synapsy.ch/) / [NCCR-SYNAPSY Swiss National Science Foundation page](https://www.snf.ch/en/rk1dIQvOuOCU9G4Z/page/researchinFocus/nccr/nccr-synapsy)) supported by [SNF-185897 grant](https://p3.snf.ch/project-185897).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/sebastientourbier"><img src="https://avatars.githubusercontent.com/u/22279770?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sébastien Tourbier</b></sub></a><br /><a href="https://github.com/NCCR-SYNAPSY/neurodatapub/commits?author=sebastientourbier" title="Code">💻</a> <a href="https://github.com/NCCR-SYNAPSY/neurodatapub/commits?author=sebastientourbier" title="Documentation">📖</a> <a href="#design-sebastientourbier" title="Design">🎨</a> <a href="#ideas-sebastientourbier" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-sebastientourbier" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-sebastientourbier" title="Maintenance">🚧</a> <a href="#mentoring-sebastientourbier" title="Mentoring">🧑‍🏫</a> <a href="#projectManagement-sebastientourbier" title="Project Management">📆</a> <a href="#question-sebastientourbier" title="Answering Questions">💬</a> <a href="https://github.com/NCCR-SYNAPSY/neurodatapub/pulls?q=is%3Apr+reviewed-by%3Asebastientourbier" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://wp.unil.ch/connectomics"><img src="https://avatars.githubusercontent.com/u/411192?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Patric Hagmann</b></sub></a><br /><a href="#fundingFinding-pahagman" title="Funding Finding">🔍</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
