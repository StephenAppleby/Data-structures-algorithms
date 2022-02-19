from typing import Any


class Stack:
    """
    Stack.

    A last in first out (LIFO) data structure.

    Example:

    >>> stack = Stack(data=[x for x in range(10)])
    >>> print(stack)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> for x in range(5):
    ...     print(stack.pop())
    ...
    9
    8
    7
    6
    5
    >>> print(stack)
    [0, 1, 2, 3, 4]

    ...

    Attributes
    ---------
    max_size : int = -1
        Upper limit on the size of the stack.
    data : list[Any]
        The contents of the stack.

    Methods
    -------
    is_full() -> bool
        Returns True if the stack is full.
    is_empty() -> bool
        Returns True if the stack is empty.
    push(x: Any)
        Insert a new item at the end of the stack.
    pop() -> Any
        Remove and return the item at the end of the stack.
    peek() -> Any
        Return but not remove the item at the end of the stack.
    extend(data: list[Any])
        Add multiple items to the end of the stack in order.
    __str__() -> str
        Return a string representation of the stack data.
    """

    def __init__(self, data: list[Any] = [], max_size: int = -1):
        """
        __init__.

        Parameters
        ----------
        data : list[Any]
            List of items to initialise the stack with.
        max_size : int
            Upper limit of the size of the stack.
        """
        self.max_size = max_size
        self.data = []
        self.extend(data)

    def is_full(self) -> bool:
        """
        Is full.

        Returns
        -------
        bool
            Returns True if the stack is full.
        """
        return len(self.data) == self.max_size

    def is_empty(self) -> bool:
        """
        Is empty.

        Returns
        -------
        bool
            Returns True if the stack is empty.
        """
        return len(self.data) == 0

    def push(self, x: Any):
        """
        Push.

        Insert a new item at the end of the stack.

        Parameters
        ----------
        x : Any
            The item to be added.
        """
        if self.is_full():
            raise Exception("Stack full, cannot push", x)
        self.data.append(x)

    def pop(self) -> Any:
        """
        Pop.

        Remove and return the last item at the end of the stack.

        Returns
        -------
        Any
            The last item at the end of the stack.
        """
        if self.is_empty():
            raise Exception("Stack empty, cannot pop")
        return self.data.pop()

    def peek(self) -> Any:
        """
        Peek.

        Returns
        -------
        Any
            The last item at the end of the stack.
        """
        return self.data[-1]

    def extend(self, data: list[Any]):
        """
        Push mutliple items.

        Parameters
        ----------
        data : list[Any]
            List of items to be pushed.
        """
        for x in data:
            self.push(x)

    def __str__(self) -> str:
        """
        __str__.

        Returns
        -------
        str
            String representation of the stack data.
        """
        return str(self.data)
