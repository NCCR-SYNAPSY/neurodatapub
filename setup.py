#!/usr/bin/env python

"""``Setup.py`` for NeuroDataPub."""

import os
import sys
import setuptools
from setuptools.command.install import install

from neurodatapub.info import __version__

directory = os.path.dirname(os.path.abspath(__file__))

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

packages = [
        "neurodatapub",
        "neurodata.cli"
]

package_data = {
        "neurodatapub": [
                'resources/*'
        ],
}

# Extract package requirements from Conda environment.yml
include_conda_pip_dependencies = False
install_requires = []
dependency_links = []
if include_conda_pip_dependencies:
    path = os.path.join(directory, 'conda', 'environment.yml')
    with open(path) as read_file:
        state = "PREAMBLE"
        for line in read_file:
            line = line.rstrip().lstrip(" -")
            if line == "dependencies:":
                state = "CONDA_DEPS"
            elif line == "pip:":
                state = "PIP_DEPS"
            elif state == "CONDA_DEPS":
                line = '=='.join(line.split('='))
                line = line.split('==')[0]
                # Python is a valid dependency for Conda but not setuptools, so skip it
                if "python" in line:
                    pass
                else:
                    # Appends to dependencies
                    install_requires.append(line)
            elif state == "PIP_DEPS":
                line = line.split('==')[0]
                # Appends to dependency links
                dependency_links.append(line)
                # Adds package name to dependencies
                install_requires.append(line)
print(f'Install requires: {install_requires}')
print(f'Dependency links: {dependency_links}')


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        version = f'v{__version__}'

        if tag != version:
            info = f'Git tag: {tag} does not match the version of this app: {version}'
            sys.exit(info)


def main():
    """Main function of the NeuroDataPub ``setup.py``"""
    setuptools.setup(
            name='neurodatapub',
            version=__version__,
            description=
            'NeuroDataPub: Tool built for publication of BIDS datasets '
            'of the NCCR-Synapsy consortium',
            long_description=
            """NeuroDataPub is built on top of Datalad and helps
            NCCR-Synapsy members in the task of referencing its dataset
            to the NCCR-SYNAPSY GitHub organization. """,
            author='Sebastien Tourbier',
            author_email='sebastien.tourbier@alumni.epfl.ch',
            url='https://github.com/Medical-Image-Analysis-Laboratory/mialsuperresolutiontoolkit',
            entry_points={
                 "console_scripts": [
                     'neurodatapub = neurodatapub.cli.neurodatapub:main',
                 ]
            },
            license='Apache-2.0',
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Science/Research',
                'Intended Audience :: Developers',
                'License :: OSI Approved',
                'Programming Language :: Python',
                'Topic :: Software Development',
                'Topic :: Scientific/Engineering',
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                'Programming Language :: Python :: 3.8'
            ],
            maintainer='Connectomics lab, University Hospital of Lausanne and the NeuroDataPub developers',
            maintainer_email='sebastien.tourbier@alumni.epfl.ch',
            # package_dir={"": "."},  # tell distutils packages are under src
            packages=packages,
            include_package_data=True,
            package_data=package_data,
            # exclude_package_data={"": ["README.txt"]},
            install_requires=install_requires,
            dependency_links=dependency_links,
            python_requires='>=3.8',
            cmdclass={
                'verify': VerifyVersionCommand,
            }
            )


if __name__ == "__main__":
    main()
