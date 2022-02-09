from math import ceil
from .bt import BinaryTree


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
                    node.add_node(key, "l")
                    return node.l
            if key > node.key:
                if node.r:
                    return rec_add(node.r, key)
                else:
                    node.add_node(key, "r")
                    return node.r

        if not self.root:
            self.add_root(key)
            return self.root
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
        self.root = self.BTNode(nodes.pop(len(nodes) // 2))

        def build(node, keys):
            if (vals_len := len(keys)) == 0:
                return
            left_vals = keys[0 : (half_vals_len := ceil(vals_len / 2))]
            right_vals = keys[half_vals_len:]
            if len(left_vals) > 0:
                node.l = self.BTNode(left_vals.pop(len(left_vals) // 2))
                build(node.l, left_vals)
            if len(right_vals) > 0:
                node.r = self.BTNode(right_vals.pop(len(right_vals) // 2))
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

        def rec_del(node):
            if key == node.key:
                return get_replacement(node)
            elif node.l and key < node.key:
                node.attach_node(rec_del(node.l), "l")
            elif node.r and key > node.key:
                node.attach_node(rec_del(node.r), "r")
            else:
                raise Exception("Attempted to delete missing key from tree:", key)
            return node

        def get_replacement(node):
            # Determine which children are present
            kids = ""
            if node.l:
                kids += "l"
            if node.r:
                kids += "r"
            # No children
            if kids == "":
                return None
            # One child
            if kids == "l":
                return node.l
            if kids == "r":
                return node.r
            # Two children -> Find successor
            # Successor is node.r
            if not node.r.l:
                node.r.attach_node(node.l, "l")
                return node.r
            # Successor is not node.r
            parent = node.r
            successor = node.r.l
            while successor.l:
                parent = successor
                successor = successor.l
            # Ensure that we save all the children we need to
            parent.attach_node(successor.r, "l")
            successor.attach_node(node.l, "l")
            successor.attach_node(node.r, "r")
            return successor

        self.root = rec_del(self.root)

    def is_bst(self):
        """
        Returns True if self satisfies the definition of a binary search tree.
        """
        nodes = list(self.flatten())
        return all(nodes[i].key < nodes[i + 1].key for i in range(len(nodes) - 1))
