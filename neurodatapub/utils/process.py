# Copyright © 2021 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.process`: utils functions to run command via subprocess."""

import os
import subprocess


def run(command, env=None, cwd=None):
    """
    Function calls to execute a command.
    It runs the command specified as input via ``subprocess.run()``.

    Parameters
    ----------
    command : string
        String containing the command to be executed (required)

    env : os.environ
        Specify a custom os.environ

    cwd : Directory
        Specify a custom current working directory

    Examples
    --------
    >>> cmd = 'ls "/path/to/folder"'
    >>> run(cmd) # doctest: +SKIP

    """

    merged_env = os.environ

    if cwd is None:
        cwd = os.getcwd()

    if env is not None:
        merged_env.update(env)

    # Python >=3.7
    process = subprocess.run(
        command,
        shell=True,
        env=merged_env,
        cwd=cwd,
        capture_output=True,
        check=True
    )

    return process
