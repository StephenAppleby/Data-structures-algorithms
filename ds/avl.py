from .bt import BinaryTree
from .bst import BinarySearchTree


class AVLTree(BinarySearchTree):
    def __init__(self, **kwargs):
        data = []
        if "data" in kwargs:
            data = kwargs.pop("data")
        super().__init__(**kwargs)
        self.add = self.add_avl
        self.extend = self.extend_default
        self.delete = self.delete_avl
        self.get = self.get_bst
        self.extend(data=data)

    class AVLNode(BinaryTree.BTNode):
        def __init__(self, key=None):
            super().__init__(key)
            self.height = 0

        def left_rotate(self):
            child = self.r
            self.r = child.l
            child.l = self
            self.height = self.get_height()
            child.height = child.get_height()
            return child

        def right_rotate(self):
            child = self.l
            self.l = child.r
            child.r = self
            self.height = self.get_height()
            child.height = child.get_height()
            return child

        def left_right_rotate(self):
            self.l = self.l.left_rotate()
            return self.right_rotate()

        def right_left_rotate(self):
            self.r = self.r.right_rotate()
            return self.left_rotate()

        def balance(self):
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
            self.height = self.get_height()

        def get_height(self):
            lh = self.l.height if self.l else -1
            rh = self.r.height if self.r else -1
            return 1 + max(lh, rh)

        def get_balance_factor(self):
            lh = self.l.height if self.l else -1
            rh = self.r.height if self.r else -1
            return lh - rh

        def add_node(self, key, side):
            if side == "l":
                self.l = AVLTree.AVLNode(key)
            if side == "r":
                self.r = AVLTree.AVLNode(key)
            self.set_height()

        def attach_node(self, node, side):
            super().attach_node(node, side)
            self.set_height()

        def del_node(self, side):
            super().del_node(side)
            self.set_height()

    def add_root(self, key):
        self.root = AVLTree.AVLNode(key)

    def add_avl(self, key):
        def rec_add(node, key):
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            if key < node.key:
                if node.l:
                    node.attach_node(rec_add(node.l, key), "l")
                else:
                    node.add_node(key, "l")
            if key > node.key:
                if node.r:
                    node.attach_node(rec_add(node.r, key), "r")
                else:
                    node.add_node(key, "r")
            return node.balance()

        if not self.root:
            self.add_root(key)
        else:
            self.root = rec_add(self.root, key).balance()

    def delete_avl(self, key):
        def rec_del(node):
            if key == node.key:
                return get_replacement(node)
            elif node.l and key < node.key:
                node.attach_node(rec_del(node.l), "l")
            elif node.r and key > node.key:
                node.attach_node(rec_del(node.r), "r")
            else:
                raise Exception("Attempted to delete missing key from tree:", key)
            return node.balance()

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
                return node.r.balance()
            # Successor is not node.r
            link, successor = get_successor(node.r)
            successor.attach_node(node.l, "l")
            successor.attach_node(link, "r")
            return successor.balance()

        def get_successor(parent):
            successor = parent.l
            if successor.l:
                link, got = get_successor(successor)
                parent.attach_node(link, "l")
                return (parent.balance(), got)
            else:
                parent.attach_node(successor.r, "l")
                return (parent.balance(), successor)

        self.root = rec_del(self.root)
