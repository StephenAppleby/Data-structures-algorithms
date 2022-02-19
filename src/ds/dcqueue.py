from __future__ import annotations
from .cqueue import CircularQueue
from typing import Any


class DynamicCircularQueue(CircularQueue):
    """
    Dynamic circular queue.

    A dynamic implementation of the circular queue. This implementation overrides the
    handle_overflow and handle_full methods to resize the queue to fit changing needs.

    The resizing of the queue upon overflow is not a very efficient algorithm (O = n)
    but happens infrequently enough that the benefits far outweight the downsides.

    Example:

    >>> queue = DynamicCircularQueue(data=[x for x in range(6)])
    >>> print(queue)
    [0, 1, 2, 3, 4, 5]
    >>> for x in range(4):
    ...     print(queue.dequeue())
    ...
    0
    1
    2
    3
    >>> print(queue)
    [4, 5]
    >>> queue.extend([x for x in range(6, 20)])
    >>> print(queue)
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    ...

    Methods
    -------
    handle_overflow(x: Any)
        Dequeues all items from the queue into a temporary buffer, doubles the size of
        the queue and adds all items in the buffer back into the queue before
        enqueueing the item x passed in.
    handle_empty()
        Dynamically resizes the queue to a size of 8 upon empty.
    """

    def __init__(self, data=[]):
        """
        __init__.

        Parameters
        ----------
        data : list[Any]
            List of items to initialise the queue with.
        """
        super().__init__(data=data, max_size=8)

    def handle_overflow(self, x: Any):
        """
        Handle overflow.

        Dequeues all items from the queue into a temporary buffer, doubles the size of
        the queue and adds all items in the buffer back into the queue before
        enqueueing the item x passed in.

        Parameters
        ----------
        x : Any
            The item attempted to be enqueued.
        """
        old_data = []
        old_max = self.max_size
        while len(self) > 0:
            old_data.append(self.dequeue())
        self.max_size = old_max * 2
        self.data = [None] * self.max_size
        self.head = self.tail = -1
        for d in old_data:
            self.enqueue(d)

    def handle_empty(self):
        """
        Handle empty.

        Dynamically resizes the queue to a size of 8 upon empty.
        """
        self.max_size = 8
        self.data = [None] * self.max_size
        self.head = self.tail = -1
