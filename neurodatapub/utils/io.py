# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.io`: utils functions for input/output."""

from .process import run


def copy_content_to_datalad_dataset(
    bids_dir,
    datalad_dataset_dir,
):
    """
    Copy BIDS dataset content to target datalad dataset directory using `rsync`.

    Parameters
    -------
    bids_dir : string
        Local path of the BIDS dataset

    datalad_dataset_dir : string
        Local path of the directory of the datalad dataset being created

    Returns
    -------
    proc :
        Output of call to `rsync` command via `subprocess.run()`
    """
    # Make sure the path ends with "/" such that rsync
    # copy the content and not the directory itself
    if not bids_dir.endswith('/'):
        bids_dir += '/'

    cmd = 'rsync -vrL '
    cmd += f'{bids_dir} '
    cmd += f'{datalad_dataset_dir}'

    # Execute the rsync command
    try:
        print(f'... cmd: {cmd}')
        proc = run(cmd)
        return proc, cmd
    except Exception as e:
        print('Failed')
        print(e)
        return None, cmd
