"""
Utility functions for PySke examples
"""

from typing import Tuple

import argparse
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from pyske.core import Distribution, SList
from pyske.core.support import parallel
from pyske.core.util.point_2D import Point_2D
from pyske.core.util.point_3D import Point_3D

PAR = 'parallel'
SEQ = 'sequential'


def standard_parse_command_line(size_arg=True, iter_arg=True, data_arg=True):
    """
    Parse command line for standard example.

    --size size for the size of the generated random list
    --iter iter for the number of iterations
    --data [parallel, sequential] for choosing a sequential or parallel list

    :param size_arg: (default True) flag to select argument --size
    :param iter_arg: (default True) flag to select argument --iter
    :param data_arg: (default True) flag to select argument --data
    :return:  (size, iter, ['parallel' | 'sequential'])
    """
    parser = argparse.ArgumentParser()
    if size_arg:
        parser.add_argument("--size", help="size of the list to generate",
                            type=int, default=1_000_000)
    if iter_arg:
        parser.add_argument("--iter", help="number of iterations",
                            type=int, default=30)
    if data_arg:
        parser.add_argument("--data", help="type of data structure",
                            choices=[PAR, SEQ], default=SEQ)
    size = num_iter = 0
    data_type = PAR
    args = parser.parse_args()
    if size_arg:
        size = max(0, args.size)
    if iter_arg:
        num_iter = max(0, args.iter)
    if data_arg:
        data_type = args.data
    return size, num_iter, data_type


def k_means_parser():
    """
    Parse command line for k-means example.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=5_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    parser.add_argument("--data", help="type of data structure", choices=[PAR, SEQ], default=SEQ)
    parser.add_argument("--clusters", help="number of clusters", type=int, default=3)
    parser.add_argument("--dimensions", help="point dimensions", type=int, default=2)
    parser.add_argument("--show-clusters", help="display the clusters graph of 2D or 3D points",
                        action="store_true")
    return parser

def select_pyske_list(choice):
    """
    Return a PySke list class.

    :param choice: either ``PAR`` or ```SEQ``
    :return: either PList or SList
    """
    # pylint: disable=import-outside-toplevel
    if choice == PAR:
        from pyske.core import PList as ListClass
    else:
        from pyske.core import SList as ListClass
    return ListClass


def select_execute(choice):
    """
    Return an execution function.

    :param choice: either ``PAR`` or ``SEQ``.
    :return: either ``par.at_root`` or ``lambda f: f()``
    """
    # pylint: disable=import-outside-toplevel
    if choice == PAR:
        from pyske.core.util import par
        return par.at_root
    return lambda f: f()


def rand_list(cls, size):
    """
    Return a randomly generated list of numbers.

    The numbers are in the interval [-100, 100].

    :param cls: the class of the generated list.
    :param size: a positive number
        Precondition: size >= 0
    :return: a list of the given class
    """
    # pylint: disable=import-outside-toplevel
    assert size >= 0
    import random
    return cls.init(lambda _: float(random.randint(-100, 100)), size)

def select_point_dimensions(dimensions):
    """
    Return a PySke list class.

    :param dimensions: point dimensions
            Precondition: dimensions >= 2
    :return: a Point
    """
    # pylint: disable=import-outside-toplevel
    if dimensions == 3:
        from pyske.core.util.point_3D import Point_3D as PointClass
    else:
        from pyske.core.util.point_2D import Point_2D as PointClass
    return PointClass

def rand_point_list(cls, size, clusters, dimensions):
    """
    Return a randomly generated list of points.

    :param cls: the class of the generated list.
    :param size: a positive number
        Precondition: size >= 0
    :param clusters: number of clusters
    :param dimensions: point dimensions
            Precondition: dimensions >= 2
    :return: a list of the given class
    """
    x, _ = make_blobs(n_samples=size, centers=clusters, n_features=dimensions)
    x = x.tolist()
    pointclass = select_point_dimensions(dimensions)
    x = list(map(lambda y: pointclass(*y), x))
    distr = Distribution().balanced(size)
    return cls.from_seq(x).distribute(distr)

def print_2D_result(clusters_list: SList[Tuple[Point_2D, int]]):
    """
    Print experiment of 2 dimension points k-means clustering
    """
    if parallel.PID == 0:
        x = clusters_list.map(lambda pair: pair[0].x)
        y = clusters_list.map(lambda pair: pair[0].y)
        colors = clusters_list.map(lambda pair: pair[1])
        plt.scatter(x, y, c=colors)
        plt.show()

def print_3D_result(clusters_list: SList[Tuple[Point_3D, int]]):
    """
    Print experiment of 3 dimension points k-means clustering
    """
    if parallel.PID == 0:
        x = clusters_list.map(lambda pair: pair[0].x)
        y = clusters_list.map(lambda pair: pair[0].y)
        z = clusters_list.map(lambda pair: pair[0].z)
        colors = clusters_list.map(lambda pair: pair[1])

        # Tracé du résultat en 3D
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')  # Affichage en 3D
        ax.scatter(x, y, z, label='Courbe', marker='d', c=colors)  # Tracé des points 3D
        plt.title("Points 3D")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.tight_layout()
        plt.show()

def print_experiment(result, timing, execute, iteration=None):
    """
    Print the result and timing of the experiment.

    :param result: the result of the experiment
    :param timing: the timing of the experiment (a triple)
    :param execute: the execution function
    :param iteration: (optional) the iteration
    """
    avg_t, max_t, all_t = timing
    iter_msg = f'Iteration:\t{iteration}\n' if iteration is not None else ''
    res_msg = f'Result:\t{result}\n'
    timing_msg = f'Timing (average):\t{avg_t}\n' + \
                 f'Timing (maximum):\t{max_t}\n' + \
                 f'Timing (all): \t{all_t}\n'
    msg = iter_msg + res_msg + timing_msg
    execute(lambda: print(msg))


def standard_main(example, size_arg=True, iter_arg=True, data_arg=True):
    """
    Perform an experiment on the given example.

    :param size_arg: (default True) flag to select argument --size
    :param iter_arg: (default True) flag to select argument --iter
    :param data_arg: (default True) flag to select argument --data
    :param example: a function on PySke lists.
    """
    # pylint: disable=import-outside-toplevel
    from pyske.core import Timing
    size, num_iter, choice = standard_parse_command_line(size_arg, iter_arg, data_arg)
    pyske_list_class = select_pyske_list(choice)
    input_list = rand_list(pyske_list_class, size)
    timing = Timing()
    execute = select_execute(choice)
    execute(lambda: print(f'Version:\t{choice}'))
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list)
        timing.stop()
        print_experiment(result, timing.get(), execute, iteration)
