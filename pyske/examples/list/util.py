"""
Utility functions for PySke examples
"""

PAR = 'parallel'
SEQ = 'sequential'


def standard_parse_command_line():
    """
    Parse command line for standard example.

    --size size for the size of the generated random list
    --iter iter for the number of iterations
    --input_list [parallel, sequential] for choosing a sequential or parallel list

    :return:  (size, iter, input_list)
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    parser.add_argument("--data", help="type of data structure",
                        choices=[PAR, SEQ], default=SEQ)
    args = parser.parse_args()
    return max(0, args.size), max(0, args.iter), args.data


def select_pyske_list(choice):
    """
    Return a PySke list class.

    :param choice: either ``PAR`` or ```SEQ``
    :return: either PList or SList
    """
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
    assert size >= 0
    import random
    return cls.init(lambda _: float(random.randint(-100, 100)), size)


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


def standard_main(example):
    """
    Perform an experiment on the given example.

    :param example: a function on PySke lists.
    """
    from pyske.core import Timing
    size, num_iter, choice = standard_parse_command_line()
    pyske_list_class = select_pyske_list(choice)
    input_list = rand_list(pyske_list_class, size)
    timing = Timing()
    execute = select_execute(choice)
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list)
        timing.stop()
        print_experiment(result, timing.get(), execute, iteration)
