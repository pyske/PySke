PySke API
=========

PySke API offer applications implemented with list and tree skeletons.
The user can use the sequential or parallel version.
The parallel version allows a faster execution time when its launched on several processors, cores or computers.

Dot Product
-----------

.. py:module:: pyske.examples.list.dot_product


Dot Product function
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: opt_dot_product

Dot Product Variant
^^^^^^^^^^^^^^^^^^^

.. autofunction:: dot_product

Running Example
^^^^^^^^^^^^^^^

.. argparse::
    :module: pyske.examples.list.util
    :func: dot_product_parser
    :prog: python3 dot_product_main.py


Discrete Fast Fourier Transform
-------------------------------

K-means Clustering
------------------

K-means clustering is an unsupervised algorithm that aims to partition group of points in k clusters.

K-means function
^^^^^^^^^^^^^^^^

.. py:module:: pyske.examples.list.k_means

.. autofunction:: k_means

Initialization functions
^^^^^^^^^^^^^^^^^^^^^^^^

This is the standard method that initializes the centroids. This method chooses the centroids in order that each point is as far as possible from the other.

.. autofunction:: k_means_init


Point Interface
^^^^^^^^^^^^^^^

K-means algorithm takes a list of points in parameters. For now two versions implement this class, one for 2 dimension points and another for 3 dimension points.

Point 2D class implementation:

.. autoclass:: pyske.core.util.point_2D.Point_2D
    :members:
    :special-members:
    :member-order: bysource

Running Example
^^^^^^^^^^^^^^^

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

