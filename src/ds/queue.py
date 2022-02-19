from typing import Any


class Queue:
    """
    Queue.

    A first in first out (FIFO) data structure.

    Example:

    >>> queue = Queue(data=[x for x in range(6)])
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

    Attributes
    ---------
    data : list[Any]
        List of items to initialise the queue with.
    max_size : int
        Upper bounds of the size of the queue.

    Methods
    -------
    is_empty() -> bool
        Returns True if the queue is empty.
    is_full() -> bool
        Returns True if the queue is full.
    enqueue(x: Any)
        Insert an item at the end of the queue.
    dequeue() -> Any
        Remove and return the item at the front of the queue.
    peek() -> Any
        Return the item at the front of the queue.
    extend(data: list[Any])
        Insert multiple items at the end of the queue in order.
    __str__ -> str
        Return a string representation of the queue data.
    """

    def __init__(self, data: list[Any] = [], max_size: int = -1):
        """
        __init__.

        Parameters
        ----------
        data : list[Any]
            List of items to initialise the queue with.
        max_size : int
            Upper bounds of the size of the queue.
        """
        self.data = []
        self.max_size = max_size
        self.extend(data)

    def is_empty(self) -> bool:
        """
        Is empty.

        Returns
        -------
        bool
            Returns True if there are no items in the queue.

        """
        return len(self.data) == 0

    def is_full(self) -> bool:
        """
        Is full.

        Returns
        -------
        bool
            Returns True if the queue is full.
        """
        return len(self.data) == self.max_size

    def enqueue(self, x: Any):
        """
        Insert item at end of queue.

        Parameters
        ----------
        x : Any
            Item to be inserted.

        Raises
        -----
        Exception
            If queue is full.
        """
        if self.is_full():
            raise Exception("Queue full, cannot enqueue", x)
        self.data.append(x)

    def dequeue(self) -> Any:
        """
        Remove and return item at start of queue.

        Returns
        -------
        Any
            Item at start of queue.

        Raises
        -----
        Exception
            If queue is empty.
        """
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        return self.data.pop(0)

    def peek(self) -> Any:
        """
        Peek.

        Returns
        -------
        Any
            The item at the start of the queue.
        """
        return self.data[0]

    def extend(self, data: list[Any]):
        """
        Insert multiple items.

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
            String representation of queue data.
        """
        return str(self.data)
