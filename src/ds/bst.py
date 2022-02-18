from __future__ import annotations
from math import ceil
from .bt import BinaryTree


class BinarySearchTree(BinaryTree):
    """
    Binary search tree (bst).

    This implementation of the binary search tree extends the BinaryTree base class.
    The methods add and delete methods provided will guarantee that a tree made with
    them satisfies the definition of a binary search tree: All node keys are sorted in
    order of smallest to largest when the nodes of the tree are traversed in-order.

    Binary search trees are optimised for data lookup speed. If the tree is balanced,
    then the worst case lookup time for a node is O = log(n). If a bst is not balanced,
    this property cannot be guaranteed.

    This implementation includes a balance method, which doubles as an extend method.
    This method simply converts the nodes of the tree into a list, appends the contents
    of the list passed to it, then creates a new bst with the result. This approach
    requires touching every node in the tree (O = n) and is therefore impractical. For
    any practical purposes, a self-balancing tree such as an AVL tree is required (see
    ./avl.py)

    ...

    Methods
    -------
    add_bst(key: int)
        Insert a new node with key into the tree while maintaining bst properties. Does
        not guarantee tree balance.
    balance(data: list[int] = [])
        Converts the nodes of the tree into a sorted list, appends the contents of
        data then creates a new balanced bst from the contents.
    get_bst(key: int)
        Retrieve the node with key if present, raise KeyError if not. Lookup time
        is O = log(n) if the tree is balanced.
    delete_bst(key: int)
        Delete a node from the tree. Does not remove the whole subtree, but rearranges
        the tree to maintain in-order sorted property. Does not guarantee tree balance.
    is_bst() -> bool
        Returns true if all the keys of the nodes of the tree are sorted from smallest
        to largest when traversed in in-order priority.
    """

    def __init__(self, root: BTNode = None, data: list[int] = []):
        """
        __init__.

        Parameters
        ----------
        root : BTNode
            Node to itialise the root of the tree.
        data : list[int]
            List of keys to create initial bst from.
        """
        super().__init__(root=root)
        # Add method aliases
        self.add = self.add_bst
        self.extend = self.balance
        self.delete = self.delete_bst
        self.get = self.get_bst
        # Create initial bst
        self.extend(data=data)

    def add_bst(self, key: int):
        """
        Insert node.

        Insert a new node with key into the tree while maintaining bst properties. Does
        not guarantee tree balance.

        Parameters
        ----------
        key : int
            Key of node to be inserted
        """

        def rec_add(node, key):
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            if key < node.key:
                if node.l:
                    rec_add(node.l, key)
                else:
                    node.add_node(key, "l")
            if key > node.key:
                if node.r:
                    rec_add(node.r, key)
                else:
                    node.add_node(key, "r")

        if not self.root:
            self.add_root(key)
        else:
            rec_add(self.root, key)

    def balance(self, data: list[int] = []):
        """
        Balance the tree.

        Converts the nodes of the tree into a sorted list, appends the contents of
        data then creates a new balanced bst from the contents.

        Parameters
        ----------
        data : list[int]
            A list of nodes to be added to the bst
        """

        old_nodes = [] if not (ar := self.flatten()) else ar
        nodes = sorted(data + [node.key for node in old_nodes])
        if len(nodes) == 0:
            return
        self.root = self.BTNode(nodes.pop(len(nodes) // 2))

        def build(node, keys):
            if (keys_len := len(keys)) == 0:
                return
            left_vals = keys[0 : (half_keys_len := ceil(keys_len / 2))]
            right_vals = keys[half_keys_len:]
            if len(left_vals) > 0:
                node.l = self.BTNode(left_vals.pop(len(left_vals) // 2))
                build(node.l, left_vals)
            if len(right_vals) > 0:
                node.r = self.BTNode(right_vals.pop(len(right_vals) // 2))
                build(node.r, right_vals)

        build(self.root, nodes)

    def get_bst(self, key: int) -> BTNode:
        """
        Get node.

        Retrieve the node with key if present, raise KeyError if not. Lookup time
        is O = log(n) if the tree is balanced.

        Parameters
        ----------
        key : int
            Key to find

        Returns
        -------
        BTNode
            The node to be returned if found.

        Raises
        ------
        KeyError
            If there is no node with the key in the tree.
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

    def delete_bst(self, key: int):
        """
        Delete node from tree.

        Delete a node from the tree. Does not remove the whole subtree, but rearranges
        the tree to maintain in-order sorted property. Does not guarantee tree balance.

        Parameters
        ----------
        key : int
            Key of node to be deleted
        """

        def rec_del(node: BTNode) -> BTNode:
            if key == node.key:
                return get_replacement(node)
            elif node.l and key < node.key:
                node.attach_node(rec_del(node.l), "l")
            elif node.r and key > node.key:
                node.attach_node(rec_del(node.r), "r")
            else:
                raise Exception("Attempted to delete missing key from tree:", key)
            return node

        def get_replacement(node: BTNode) -> BTNode:
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
            # Two children -> Find successor
            # If the nodes right child has no left child, then the nodes right child
            # is it's successor
            if not node.r.l:
                node.r.attach_node(node.l, "l")
                return node.r
            # If the nodes right child has a left child, then we travel down to the
            # left from the nodes right child until we find a node with no left child.
            parent = node.r
            successor = node.r.l
            while successor.l:
                parent = successor
                successor = successor.l
            # Ensure that we save all the children we need to
            parent.attach_node(successor.r, "l")
            successor.attach_node(node.l, "l")
            successor.attach_node(node.r, "r")
            # Return the altered successor
            return successor

        self.root = rec_del(self.root)

    def is_bst(self) -> bool:
        """is_bst.

        Returns true if all the keys of the nodes of the tree are sorted from smallest
        to largest when traversed in in-order priority.

        Returns
        -------
        bool
            True if the tree satisfies the definition of a binary search tree.
        """
        nodes = list(self.flatten())
        return all(nodes[i].key < nodes[i + 1].key for i in range(len(nodes) - 1))
