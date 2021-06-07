PySke API
=========

Pyske API offer applications implemented with list and tree skeletons.
The user can use the sequential or parallel version.
The parallel version allows a faster execution time when its launched on several processors or computers.

Dot Product
-----------

Discrete Fast Fourier Transform
-------------------------------

K-means Clustering
------------------

K-means clustering is an unsupervised algorithm that aims to partition group of points in k clusters.

K-means function
^^^^^^^^^^^^^^^^

.. py:module:: pyske.examples.list.k_means

.. autofunction:: k_means

Here the implementation of the 2 dimensions point class.

.. autoclass:: pyske.core.util.point_2D.Point_2D
    :members:
    :special-members:
    :show-inheritance:
    :private-members:
    :member-order: bysource

Initialization functions
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: k_means_init

Running Example
^^^^^^^^^^^^^^^^^^^^

.. argparse::
    :module: pyske.examples.list.util
    :func: k_means_parser
    :prog: python3 k_means_main.py


Maximum Prefix Sum
------------------

Maximum Segment Sum
-------------------

Parallel Regular Sampling Sort
------------------------------

Variance Example
----------------

