"""
Utility functions for tests
"""


def swap(size):
    """Bijection that swaps odd and even elements."""
    return lambda index: \
        index if index == size - 1 and size % 2 == 1 \
            else index + 1 if index % 2 == 0 \
            else index - 1
