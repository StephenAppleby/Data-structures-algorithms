from __future__ import annotations
from .bt import BinaryTree


class Heap:
    """
    Heap.

    An array implementation of the binary heap data structure. A heap guarantees that
    the first element in the array will be the largest for a max heap or the smallest
    for a min heap. The rest of the array is only loosely ordered; order is not
    guaranteed.

    ...

    Attributes
    ---------
    data : list[int]
        The contents of the heap. It is treated as a complete binary tree where the
        location of the left child of a node at index n is (n * 2) + 1 and the
        right child is (n * 2) + 2.

    Methods
    -------
    compare(a: int, b: int) -> bool
        Returns True if a > b if initialised as a max heap and a < b for a min heap.
        Used for internal methods.
    heapify_node(i: int, size: int, recursive: str)
        Ensures that the node at data[i] is greater than the nodes at data[(i * 2) + 1]
        and data[(i * 2) + 2] for a max heap, or less than for a min heap. Can be run
        recursively to check nodes above or below in the tree structure.
    heapify()
        Guarantees that the first element of the heap will be the largest for a max
        heap or the smallest for a min heap by running heapify_node on each node, not
        including leaf nodes.
    add(key: int)
        Insert a node into the heap and maintain heap ordering properties.
    pop() -> int
        Remove and return the first element of the heap and reorder the heap to
        maintain heap ordering properties.
    peek() -> int
        Return the first element without altering the heap.
    is_heap() -> bool
        Returns True if the heap satisfies heap ordering properties.
    display()
        Render the heap to the console in a readable format. The heap's data is used
        to initialise a BinaryTree (./bt.py) and use it's display implementation (found
        at ./util/util.py).
    """

    def __init__(self, data: list[int] = [], max_or_min: str = "max"):
        """
        __init__.

        Parameters
        ----------
        data : list[int] = []
            List of ints to initialise the heap with.
        max_or_min : str = "max"
            Initialise the heap as either a max heap or a min heap.
        """
        if max_or_min == "max":
            self.compare = lambda a, b: a > b
        if max_or_min == "min":
            self.compare = lambda a, b: a < b
        self.data = data
        self.heapify()

    def heapify_node(self, i: int, size: int, recursive: str = None):
        """
        Heapify a node.

        Ensures that the node at data[i] is greater than the nodes at data[(i * 2) + 1]
        and data[(i * 2) + 2] for a max heap, or less than for a min heap. Can be run
        recursively to check nodes above or below in the tree structure.

        Parameters
        ----------
        i : int
            The index of the node to check.
        size : int
            The size of the heap
        recursive : str = None
            If the heap was altered during the heapify process, the method can be run
            recursively on the parent of the node changed (recursive == \"up\") or the
            child which was changed (recursive == \"down\") to guarantee that the whole
            heap maintains heap ordering properties.
        """
        top = i
        l = (2 * i) + 1
        r = (2 * i) + 2
        kids = []
        if l < size and not self.compare(self.data[i], self.data[l]):
            kids.append(l)
        if r < size and not self.compare(self.data[i], self.data[r]):
            kids.append(r)
        if len(kids) == 2:
            top = (
                kids[0]
                if self.compare(self.data[kids[0]], self.data[kids[1]])
                else kids[1]
            )
        if len(kids) == 1:
            top = kids[0]
        if top != i:
            self.data[i], self.data[top] = self.data[top], self.data[i]
            if recursive == "down":
                self.heapify_node(top, size, "down")
            if recursive == "up":
                self.heapify_node(abs(i - 1) // 2, size, "up")

    def heapify(self):
        """
        Heapify.

        Guarantees that the first element of the heap will be the largest for a max
        heap or the smallest for a min heap by running heapify_node on each node, not
        including leaf nodes.
        """

        size = len(self.data)
        if size < 1:
            return
        last_non_leaf = (size // 2) - 1
        for i in range(last_non_leaf, -1, -1):
            self.heapify_node(i, size, recursive="down")

    def add(self, key: int):
        """
        Add a node.

        Insert a node into the heap and maintain heap ordering properties.

        Parameters
        ----------
        key : int
            The key of the node to be inserted.
        """
        self.data.append(key)
        size = len(self.data)
        self.heapify_node(abs(size - 2) // 2, size, recursive="up")

    def pop(self) -> int:
        """
        Pop.

        Remove and return the first element of the heap and reorder the heap to
        maintain heap ordering properties.

        Returns
        -------
        int
            The first element of the heap.

        """
        size = len(self.data)
        if size == 0:
            raise Exception("Heap empty, cannot pop")
        if size == 1:
            return self.data.pop(0)
        output = self.data[0]
        self.data[0] = self.data.pop(size - 1)
        self.heapify_node(0, size - 1, recursive="down")
        return output

    def peek(self) -> int:
        """
        Peek.

        Returns
        -------
        int
            Return the first element without altering the heap.
        """
        return self.data[0]

    def is_heap(self) -> bool:
        """
        Is heap.

        Returns
        -------
        bool
            Returns True if the heap satisfies heap ordering properties.
        """
        size = len(self.data)
        for i in range(size // 2):
            l = (2 * i) + 1
            r = (2 * i) + 2
            if l < size and not self.compare(self.data[i], self.data[l]):
                return False
            if r < size and not self.compare(self.data[i], self.data[r]):
                return False
        return True

    def display(self):
        """
        Display.

        Render the heap to the console in a readable format. The heap's data is used
        to initialise a BinaryTree (./bt.py) and use it's display implementation (found
        at ./util/util.py).
        """
        tree = BinaryTree(data=self.data)
        tree.display()
