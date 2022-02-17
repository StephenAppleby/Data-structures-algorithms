from __future__ import annotations
from .util import util
from .dcqueue import DynamicCircularQueue


class BinaryTree:
    """
    Binary Tree.

    This is a base class for binary tree data structures like the binary search tree.

    It contains the definition of a subclass: BTNode. This represents a node of the
    tree and contains methods for adding, attaching and deleting children from the
    node.

    The base class also contains methods for ascertaining properties of the tree like
    is_perfect, is_full, is_complete and is_balanced. There are also methods for
    returning iterators over the nodes of the tree in breadth_first, inorder(flatten),
    preorder and postorder priorities.

    This base class also uses an implementation defined in ./util/util.py for rendering
    a binary tree to the console

    The binary tree can be rendered to the console with the display() method. The logic
    for this implementation can be found in ./util/util.py. For example:

    >>> tree = BinaryTree().preset(7)
    >>> tree.display()
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6

    ...

    Attributes
    ---------
    BTNode : class
        A subclass defining the node of a binary tree, with key and left and right
        children.
    root : BTNode
        The root node of the tree.

    Methods
    -------
    preset(n: int) -> BinaryTree
        Modify an empty tree to add n nodes in ascending order to the tree. Calling the
        method on the tree after it has been initialised ensures that if it is being
        called on a class extending BinaryTree, the correct methods and types are used
        to construct the tree.
    add_root(key: int)
        Add a node with key as the root of the tree.
    extend_default(data: list[int] = [])
        The default method of extending a tree with a list of keys is to call add(key)
        for each key in the list.
    get_default(key: int) -> BTNode
        The default get behaviour searches the tree with preorder priority and returns
        the node if present. Raises a KeyError if node absent.
    delete_default(key: int)
        The default delete behavior searches the tree for key with preorder priority
        and removes it from it's parent. Note that this will delete the subtree
        as well.
    add_breadth_first(key: int)
        This is the default add method for the base class. It creates a new node in
        the place of the first missing space when traversed breadth-first.
    is_perfect() -> bool
        A binary tree is perfect if every internal node has two children and all the
        leaf nodes are on the same level.
    is_full() -> bool
        A binary tree is full if every node has either 0 or 2 children.
    is_complete() -> bool
        A binary tree is complete if every space in every level of the tree is filled,
        except possibly the lowest level which must be filled from the left.
    is_balanced() -> bool
        A binary tree is balanced if the difference between the height of the children
        of each node is no greater than 1 and no less than -1.
    breadth_first() -> Iterator[BTNode]
        Returns an iterator which provides all the nodes in the tree from top to
        bottom, left to right.
    flatten() -> Iterator[BTNode]
        Returns an iterator which provides all the nodes in the tree in in-order
        priority.
    preorder() -> Iterator[BTNode]
        Returns an iterator which provides all the nodes in the tree in preorder
        priority.
    postorder() -> Iterator[BTNode]
        Returns an iterator which provides all the nodes in the tree in postorder
        priority.
    display()
        Prints a visual representation of the tree to the console. Reccommended for
        use with trees no greater than 31 nodes, depending on the width of the console.
    str() -> str
        Returns a string representation of the tree.
    inspect() -> str
        For testing and internal use. Returns a formatted list of the contents of the
        tree.
    """

    def __init__(self, root: BTNode = None, data: list[int] = []):
        """__init__.

        Parameters
        ----------
        root : BTNode
            Optional root node to initialise the tree with.
        data : list[int]
            Initial data to input into the tree.
        """
        self.root = root
        self.add = self.add_breadth_first
        self.extend = self.extend_default
        self.delete = self.delete_default
        self.get = self.get_default
        self.extend(data)

    def preset(self, n: int) -> BinaryTree:
        """
        Preset.

        Adds n elements of values 0 - n to the tree. Useful for examples and testing.

        Parameters
        ----------
        n : int
            Nodes to add

        Returns
        -------
        BinaryTree
            Self
        """
        self.extend([x for x in range(n)])
        return self

    class BTNode:
        """
        BTNode.

        Represents a node in a binary tree.

        ...

        Attributes
        ---------
        key : int
            Key
        l : BTNode
            Left child
        r : BTNode
            Right child

        Methods
        -------
        add_node(key: int, side: str)
            Create new child with key at side where side is either \"l\" for left or
            \"r\" for right. This can be used to override existing child.
        attach_node(node: BTNode, side: str)
            Attach existing node to side where side is either \"l\" for left or \"r\"
            for right. This can be used to override existing child.
        del_node(side: str)
            Remove the child on side where side is either \"l\" for left or \"r\" for
            right.
        get_height() -> int
            Returns the height of the node where height is the largest distance to a
            child leaf node.
        inspect() -> str
            Returns a formatted string representing the node and its attributes. Used
            for internal purposes and testing.
        """

        def __init__(self, key: int = None):
            """__init__.

            Parameters
            ----------
            key : int
                Key
            """
            self.l = self.r = None
            self.key = key

        def add_node(self, key: int, side: str):
            """
            Add node.

            Create new child with key at side where side is either \"l\" for left or
            \"r\" for right. This can be used to override existing child.

            Parameters
            ----------
            key : int
                Node key
            side : str
                Side to insert node.
            """

            if side == "l":
                self.l = BinaryTree.BTNode(key)
            if side == "r":
                self.r = BinaryTree.BTNode(key)

        def attach_node(self, node: BTNode, side: str):
            """
            Attach node.

            Attach existing node to side where side is either \"l\" for left or \"r\"
            for right. This can be used to override existing child.

            Parameters
            ----------
            node : BTNode
                Node to be attached.
            side : str
                Side to attach to.
            """
            if side == "l":
                self.l = node
            if side == "r":
                self.r = node

        def del_node(self, side: str):
            """
            Delete node.

            Remove the child on side where side is either \"l\" for left or \"r\" for
            right.

            Parameters
            ----------
            side : str
                Side to remove.
            """
            if side == "l":
                self.l = None
            if side == "r":
                self.r = None

        def get_height(self) -> int:
            """
            Get height of node.


            Returns
            -------
            int
                Returns the height of the node where height is the largest distance
                to a child leaf node.
            """
            if not self.l and not self.r:
                return 0
            lh = rh = 0
            if self.l:
                lh = self.l.get_height()
            if self.r:
                rh = self.r.get_height()
            return max(lh, rh) + 1

        def inspect(self) -> str:
            """
            Inspect node attributes.

            Code implementation available at ./util/util.py

            Returns
            -------
            str
                Returns a formatted string representing the node and its attributes.
                Used for internal purposes and testing.
            """
            return util.inspect_node(self)

    def add_root(self, key: int):
        """
        Add node at root of tree.

        Parameters
        ----------
        key : int
            Key of root node to be created.
        """
        self.root = BinaryTree.BTNode(key)

    def extend_default(self, data: list[int] = []):
        """
        Extend tree.

        The default method of extending a tree with a list of keys is to call add(key)
        for each key in the list.

        Parameters
        ----------
        data : list[int] = []
            List of keys to extend the tree with.
        """
        for k in data:
            self.add(k)

    def get_default(self, key: int) -> BTNode:
        """
        Get a node by key.

        The default get behaviour searches the tree with preorder priority and returns
        the node if present. Raises a KeyError if node absent.

        Parameters
        ----------
        key : int
            Key to search for

        Returns
        -------
        BTNode
            Node to be returned if found.

        Raises
        ------
        KeyError
            If there are no nodes with the key present in the tree.
        """
        found = None
        for node in self.preorder():
            if node.key == key:
                found = node
        if found is None:
            raise KeyError(f"{key} not in tree")
        return found

    def delete_default(self, key: int):
        """
        Delete a node from the tree.

        The default delete behavior searches the tree for key with preorder priority
        and removes it from it's parent. Note that this will delete the whole subtree.

        Parameters
        ----------
        key : int
            Key of node to be deleted.
        """

        def delete(node, key):
            if node.l:
                if node.l.key == key:
                    node.del_node("l")
                    return
                delete(node.l, key)
            if node.r:
                if node.r.key == key:
                    node.del_node("r")
                    return
                delete(node.r, key)

        if self.root:
            if self.root.key == key:
                self.root = None
                return
            delete(self.root, key)

    def add_breadth_first(self, key: int):
        """
        Insert node.

        This is the default add method for the base class. It creates a new node in
        the place of the first missing space when traversed breadth-first.

        Parameters
        ----------
        key : int
            Key of node to be inserted.
        """
        if not self.root:
            self.add_root(key)
            return
        for node in self.breadth_first():
            if not node.l:
                node.add_node(key, "l")
                return
            if not node.r:
                node.add_node(key, "r")
                return

    def is_perfect(self) -> bool:
        """
        Check if tree is perfect.

        A binary tree is perfect if every internal node has two children and all the
        leaf nodes are on the same level.

        Returns
        -------
        bool
            True if tree satisfies definion of perfect tree.
        """

        def node_is_perfect(node: BTNode) -> bool:
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

    def is_full(self) -> bool:
        """
        Check if tree is full.

        A binary tree is full if every node has either 0 or 2 children.

        Returns
        -------
        bool
            True if tree satisfies definition of full tree.
        """

        def rec_is_full(node: BTNode) -> bool:
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

    def is_complete(self) -> bool:
        """
        Check if tree is complete.

        A binary tree is complete if every space in every level of the tree is filled,
        except possibly the lowest level which must be filled from the left.

        Returns
        -------
        bool
            True if tree satisfies definition of complete tree.
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

    def is_balanced(self) -> bool:
        """
        Check if tree is balanced.

        A binary tree is balanced if the difference between the height of the children
        of each node is no greater than 1 and no less than -1.

        Returns
        -------
        bool
            True if the tree satisfies the definition of a balanced tree.
        """
        if not self.root:
            return True
        for node in self.flatten():
            rh = node.r.get_height() if node.r else -1
            lh = node.l.get_height() if node.l else -1
            if (diff := rh - lh) < -1 or diff > 1:
                return False
        return True

    def breadth_first(self) -> Iterator[BTNode]:
        """
        Breadth-first traversal.

        Returns an iterator which provides all the nodes in the tree from top to
        bottom, left to right.

        Returns
        -------
        Iterator[BTNode]
            Yields all the nodes of the tree in breadth-first priority.
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

    def flatten(self) -> Iterator[BTNode]:
        """
        In-order traversal.

        Returns an iterator which provides all the nodes in the tree in in-order
        priority. In-order priority is left child -> node -> right child.

        Returns
        -------
        Iterator[BTNode]
            Yields all nodes in tree in in-order priority.
        """
        if self.root:

            def rec_flatten(node: BTNode) -> Iterator[BTNode]:
                if node.l:
                    for n in rec_flatten(node.l):
                        yield n
                yield node
                if node.r:
                    for n in rec_flatten(node.r):
                        yield n

            for n in rec_flatten(self.root):
                yield n

    def preorder(self) -> Iterator[BTNode]:
        """
        Pre-order traversal.

        Returns an iterator which provides all the nodes in the tree in preorder
        priority. Preorder priority is node -> left child -> right child.

        Returns
        -------
        Iterator[BTNode]
            Yields all nodes in tree in preorder priority.
        """
        if self.root:

            def rec_preorder(node: BTNode) -> Iterator[BTNode]:
                yield node
                if node.l:
                    for n in rec_preorder(node.l):
                        yield n
                if node.r:
                    for n in rec_preorder(node.r):
                        yield n

            for n in rec_preorder(self.root):
                yield n

    def postorder(self) -> Iterator[BTNode]:
        """
        Post-order traversal.

        Returns an iterator which provides all the nodes in the tree in postorder
        priority. Postorder priority is left child -> right child -> node.

        Returns
        -------
        Iterator[BTNode]
            Yields all nodes in tree in postorder priority.
        """
        if self.root:

            def rec_postorder(node: BTNode) -> Iterator[BTNode]:
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
        """
        Render tree to console.

        Prints a visual representation of the tree to the console. Reccommended for
        use with trees no greater than 31 nodes, depending on the width of the console.

        Implementation logic can be found at ./util/util.py
        """
        print(util.display(self))

    def __str__(self) -> str:
        """
        To string.

        Returns
        -------
        str
            Returns a string representation of the tree.
        """
        return util.display(self)

    def inspect(self) -> str:
        """
        Inspect tree.

        Returns
        -------
        str
            For testing and internal use. Returns a formatted list of the contents of
            the tree.
        """
        return util.inspect(self)
