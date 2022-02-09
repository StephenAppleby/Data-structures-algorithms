from .util import util
from .dcqueue import DynamicCircularQueue


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

    def __init__(self, root=None, data=[], preset=None):
        self.root = root
        self.add = self.add_breadth_first
        self.extend = self.extend_default
        self.delete = self.delete_default
        self.get = self.get_default
        if preset is not None:
            self.extend([x for x in range(preset)])
        else:
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

        def __init__(self, key=None):
            self.l = self.r = None
            self.key = key

        def add_node(self, key, side):
            if side == "l":
                self.l = BinaryTree.BTNode(key)
            if side == "r":
                self.r = BinaryTree.BTNode(key)

        def attach_node(self, node, side):
            if side == "l":
                self.l = node
            if side == "r":
                self.r = node

        def del_node(self, side):
            if side == "l":
                self.l = None
            if side == "r":
                self.r = None

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

        def get_child(self, side):
            if side == "l":
                return self.l
            if side == "r":
                return self.r

        def inspect(self):
            return util.inspect_node(self)

    def add_root(self, key):
        self.root = BinaryTree.BTNode(key)

    def extend_default(self, data=[]):
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
        for k in data:
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

        def delete(node, key):
            if node.l:
                if node.l.key == key:
                    node.l = None
                    return
                delete(node.l, key)
            if node.r:
                if node.r.key == key:
                    node.r = None
                    return
                delete(node.r, key)

        if self.root:
            if self.root.key == key:
                self.root = None
                return
            delete(self.root, key)

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
            return self.root
        for node in self.breadth_first():
            if not node.l:
                node.add_node(key, "l")
                return node.l
            if not node.r:
                node.add_node(key, "r")
                return node.r

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
            queue = DynamicCircularQueue()
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

    def display(self):
        print(util.display(self))

    def __str__(self):
        return util.display(self)

    def inspect(self):
        return util.inspect(self)
