PySke API
#########

PySke API offer applications implemented with list and tree skeletons.
The user can use the sequential or parallel version.
The parallel version allows a faster execution time when its launched on several processors, cores or computers.

Run examples with parallel computing:

    .. code-block:: console

        mpirun -np NB_CORES python3 PROGRAM_NAME [OPTIONS]

Examples without :code:`--data` option are only runnable in parallel.

List Examples
=============

Dot Product
-----------

.. py:module:: pyske.examples.list.dot_product


Dot Product functions
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: opt_dot_product

.. autofunction:: dot_product

Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:dot_product_parser()
    :prog: dot_product_main.py


Discrete Fast Fourier Transform
-------------------------------
.. py:module:: pyske.examples.list.fft

Fast Fourier Transform function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: fft

Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:standard_parser(data_arg=False)
    :prog: fft_main.py


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

.. autoprogram:: pyske.examples.list.util:k_means_parser()
    :prog: k_means_main.py


Maximum Prefix Sum
------------------

.. py:module:: pyske.examples.list.maximum_prefix_sum

Maximum Prefix Sum function
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: mps

Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:standard_parser()
    :prog: maximum_prefix_sum_main.py

Maximum Segment Sum
-------------------

Maximum Segment Sum is the task of finding a contiguous subarray with the largest sum.

Naive version
^^^^^^^^^^^^^^^^

.. py:module:: pyske.core.support.maximum_subarray_problem

One of the naive version is to transform a list of numbers into a list of all its sub-arrays.
Then, we have to sum all of its sub-arrays and take the maximum of them.

.. autofunction:: list_to_segment


Maximum Segment Sum function
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:module:: pyske.examples.list.maximum_segment_sum

.. autofunction:: maximum_segment_sum

Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:standard_parser()
    :prog: maximum_segment_sum_main.py

Parallel Regular Sampling Sort
------------------------------

.. py:module:: pyske.examples.list.regular_sampling_sort


Broadcast function
^^^^^^^^^^^^^^^^^^

.. autofunction:: bcast

Sort function
^^^^^^^^^^^^^

.. autofunction:: pssr


Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:standard_parser()
    :prog: regular_sampling_sort_main.py

Variance Example
----------------

.. py:module:: pyske.examples.list.variance

Variance function
^^^^^^^^^^^^^^^^^

.. autofunction:: variance

Running Example
^^^^^^^^^^^^^^^

.. autoprogram:: pyske.examples.list.util:standard_parser()
    :prog: variance_main.py


Tree Examples
=============