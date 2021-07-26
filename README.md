# synapsy-neurodata-publishing-tool

**Suggested name:** *NeuroDataPub*

This tool should facilitate the conversion to a Datalad dataset, the publication of the dataset repository (only metadata) to GitHub and its annexed data on a SSH data server of the institution.

It should take as input:

* Local path of original bids dataset directory

* Local path of output directory for bids dataset managed by Datalad

* Remote SSH data storage server:
  * SSH Username
  * SSH URL
  * Remote path of dataset (if the folder does not exist it is created inside a parent directory which has to be existing)

* Github:
  * Authentification token
  * Repository name
  * (will be created by default using the organization  NCCR-SYNAPSY)

it should follow the following features and design principles:

 **Open**

 * The tool will be made freely available under the open-source Apache 2.0 license.

 **Transparent**

 * All developement and issues discussed and managed on GitHub

 **Easy-to-use**

 * The use of `traits/traitsui` could allow the development of a GUI.

 * Inputs could be given as a configuration json file as input to run the command-line interface or to initiate the GUI.

 **Focus**

 * This tool should give the following limited number of options:
   * Only create the datalad dataset with configure siblings
   * Only publish the datalad dataset (check if the dataset is ready-to-be-published)
   * Both create and publish the datalad dataset

 **Easy-to-install**

 * This tool should be easy to be installed along with the dependencies (`pybids`, `datalad`, `datalad-neuroimaging`, `git-annex`). This could be achieved by:
   * A conda environment that facilitates the installation of the dependencies at a fixed versions
   * Creation of a `setup.py` such that it can be installed with `pip install .`

   Thought, this would not address the installation of git-annex on the remote SSH data storage server.

 **Robust**

 * This tool should be robust to to adverse code changes with continuous integration testing.

## Risk study

* The user wants to "create only" or "create and publish" a non-existing datalad dataset:
  *  BIDS dataset has to be valid
  *  Local path of output directory for bids dataset managed by Datalad has to be non-existing or empty, otherwise an error is raised

* The user wants to "publish only" an existing datalad dataset:
 * status should be checked and an error raised if not up-to-date
 * siblings should be checked and if the siblings are not existing, they are created
