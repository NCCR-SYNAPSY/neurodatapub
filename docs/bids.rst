
.. _bids:

*******************************************
BIDS Standard
*******************************************

By default, a dataset published with `NeuroDataPub` SHOULD ADOPT the :abbr:`BIDS (Brain Imaging Data Structure)` standard for data organization. This means that `NeuroDataPub` handle by default only datasets formatted following the BIDS standard. However, since `v0.4`, `NeuroDataPub` can handle dataset not necessary in a BIDS format with the `--is_not_bids` option. See :ref:`cmdusage` for more details.

For more information about BIDS, please consult the `BIDS Website <https://bids.neuroimaging.io/>`_ and the `Online BIDS Specifications <https://bids-specification.readthedocs.io/en/stable/>`_. `HeuDiConv <https://github.com/nipy/heudiconv>`_ can assist you in converting DICOM brain imaging data to BIDS. A nice tutorial can be found @ `BIDS Tutorial Series: HeuDiConv Walkthrough <http://reproducibility.stanford.edu/bids-tutorial-series-part-2a/>`_ .

.. important:: 
    Before using `NeuroDataPub`, we highly recommend you to validate your BIDS structured dataset with the free, online `BIDS Validator <http://bids-standard.github.io/bids-validator/>`_.
