"""Neurodatapub package information."""

_version_major = 0
_version_minor = 2

__release_date__ = '09.08.2021'

__version__ = "%s.%s" % (_version_major, _version_minor)

# __current_year__ = datetime.datetime.now().strftime("%Y")
__current_year__ = '2021'

__author__ = 'Sebastien Tourbier'
__copyright__ = ('Copyright {year}, '.format(year=__current_year__)
                 + 'Connectomics Lab, University Hospital Center and '
                 + 'University of Lausanne (UNIL-CHUV), Switzerland, '
                 + 'and contributors')
__credits__ = ('Contributors: please check the ``.zenodo.json`` file '
               'at the top-level folder of the repository')
__license__ = 'Apache 2.0'
__maintainer__ = 'Sebastien Tourbier'
__email__ = 'sebastien.tourbier@alumni.epfl.ch'
__status__ = 'Prototype'

__packagename__ = 'neurodatapub'

__url__ = 'https://github.com/NCCR-SYNAPSY/{name}'.format(name=__packagename__)

DOWNLOAD_URL = (
    'https://github.com/NCCR-SYNAPSY/{name}/archive/{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__)
)
