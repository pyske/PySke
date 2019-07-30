"""
A module to time the execution of PySke parallel programs
"""
from operator import add
from pyske.core.list.plist import PList
from pyske.core.util import par


class Timing:
    """
    A class to time the execution of PySke parallel programs
    """
    def __init__(self):
        self.__elapsed = None

    def start(self):
        """
        Starts the timing.
        :return: None
        """
        self.__elapsed = PList.init(lambda _: par.wtime())

    def stop(self):
        """
        Stops the timing
        :return: None
        """
        if self.__elapsed is None:
            raise Exception("timing: stop() called before start()")
        self.__elapsed = self.__elapsed.map(lambda time: par.wtime() - time)

    def get(self):
        """
        Return a tuple containing:
        - the maximum elapsed time (on all the processors)
        - the average elapsed time (on all the processors)
        - the list of elapsed times on all the processors
        :return: float, float, list
        """
        max_elapsed = self.__elapsed.reduce(max)
        avg_elapsed = self.__elapsed.reduce(add) / self.__elapsed.length()
        all_elapsed = self.__elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()
        return max_elapsed, avg_elapsed, all_elapsed
