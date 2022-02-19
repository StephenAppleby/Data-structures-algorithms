from __future__ import annotations
from .bt import BinaryTree
from .bst import BinarySearchTree


class AVLTree(BinarySearchTree):
    """
    AVLTree.

    A self balancing implementation of the binary search tree.

    Example:
    >>> avl = AVLTree(data=[x for x in range(9)])
    >>> avl.display()
                   3
           ┌───────┴───────┐
           1               5
       ┌───┴───┐       ┌───┴───┐
       0       2       4       7
                             ┌─┴─┐
                             6   8
    >>> avl.delete(3)
    >>> avl.display()
                   4
           ┌───────┴───────┐
           1               7
       ┌───┴───┐       ┌───┴───┐
       0       2       5       8
                       └─┐
                         6
    >>> avl.extend([x for x in range(10, 15)])
    >>> avl.display()
                   7
           ┌───────┴───────┐
           4              12
       ┌───┴───┐       ┌───┴───┐
       1       5      10      13
     ┌─┴─┐     └─┐   ┌─┴─┐     └─┐
     0   2       6   8  11      14

    ...

    Attributes
    ---------
    AVLNode : class
        A nested class representing a node of an AVL tree
    root : AVLNode
        The root node of the AVL tree

    Methods
    -------
    add_root(key: int)
        Create a new AVLNode with key and assign as root of tree
    add_avl(key: int)
        Insert a new AVLNode into the tree while preserving balance and binary search
        properties
    delete_avl(key: int)
        Remove an AVLNode from the tree while preserving balance and binary search
        properties
    """

    def __init__(self, root: AVLNode = None, data: list[int] = []):
        """__init__.

        Parameters
        ----------
        root : AVLNode
            Root node
        data : list[int]
            data
        """
        super().__init__(root=root)
        # Initialise default aliases using sub-class specific methods
        self.add = self.add_avl
        self.extend = self.extend_default
        self.delete = self.delete_avl
        self.get = self.get_bst
        # Initialise data
        self.extend(data=data)

    class AVLNode(BinaryTree.BTNode):
        """
        AVLNode.

        A subclass of BinaryTree.BTNode.

        ...

        Attributes
        ---------
        height : int
            Max distance between this node and a child leaf node

        Methods
        -------
        left_rotate() -> AVLNode
            Performs a left rotation on the subtree with the node called as root.
            Returns the new root of the subtree.
        right_rotate() -> AVLNode
            Performs a right rotation on the subtree with the node called as root.
            Returns the new root of the subtree.
        left_right_rotate() -> AVLNode
            Performs a left-right rotation on the subtree with the node called as root.
            Returns the new root of the subtree.
        right_left_rotate() -> AVLNode
            Performs a right-left rotation on the subtree with the node called as root.
            Returns the new root of the subtree.
        balance() -> AVLNode
            Calculates the balance factor of the node by calling get_balance_factor
            and performs a rotation on the node as needed to restore balance. Returns
            the new root of the subtree.
        set_height()
            Sets the height of the node using get_height.
        get_height() -> int
            Returns the height of the node by getting the max height of it's children
            and adding 1.
        get_balance_factor() -> int
            Returns the balance factor of the node by comparing the height of it's
            children.
        add_node(key: int, side: str)
            Overrides parent implementation to add AVLNodes instead of BTNodes.
        attach_node(node: AVLNode, side: str)
            Extends parent implementation to set the height of the node after attaching.
        del_node(side: str)
            Extends parent implementation to set the height of the node after deleting.
        """

        def __init__(self, key: int = None):
            """__init__.

            Extends parent implementation to initialise node height as 0

            Parameters
            ----------
            key : int
                key
            """
            super().__init__(key)
            self.height = 0

        def left_rotate(self) -> AVLNode:
            """
            Left rotate.

            Performs a left rotation on the subtree with the node called as root.
            Returns the new root of the subtree.

            Returns
            -------
            AVLNode

            """
            child = self.r
            self.r = child.l
            child.l = self
            self.height = self.get_height()
            child.height = child.get_height()
            return child

        def right_rotate(self) -> AVLNode:
            """
            Right rotate.

            Performs a right rotation on the subtree with the node called as root.
            Returns the new root of the subtree.

            Returns
            -------
            AVLNode

            """
            child = self.l
            self.l = child.r
            child.r = self
            self.height = self.get_height()
            child.height = child.get_height()
            return child

        def left_right_rotate(self) -> AVLNode:
            """
            Left-right rotate.

            Performs a left-right rotation on the subtree with the node called as root.
            Returns the new root of the subtree.

            Returns
            -------
            AVLNode

            """
            self.l = self.l.left_rotate()
            return self.right_rotate()

        def right_left_rotate(self) -> AVLNode:
            """
            Right-left rotate.

            Performs a right-left rotation on the subtree with the node called as root.
            Returns the new root of the subtree.

            Returns
            -------
            AVLNode

            """
            self.r = self.r.right_rotate()
            return self.left_rotate()

        def balance(self) -> AVLNode:
            """
            Balance.

            Calculates the balance factor of the node by calling get_balance_factor
            and performs a rotation on the node as needed to restore balance. Returns
            the new root of the subtree.

            Returns
            -------
            AVLNode

            """
            bal_fac = self.get_balance_factor()
            if bal_fac > 1:
                if self.l.get_balance_factor() >= 0:
                    return self.right_rotate()
                else:
                    return self.left_right_rotate()
            if bal_fac < -1:
                if self.r.get_balance_factor() <= 0:
                    return self.left_rotate()
                else:
                    return self.right_left_rotate()
            return self

        def set_height(self):
            """
            Set height.

            Sets the height of the node using get_height.
            """
            self.height = self.get_height()

        def get_height(self) -> int:
            """
            Get height.

            Returns the height of the node by getting the max height of its children
            and adding 1.


            Returns
            -------
            int

            """
            lh = self.l.height if self.l else -1
            rh = self.r.height if self.r else -1
            return 1 + max(lh, rh)

        def get_balance_factor(self) -> int:
            """
            Get balance factor.

            Returns the balance factor of the node by comparing the height of its
            children.

            Returns
            -------
            int

            """
            lh = self.l.height if self.l else -1
            rh = self.r.height if self.r else -1
            return lh - rh

        def add_node(self, key: int, side: str):
            """
            Add node.

            Overrides parent implementation to add AVLNodes instead of BTNodes.

            Parameters
            ----------
            key : int
                key
            side : str
                side
            """
            if side == "l":
                self.l = AVLTree.AVLNode(key)
            if side == "r":
                self.r = AVLTree.AVLNode(key)
            self.set_height()

        def attach_node(self, node: AVLNode, side: str):
            """
            Attach node.

            Extends parent implementation to set the height of the node after attaching.

            Parameters
            ----------
            node : AVLNode
                node
            side : str
                side
            """
            super().attach_node(node, side)
            self.set_height()

        def del_node(self, side: str):
            """
            Delete node.

            Extends parent implementation to set the height of the node after deleting.

            Parameters
            ----------
            side : str
                side
            """
            super().del_node(side)
            self.set_height()

    def add_root(self, key: int):
        """
        Add root.

        Create a new AVLNode with key and assign as root of tree.

        Parameters
        ----------
        key : int
            key
        """
        self.root = AVLTree.AVLNode(key)

    def add_avl(self, key: int):
        """
        Add a node to the tree.

        Insert a new AVLNode into the tree while preserving balance and binary search
        properties.

        Parameters
        ----------
        key : int
            key
        """

        def rec_add(node: AVLNode) -> AVLNode:
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            # Search left
            if key < node.key:
                if node.l:
                    # Search down to the left child then replace the left child
                    # with the altered and balanced node returned
                    node.attach_node(rec_add(node.l), "l")
                else:
                    # Insert node
                    node.add_node(key, "l")
            # Search right
            if key > node.key:
                if node.r:
                    # Search down to the right child then replace the right child
                    # with the altered and balanced node returned
                    node.attach_node(rec_add(node.r), "r")
                else:
                    # Insert node
                    node.add_node(key, "r")
            # Send the altered and balanced node back up
            return node.balance()

        if not self.root:
            self.add_root(key)
        else:
            # Perform the recursive function defined above to add a node then replace
            # the root with the result
            self.root = rec_add(self.root).balance()

    def delete_avl(self, key: int):
        """
        Delete node from tree.

        Remove an AVLNode from the tree while preserving balance and binary search
        properties.

        Parameters
        ----------
        key : int
            key
        """

        def rec_del(node: AVLNode) -> AVLNode:
            if key == node.key:
                # Found the node to be deleted -> return the node to replace it if any
                return get_replacement(node)
            elif node.l and key < node.key:
                # Search the left child and then replace the left child with the
                # altered and balanced result
                node.attach_node(rec_del(node.l), "l")
            elif node.r and key > node.key:
                # Search the left child and then replace the left child with the
                # altered and balanced result
                node.attach_node(rec_del(node.r), "r")
            else:
                raise Exception("Attempted to delete missing key from tree:", key)
            # Return the altered and balanced node
            return node.balance()

        def get_replacement(node: AVLNode) -> AVLNode:
            # Expects to receive a node which is to be replaced
            # Determine which children are present
            kids = ""
            if node.l:
                kids += "l"
            if node.r:
                kids += "r"
            # No children -> Simply delete the node
            if kids == "":
                return None
            # One child -> Simply return the child to replace it
            if kids == "l":
                return node.l
            if kids == "r":
                return node.r
            # Two children -> Find the successor
            # If the nodes right child has no left child, then the nodes right child
            # is it's successor
            if not node.r.l:
                node.r.attach_node(node.l, "l")
                return node.r.balance()
            # If the nodes right child has a left child, then we need to find the
            # successor and bring it up. While doing this, we will alter the subtree
            # with the right child as root, so we get that and replace the right child
            # with it when we're done
            link, successor = get_successor(node.r)
            # Give the successor the nodes children then balance and return it
            successor.attach_node(node.l, "l")
            successor.attach_node(link, "r")
            return successor.balance()

        def get_successor(parent: AVLNode) -> tuple[AVLNode, AVLNode]:
            # To find the successor of a node to be deleted, we search down the left
            # side until we find a node with no left child
            successor = parent.l
            if successor.l:
                # If there is a left child, keep searching and replace the left child
                # with the altered and balanced result
                link, got = get_successor(successor)
                parent.attach_node(link, "l")
                # Return this node and the successor
                return (parent.balance(), got)
            else:
                # parent has no left child and we have found the successor. Save it's
                # right child if it has one by attaching it to the parent's left, then
                # return the altered and balanced parent along with the successor
                parent.attach_node(successor.r, "l")
                return (parent.balance(), successor)

        # Perform the recursive deletion function defined above on the root of the
        # tree then replace the root with the altered and balanced result
        self.root = rec_del(self.root)
