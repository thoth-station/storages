"""A cache to optimize syncs to JanusGraph database."""

from collections import deque


class CacheMiss(Exception):
    """Exception raised when the given item is not present inside cache."""


class Cache(object):
    """A generic cache to store item-value pair for items that are not hashable."""
    def __init__(self):
        # Let's implement cache as a linked list now.
        self._cache = deque()

    def wipe(self):
        """Clear the cache."""
        self._cache.clear()

    def get(self, item):
        """Get the given item from cache."""
        item.pop('id', None)
        for entry in self._cache:
            if entry[0] == item:
                return entry[1]

        raise CacheMiss

    def put(self, item, value):
        """Store the given item with the given value into a cache."""
        item.pop('id', None)  # Do not store ids as they are the actual value.
        self._cache.appendleft((item, value))
