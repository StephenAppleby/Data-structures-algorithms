"""
This file contains my own versions of all the common data structures which \
I am writing for my own personal study. I'm following the programiz tutorial \
at https://www.programiz.com/dsa
"""

import util
from math import ceil


class Stack:
    """
    LIFO Stack.

    This representation of the stack handles push, pop, is_empty, is_full, \
    peek, __str__ and extend methods. For example:

    >>> stack = Stack(max_size=3)
    >>> stack.is_empty()
    True
    >>> stack.push(5)
    >>> print(stack)
    [5]
    >>> stack.extend([7, 9])
    >>> stack.is_full()
    True
    >>> stack.pop()
    9
    >>> print(stack)
    [5, 7]
    >>> stack.peek()
    7
    """

    def __init__(self, data=[], max_size=-1):
        self.max_size = max_size
        self.data = []
        self.extend(data)

    def is_full(self):
        return len(self.data) == self.max_size

    def is_empty(self):
        return len(self.data) == 0

    def push(self, x):
        if self.is_full():
            raise Exception("Stack full, cannot push", x)
        self.data.append(x)

    def pop(self):
        if self.is_empty():
            raise Exception("Stack empty, cannot pop")
        return self.data.pop()

    def peek(self):
        return self.data[-1]

    def extend(self, data):
        for x in data:
            self.push(x)

    def __str__(self):
        return str(self.data)


class Queue:
    """
    FIFO Queue.

    This representation of the queue handles enqueue, dequeue, is_empty, \
    is_full, peek, extend, __str__ and __iter__ methods. For example:

    >>> queue = Queue(max_size = 3)
    >>> queue.is_empty()
    True
    >>> queue.enqueue(2)
    >>> print(queue)
    [2]
    >>> queue.extend([4, 6])
    >>> print(queue)
    [2, 4, 6]
    >>> queue.is_full()
    True
    >>> queue.dequeue()
    2
    >>> print(queue)
    [4, 6]
    >>> queue.peek()
    4
    >>> for x in queue: print(x * 2)
    8
    12
    """

    def __init__(self, data=[], max_size=-1):
        self.data = []
        self.max_size = max_size
        self.extend(data)

    def is_empty(self):
        return len(self.data) == 0

    def is_full(self):
        return len(self.data) == self.max_size

    def enqueue(self, x):
        if self.is_full():
            raise Exception("Queue full, cannot enqueue", x)
        self.data.append(x)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        return self.data.pop(0)

    def peek(self):
        return self.data[0]

    def extend(self, arr):
        for x in arr:
            self.enqueue(x)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        return (x for x in self.data)


class CircularQueue:
    """
    FIFO Queue with circular implementation.

    To make the best use of memory, the circular queue reuses the memory at \
    the start of the queue when items overflow the size and there is space. \
    This has the added benefit of bypassing the need to remake the array \
    every time an item is dequeued.

    This implementation is statically sized.

    Supported methods are enqueue, dequeue, is_empty, is_full, peek, extend, \
    __iter__ and __str__. For usage examples, see Queue above

    >>> queue = CircularQueue(size = 3)
    >>> queue.is_empty()
    True
    >>> queue.enqueue(2)
    >>> print(queue)
    [2, None, None]
    >>> queue.extend([4, 6])
    >>> print(queue)
    [2, 4, 6]
    >>> queue.is_full()
    True
    >>> queue.dequeue()
    2
    >>> queue.dequeue()
    4
    >>> queue.enqueue(8)
    >>> print(queue)
    [8, None, 6]
    >>> print(len(queue))
    2
    >>> queue.peek()
    6
    >>> for x in queue: print(x * 2)
    12
    16
    """

    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size
        self.head = self.tail = -1

    def is_empty(self):
        return self.head == -1

    def is_full(self):
        return (self.head - self.tail) % self.size == 1

    def enqueue(self, x):
        if self.is_full():
            self.handle_full()
        if self.head == -1:
            self.head = self.tail = 0
            self.data[self.tail] = x
        else:
            self.tail = (self.tail + 1) % self.size
            self.data[self.tail] = x

    def handle_full(self):
        raise Exception("Queue full, cannot enqueue")

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        output = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.size
        return output

    def peek(self):
        return self.data[self.head]

    def extend(self, arr):
        for x in arr:
            self.enqueue(x)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len([x for x in self if x != None])

    def __iter__(self):
        i = self.head
        for x in range(self.size):
            if self.data[i]:
                yield self.data[i]
            i = (i + 1) % self.size


class DCQueue(CircularQueue):
    """Dynamic implementation of CircularQueue.

    >>> dcqueue = DCQueue(size=3)
    >>> dcqueue.enqueue(3)
    >>> print(dcqueue)
    [3, None, None]
    >>> dcqueue.extend([x for x in range(4)])
    >>> print(dcqueue)
    [3, 0, 1, 2, 3, None]
    """

    def handle_full(self):
        old_data = []
        while len(self) > 0:
            old_data.append(self.dequeue())
        self.size *= 2
        self.data = [None] * self.size
        self.head = self.tail = -1
        for d in old_data:
            self.enqueue(d)


class BinaryTree:
    """

    >>> tree = BinaryTree(data=[x for x in range(7)])
    >>> print(tree)
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6

    """

    def __init__(self, root=None, data=[]):
        self.root = root
        self.add = self.add_breadth_first
        self.extend = self.extend_default
        self.delete = self.delete_default
        self.get = self.get_default
        self.extend(data)

    class BTNode:
        """
        Recursive binary tree base class.

        This base class implements a breadth first add method which adds the new
        node at the first location in left -> right, top -> bottom order. This
        leads to the simple creation of perfect trees. Classes which extend this
        base class will define their own add methods. The extend method uses the
        class specific add method to add multiple nodes at once.

        The default deletion method assigns the node it is called on to None. This
        ensures that the parent of the child deleted has None as a child instead of
        removing it's child attribute, which would happen with del self. Classes
        that extend BTNode will implement their own deletion methods
        as appropriate.

        Basic usage:
        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.root.r.delete()
        >>> print(tree)
               0
           ┌───┘
           1
         ┌─┴─┐
         3   4
        >>> tree.add(2)
        1
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4
        >>> tree.extend([5, 6])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        """

        def __init__(self, key=None, side=None, depth=0, parent=None, tree=None):
            self.l = self.r = None
            self.key = key
            self.side = side
            self.depth = depth
            self.parent = parent
            self.tree = tree
            self.height = 0
            self.recalc_parent_heights()

        def recalc_parent_heights(self):
            if self.parent:
                lh = self.parent.l.height if self.parent.l else -1
                rh = self.parent.r.height if self.parent.r else -1
                self.parent.height = 1 + max(lh, rh)
                self.parent.recalc_parent_heights()

        def detach(self):
            parent = None
            if self.parent:
                parent = self.parent
            if self is self.tree.root:
                self.tree.root = None
            elif self.side == "l":
                self.parent.l = None
            elif self.side == "r":
                self.parent.r = None
            self.side = None
            self.parent = None
            if parent:
                parent.height = parent.get_height()
                parent.recalc_parent_heights()

        def attach(self, node, side):
            if side == "l":
                self.l = node
                node.side = "l"
            if side == "r":
                self.r = node
                node.side = "r"
            node.parent = self

        def move(self, destination, keep_children=False):
            """
            Replace destination with self
            """
            # Detach
            parent = None
            if self.parent:
                parent = self.parent
            self.detach()
            if parent:
                parent.height = parent.get_height()
                parent.recalc_parent_heights()
            # If not going to root attach to parent
            if destination.parent:
                self.parent = destination.parent
                self.depth = destination.parent.depth + 1
                if destination.side == "l":
                    destination.parent.l = self
                    self.side = "l"
                elif destination.side == "r":
                    destination.parent.r = self
                    self.side = "r"
            # If going to root
            else:
                self.tree.root = self
                self.parent = None
            # Manage children
            if not keep_children:
                self.l = None
                self.r = None
                if destination.l and self is not destination.l:
                    self.l = destination.l
                    destination.l.parent = self
                if destination.r and self is not destination.r:
                    self.r = destination.r
                    destination.r.parent = self
                self.height = self.get_height()
            self.recalc_parent_heights()

        def add_l(self, key):
            """
            Manually insert a node to the left of self.

            This convenience method is primarily for testing. You generally won't
            be adding elements to a binary tree by hand.
            """
            self.l = BinaryTree.BTNode(
                key, depth=self.depth + 1, side="l", parent=self, tree=self.tree
            )

        def add_r(self, key):
            """
            Manually insert a node to the right of self.

            This convenience method is primarily for testing. You generally won't
            be adding elements to a binary tree by hand.
            """
            self.r = BinaryTree.BTNode(
                key, depth=self.depth + 1, side="r", parent=self, tree=self.tree
            )

        def get_height(self):
            """
            Returns maximum distance from self to a leaf (external) node.

            Visits every child node recursively to find the maximum distance. This
            approach calculates the height when needed instead of storing the
            height of a node as an attribute. This is because the height of a node
            can change dynamically when children are added or deleted. While this
            could be handled and height keys recalculated every time a node is
            inserted or deleted, this approach seems simpler.

            >>> tree = bt_example(2)
            >>> print(tree)
                   0
               ┌───┴───┐
               1       2
             ┌─┴─┐
             3   4
            >>> tree.get_height()
            2
            >>> tree.r.get_height()
            0
            >>> tree.l.get_height()
            1
            """
            if not self.l and not self.r:
                return 0
            lh = rh = 0
            if self.l:
                lh = self.l.get_height()
            if self.r:
                rh = self.r.get_height()
            return max(lh, rh) + 1

        def inspect(self):
            return util.inspect_node(self)

    def extend_default(self, keys):
        """
        Add each key in keys to the tree in sequence.

        This method utilises the .add method, meaning that as long as the
        binary tree class which is inheriting this base class has properly
        initialised it's own .add method, .extend will work in every case.

        Example using the default breadth-first add method:
        >>> tree = BinaryTree.BTNode(0)
        >>> tree.extend([x for x in range(1, 7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        """
        for k in keys:
            self.add(k)

    def get_default(self, key):
        """
        Default search method.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> print(tree.get(1))
           1
         ┌─┴─┐
         3   4
        """
        found = None
        for node in self.preorder():
            if node.key == key:
                found = node
        if found is None:
            raise KeyError(f"{key} not in tree")
        return found

    def delete_default(self, key):
        """
        Remove a node from the tree.

        Removes the node from memory by changing it's parent's reference to it
        to None. This ensures that the parent maintains it's l or r attribute
        which can be tested for truthyness.
        """
        node = self.get(key)
        node.detach()

    def add_breadth_first(self, key):
        """
        Default insertion method for binary trees.

        Inserts a node into the first available place using breadth-first
        search.

        All insertion methods return the depth of the node inserted

        >>> tree = BinaryTree.BTNode()
        >>> for x in range(0, 5):
        ...     tree.add(x)
        ...     print(tree)
        0
         0
        1
           0
         ┌─┘
         1
        1
           0
         ┌─┴─┐
         1   2
        2
               0
           ┌───┴───┐
           1       2
         ┌─┘
         3
        2
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4

        """
        if not self.root:
            self.add_root(key)
            return 0
        for node in self.breadth_first():
            if not node.l:
                node.add_l(key)
                return node.depth + 1
            if not node.r:
                node.add_r(key)
                return node.depth + 1

    def add_root(self, key):
        self.root = BinaryTree.BTNode(key=key, tree=self)

    def is_perfect(self):
        """
        Returns true if self satisfies the definition of a perfect binary tree.

        A perfect binary tree is any binary tree where each internal node has
        exactly two children and each external node has the same depth.

        >>> tree = bt_example(3)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┘
         3   4   5
        >>> tree.is_perfect()
        False
        >>> tree.add(6)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.is_perfect()
        True
        """

        def node_is_perfect(node):
            # Height of 0
            if not node.l and not node.r:
                return True
            # Only one child
            if not node.l or not node.r:
                return False
            # Both children have same height
            if (
                node.l.get_height() == node.get_height() - 1
                and node.r.get_height() == node.get_height() - 1
            ):
                return node_is_perfect(node.l) and node_is_perfect(node.r)
            # Default case
            return False

        if not self.root:
            return
        return node_is_perfect(self.root)

    def is_full(self):
        """
        Returns true if self is a full binary tree.

        A full binary is defined as any tree in which every node has either
        two or no children.

        >>> tree = bt_example(4)
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        >>> tree.is_full()
        True
        >>> tree.add(3)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┘
         3
        >>> tree.is_full()
        False
        >>> tree.add(4)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4
        >>> tree.is_full()
        True
        """

        def rec_is_full(node):
            # No children
            if not node.l and not node.r:
                return True
            # 2 children
            if node.l and node.r:
                return rec_is_full(node.l) and rec_is_full(node.r)
            # Default case: 1 child
            return False

        if not self.root:
            return
        return rec_is_full(self.root)

    def is_complete(self):
        """
        Returns true if self is a complete binary tree.

        A tree is defined as complete if each level of the tree is full except
        possibly the last level, which must be filled from the left. A tree
        which is constructed only with .add_breadth_first with no nodes
        removed will always be complete.

        >>> tree = bt_example(3)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┘
         3   4   5
        >>> tree.is_complete()
        True
        >>> tree.r.add_r(6)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.is_complete()
        True
        >>> tree.r.l.delete()
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐     └─┐
         3   4       6
        >>> tree.is_complete()
        False
        >>> tree.r.delete()
        >>> print(tree)
               0
           ┌───┘
           1
         ┌─┴─┐
         3   4
        >>> tree.is_complete()
        False
        """
        if not self.root:
            return
        # Nodes in a perfect tree when iterated over breadth-first will all
        # have 2 children (internal) until the last or second last level. After
        # finding a node with one (left) or zero children, every following node
        # will have no children.

        # Track state
        state = "internal"
        # Iterate over nodes breadth-first
        for node in self.breadth_first():
            # Only right child
            if node.r and not node.l:
                return False
            if state == "internal":
                # One or zero children -> change state
                if not node.r:
                    state = "external"
                    continue
            if state == "external":
                # Any child
                if node.r or node.l:
                    return False
        return True

    def is_balanced(self):
        """
        Returns True if self is a balanced binary tree.

        A binary tree is defined as balanced if the difference in height of
        each child of each node is no more than 1. Height is defined as the
        maximum distance to a leaf (external) node where leaf nodes have a
        height of 0.

        >>> tree = bt_example(2)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4

        The left subtree of the root has a height of 1. The right subtree
        is a leaf and so has a height of 0. Therefore it is considered
        balanced.

        >>> tree.is_balanced()
        True
        >>> tree.r.delete()
        >>> print(tree)
               0
           ┌───┘
           1
         ┌─┴─┐
         3   4

        This time, the right subtree of the root doesn't exist and so is
        considered to have a height of -1. The difference between -1 and 1 is
        greater than 1, therefore this tree is not balanced.

        >>> tree.is_balanced()
        False
        """
        if not self.root:
            return
        for node in self.flatten():
            rh = node.r.get_height() if node.r else -1
            lh = node.l.get_height() if node.l else -1
            if (diff := rh - lh) < -1 or diff > 1:
                return False
        return True

    def display(self, item="key"):
        print(util.display(self, item))

    def inspect(self):
        return util.inspect(self)

    def breadth_first(self):
        """
        Returns a left -> right, top -> bottom iterator.

        This iteration method, while slightly more complex than preorder,
        inorder and postorder operations, is needed for binary search tree and
        complete tree operations.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.key for node in tree.breadth_first())
        [0, 1, 2, 3, 4, 5, 6]
        """
        if self.root:
            yield self.root
            queue = DCQueue()
            if self.root.l:
                queue.enqueue(self.root.l)
            if self.root.r:
                queue.enqueue(self.root.r)
            while len(queue) > 0:
                node = queue.dequeue()
                yield node
                if node.l:
                    queue.enqueue(node.l)
                if node.r:
                    queue.enqueue(node.r)

    def flatten(self):
        """
        Returns an inorder iterator for the children of self.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.key for node in tree.flatten())
        [3, 1, 4, 0, 5, 2, 6]
        """
        if self.root:

            def rec_flatten(node):
                if node.l:
                    for n in rec_flatten(node.l):
                        yield n
                yield node
                if node.r:
                    for n in rec_flatten(node.r):
                        yield n

            for n in rec_flatten(self.root):
                yield n

    def preorder(self):
        """
        Returns a preorder iterator for the children of self.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.key for node in tree.preorder())
        [0, 1, 3, 4, 2, 5, 6]
        """
        if self.root:

            def rec_preorder(node):
                yield node
                if node.l:
                    for n in rec_preorder(node.l):
                        yield n
                if node.r:
                    for n in rec_preorder(node.r):
                        yield n

            for n in rec_preorder(self.root):
                yield n

    def postorder(self):
        """
        Returns a postorder iterator for the children of self.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.key for node in tree.postorder())
        [3, 4, 1, 5, 6, 2, 0]
        """
        if self.root:

            def rec_postorder(node):
                if node.l:
                    for n in rec_postorder(node.l):
                        yield n
                if node.r:
                    for n in rec_postorder(node.r):
                        yield n
                yield node

            for n in rec_postorder(self.root):
                yield n

    def fill(self, key):
        """
        Adds nodes to self until perfect.

        Assigns the key argument as the key for each node added this way.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.l.delete()
        >>> print(tree)
               0
               └───┐
                   2
                 ┌─┴─┐
                 5   6

        >>> tree.fill(7)
        >>> print(tree)
               0
           ┌───┴───┐
           7       2
         ┌─┴─┐   ┌─┴─┐
         7   7   5   6
        """
        while not self.is_perfect():
            self.add_breadth_first(key)

    def get_levels(self):
        """
        Returns the children of the tree grouped in arrays by depth.

        >>> tree = bt_example(0)
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> print([[n.key for n in level] for level in tree.get_levels()])
        [[0], [1, 2], [3, 4, 5, 6]]

        """
        output = [[]]
        level = 0
        for node in self.breadth_first():
            if node.depth > level:
                output.append([])
                level += 1
            output[level].append(node)
        return output

    def copy(self):
        """
        Returns a shallow copy of self.

        >>> tree = bt_example(4)
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        >>> copy = tree.copy()
        >>> print(copy)
           0
         ┌─┴─┐
         1   2
        >>> copy.extend([3, 4, 5, 6])
        >>> print(copy)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        """

        def copy_children(original_node, copy_node):
            if original_node.l:
                copy_node.add_l(original_node.l.key)
                copy_children(original_node.l, copy_node.l)
            if original_node.r:
                copy_node.add_r(original_node.r.key)
                copy_children(original_node.r, copy_node.r)

        if not self.root:
            return BinaryTree()
        copy_root = BinaryTree.BTNode(key=self.root.key)
        copy_children(self.root, copy_root)
        return BinaryTree(root=copy_root)


class BinarySearchTree(BinaryTree):
    def __init__(self, **kwargs):
        data = []
        if "data" in kwargs:
            data = kwargs.pop("data")
        super().__init__(**kwargs)
        self.add = self.add_bst
        self.extend = self.balance
        self.delete = self.delete_bst
        self.get = self.get_bst
        self.extend(data=data)

    def add_bst(self, key):
        def rec_add(node, key):
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            if key < node.key:
                if node.l:
                    return rec_add(node.l, key)
                else:
                    node.add_l(key)
                    return node.depth + 1
            if key > node.key:
                if node.r:
                    return rec_add(node.r, key)
                else:
                    node.add_r(key)
                    return node.depth + 1

        if not self.root:
            self.root = self.BTNode(key=key, tree=self)
            return 0
        return rec_add(self.root, key)

    def balance(self, data=[]):
        """
        If self is not balanced, rearrange nodes such that it is balanced.

        This implementation will prioritise placing nodes on the left. This
        method is used as the default extend behaviour, to efficiently
        maintain balance after adding multiple nodes at once.

        >>> bst = bst_example(3)
        >>> print(bst)
                                       3
                       ┌───────────────┴───────────────┐
                       1                               4
               ┌───────┴───────┐                       └───────┐
               0               2                               5
                                                               └───┐
                                                                   6
                                                                   └─┐
                                                                     7
        >>> bst.is_balanced()
        False
        >>> bst.balance()
        >>> print(bst)
                       4
               ┌───────┴───────┐
               2               6
           ┌───┴───┐       ┌───┴───┐
           1       3       5       7
         ┌─┘
         0
        >>> bst.is_balanced()
        True
        """
        old_nodes = [] if not (ar := self.flatten()) else ar
        nodes = sorted(data + [node.key for node in old_nodes])
        if len(nodes) == 0:
            return
        self.add_root(nodes.pop(len(nodes) // 2))

        def build(node, keys):
            if (vals_len := len(keys)) == 0:
                return
            left_vals = keys[0 : (half_vals_len := ceil(vals_len / 2))]
            right_vals = keys[half_vals_len:]
            if len(left_vals) > 0:
                node.add_l(left_vals.pop(len(left_vals) // 2))
                build(node.l, left_vals)
            if len(right_vals) > 0:
                node.add_r(right_vals.pop(len(right_vals) // 2))
                build(node.r, right_vals)

        build(self.root, nodes)

    def get_bst(self, key):
        """
        Binary search algorithm.

        Structuring data in a binary search tree allows the use of this
        look-up method which halves the number of remaining possibilities with
        each iteration leading to a computational complexity of Olog(n). This
        is why the binary search tree is so commonly used when lookup speed is
        key.

        Note that the balance of the tree is also important for keeping lookup
        time low. Consider this poorly balanced binary search tree:
        >>> bst = bst_example(2)
        >>> print(bst)
                                       0
                                       └───────────────┐
                                                       1
                                                       └───────┐
                                                               2
                                                               └───┐
                                                                   3
                                                                   └─┐
                                                                     4

        This linear bst is no better than an array and access time is now
        On. Here we have 5 elements and the maximum number of nodes traversed
        in order to locate a node is 5. On the other hand, consider this
        well balanced bst:
        >>> bst = bst_example(1)
        >>> print(bst)
                       7
               ┌───────┴───────┐
               3              11
           ┌───┴───┐       ┌───┴───┐
           1       5       9      13
         ┌─┴─┐   ┌─┴─┐   ┌─┴─┐   ┌─┴─┐
         0   2   4   6   8  10  12  14

        Here there are 14 elements and each can be reached within 4 of the
        root.

        For this reason we have self-balancing trees like the AVL tree and the
        Red-Black tree. This basic implementation however does not include
        any advanced self-balancing techniques, but does rebalance when adding
        multiple elements at once, however in a slower fashion than a proper
        self-balancing tree.
        """

        def rec_get(node, key):
            if key == node.key:
                return node
            if key < node.key and node.l:
                return rec_get(node.l, key)
            if key > node.key and node.r:
                return rec_get(node.r, key)

        found = None
        if self.root:
            found = rec_get(self.root, key)
        if found is None:
            raise KeyError(f"{key} not in tree")
        return found

    def delete_bst(self, key):
        """
        Remove node from tree.

        When removing nodes from a binary search tree, it helps to recognise
        the difference between the structure of the tree and the position of
        its keys. In every case of deleting a node, the structure will
        contain one less node than before, but in several cases the position
        of the keys in the tree will need to change as well.

        In order to ensure that the tree that self is a part of adheres to the
        definition of a binary search tree, three cases need to be taken into
        account. The first is if self is a leaf node, in which case it is
        simply removed from the tree. The second is in the case that self has
        one child, in which case the child is attached to the parent of self
        in it's place. If self has two children, we need to identify the
        inorder successor of self by taken the left-most child of the right
        child of self, and switching it into the place of self.

        >>> bst = bst_example(1)
        >>> print(bst)
                       7
               ┌───────┴───────┐
               3              11
           ┌───┴───┐       ┌───┴───┐
           1       5       9      13
         ┌─┴─┐   ┌─┴─┐   ┌─┴─┐   ┌─┴─┐
         0   2   4   6   8  10  12  14

        """
        to_delete = self.get(key)
        # Case 1: Leaf node
        if not to_delete.l and not to_delete.r:
            to_delete.detach()
        # Case 2: One child
        elif bool(to_delete.l) != bool(to_delete.r):
            child = to_delete.l if to_delete.l else to_delete.r
            # Replace child with self
            child.move(to_delete, keep_children=True)
        # Case 3: Two children
        else:
            successor = to_delete.r
            while successor.l:
                successor = successor.l
            # Rescue successors right child
            if successor.r:
                successor.r.move(successor, keep_children=True)
            successor.move(to_delete)

    def is_bst(self):
        """
        Returns True if self satisfies the definition of a binary search tree.
        """
        nodes = list(self.flatten())
        return all(nodes[i] <= nodes[i + 1] for i in range(len(nodes) - 1))


class AVLTree(BinarySearchTree):
    def __init__(self, **kwargs):
        data = []
        if "data" in kwargs:
            data = kwargs.pop("data")
        super().__init__(**kwargs)
        self.add = self.add_avl
        self.extend = self.balance
        self.delete = self.delete_bst
        self.get = self.get_bst
        self.extend(data=data)

    class AVLNode(BinaryTree.BTNode):
        def left_rotate(self):
            child = self.r
            child.detach()
            if child.l:
                cl = child.l
                cl.detach()
                self.attach(cl, "r")
            if not self.parent:
                self.detach()
                self.tree.root = child
            else:
                parent = self.parent
                side = self.side
                self.detach()
                parent.attach(child, side)
            child.attach(self, "l")
            child.height = child.get_height()
            child.recalc_parent_heights()

        def add_l(self, key):
            """
            Manually insert a node to the left of self.

            This convenience method is primarily for testing. You generally won't
            be adding elements to a binary tree by hand.
            """
            self.l = AVLTree.AVLNode(
                key, depth=self.depth + 1, side="l", parent=self, tree=self.tree
            )

        def add_r(self, key):
            """
            Manually insert a node to the right of self.

            This convenience method is primarily for testing. You generally won't
            be adding elements to a binary tree by hand.
            """
            self.r = AVLTree.AVLNode(
                key, depth=self.depth + 1, side="r", parent=self, tree=self.tree
            )

    def add_avl(self, key):
        def rec_add(node, key):
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            if key < node.key:
                if node.l:
                    return rec_add(node.l, key)
                else:
                    node.add_l(key)
                    return node.depth + 1
            if key > node.key:
                if node.r:
                    return rec_add(node.r, key)
                else:
                    node.add_r(key)
                    return node.depth + 1

        if not self.root:
            self.add_root(key)
            return 0
        return rec_add(self.root, key)

    def add_root(self, key):
        self.root = AVLTree.AVLNode(key=key, tree=self)


def bt_example(i):
    examples = []
    examples.append(BinaryTree(data=[x for x in range(7)]))
    examples.append(BinaryTree(data=[x for x in range(15)]))
    examples.append(BinaryTree(data=[x for x in range(5)]))
    examples.append(BinaryTree(data=[x for x in range(6)]))
    examples.append(BinaryTree(data=[0, 1, 2]))
    return examples[i]


def bst_example(i):
    examples = []
    examples.append(BSTNode(data=[x for x in range(7)]))
    examples.append(BSTNode(data=[x for x in range(15)]))
    patho_bst = BSTNode(key=0)
    for x in range(1, 5):
        patho_bst.add(x)
    examples.append(patho_bst)
    patho_bst_two = BSTNode(key=3)
    patho_bst_two.add(1)
    patho_bst_two.add(2)
    patho_bst_two.add(0)
    patho_bst_two.add(4)
    patho_bst_two.add(5)
    patho_bst_two.add(6)
    patho_bst_two.add(7)
    examples.append(patho_bst_two)
    return examples[i]


if __name__ == "__main__":
    # import doctest

    # doctest.testmod()
    avl = AVLTree()
    for x in [3, 1, 2, 0, 5, 4, 6]:
        avl.add(x)
    avl.display()
    print(avl.root)
    avl.root.r.l.add_r(14)
    avl.display()
