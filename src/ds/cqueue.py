from __future__ import annotations
from typing import Any


class CircularQueue:
    """
    Circular Queue.

    An implementation of the first in first out (FIFO) queue which uses a circular
    array for memory optimisation.

    The drawback of a queue without a circular implementation is that every item
    dequeued from the front of the queue increases the gap between the head of the
    array in memory and the head of the queue, wasting memory and leading to longer
    lookup times.

    This circular implementation addresses this drawback by wrapping around the end
    of the array in memory to utilise any empty space at the front. The obvious
    problem with this approach is that the size of the queue is fixed, which is
    impractical for many purposes. For a dynamic implementation, see ./dcqueue.py.

    ...

    Attributes
    ---------
    max_size : int
        The upper bounds of the size of the queue.
    data : list[Any]
        The contents of the queue.
    head : int
        The index of the queue representing the first item in the queue.
    tail : int
        The index of the queue representing the last item in the queue.


    Methods
    -------
    is_full() -> bool
        Returns True if the queue is full.
    is_empty() -> bool
        Returns True if the queue is empty.
    handle_overflow(x: Any)
        Raises an exception
    handle_empty()
        Resets head and tail to -1
    enqueue(x: Any)
        Insert an item at the end of the queue.
    dequeue() -> Any
        Remove and return the item at the start of the queue.
    peek() -> Any
        Return the item at the start of the queue.
    extend(data: list[Any])
        Insert mutliple items at the end of the queue in order.
    __str__() -> str
        Returns a string representation of the queue.
    __len__() -> int
        Returns the distance between head and tail.
    inspect() -> str
        Returns a string of the attributes of the queue. Used for internal purposes
        and testing.
    __iter__() -> Iterator[Any]
        Yields all the items in the queue starting at head and ending at tail.
    """

    def __init__(self, data: list[Any] = [], max_size: int = 8):
        """
        __init__.

        Parameters
        ----------
        data : list[Any]
            List of items to initialise queue with.
        max_size : int
            Upper bounds of the size of the queue.
        """
        self.max_size = max_size
        self.data = [None] * self.max_size
        self.head = self.tail = -1
        self.extend(data)

    def is_full(self) -> bool:
        """
        Is full.

        Returns
        -------
        bool
            Returns True if the queue is full.
        """
        return (self.tail + 1) % self.max_size == self.head

    def is_empty(self) -> bool:
        """
        Is empty.

        Returns
        -------
        bool
            Returns True if the queue is empty.
        """
        return self.head == -1

    def handle_overflow(self, x: Any):
        """
        Handle attempted insertion into full queue.

        Raises an exception.

        Parameters
        ----------
        x : Any
            The item attempted to be enqueued.

        Raises
        ------
        Exception
            This is the default handling method.
        """
        raise Exception("Queue full, cannot enqueue", x)

    def handle_empty(self):
        """
        Handle attempted dequeue from empty queue.

        Reset head and tail to -1.
        """
        self.head = self.tail = -1

    def enqueue(self, x: Any):
        """
        Enqueue.

        Insert an item at the end of the queue.

        Parameters
        ----------
        x : Any
            Item to be inserted.
        """
        if self.is_full():
            self.handle_overflow(x)
        if self.tail == -1:
            self.head = self.tail = 0
        else:
            self.tail = (self.tail + 1) % self.max_size
        self.data[self.tail] = x

    def dequeue(self) -> Any:
        """
        Dequeue.

        Remove and return the item at the start of the queue.

        Returns
        -------
        Any
            Item at start of queue.

        Raises
        ------
        Exception
            If queue is empty.

        """
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        output = self.data[self.head]
        self.data[self.head] = None
        if self.head == self.tail:
            self.handle_empty()
        else:
            self.head = (self.head + 1) % self.max_size
        return output

    def peek(self) -> Any:
        """
        Peek.

        Returns
        -------
        Any
            Item at the start of the queue.

        """
        if self.is_empty():
            raise Exception("Queue empty, cannot peek")
        return self.data[self.head]

    def extend(self, data: list[Any]):
        """
        Extend.

        Insert mutliple items at the end of the queue in order.

        Parameters
        ----------
        data : list[Any]
            List of items to be inserted at the end of the queue in order.
        """
        for x in data:
            self.enqueue(x)

    def __str__(self) -> str:
        """
        __str__.

        Returns
        -------
        str
            Returns a string representation of the queue.
        """
        return str(list(self.iter()))

    def __len__(self) -> int:
        """
        __len__.

        Returns
        -------
        int
            Returns the distance between head and tail.
        """
        if self.head == -1:
            return 0
        return ((self.tail - self.head) % self.max_size) + 1

    def inspect(self) -> str:
        """
        Inspect.

        Returns
        -------
        str
            Returns a string of the attributes of the queue. Used for internal purposes
            and testing.
        """
        return f"{self.data}, {self.max_size}, {self.head}, {self.tail}"

    def __iter__(self) -> Iterator[Any]:
        """
        __iter__.

        Returns
        -------
        Iterator[Any]
            Yields all the items in the queue starting at head and ending at tail.
        """
        if self.head != -1:
            i = self.head
            while i != self.tail:
                yield self.data[i]
                i = (i + 1) % self.max_size
