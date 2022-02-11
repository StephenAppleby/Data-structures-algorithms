from .bt import BinaryTree


class Heap(BinaryTree):
    def __init__(self, max_or_min="max", **kwargs):
        self.max_or_min = max_or_min
        if max_or_min == "max":
            self.compare = lambda a, b: a > b
        if max_or_min == "min":
            self.compare = lambda a, b: a < b
        super().__init__(**kwargs)
        self.heapify()

    def heapify(self):
        def swap(parent, child, side):
            child_l = child.l
            child_r = child.r
            if side == "l":
                child.attach_node(parent.r, "r")
                parent.attach_node(child_l, "l")
                parent.attach_node(child_r, "r")
                child.attach_node(rec_heapify(parent), "l")
            if side == "r":
                child.attach_node(parent.l, "l")
                parent.attach_node(child_l, "l")
                parent.attach_node(child_r, "r")
                child.attach_node(rec_heapify(parent), "r")
            return child

        def rec_heapify(node):
            children = ""
            if node.l:
                children += "l"
            if node.r:
                children += "r"
            if "l" in children:
                node.attach_node(rec_heapify(node.l), "l")
            if "r" in children:
                node.attach_node(rec_heapify(node.r), "r")
            if children == "":
                return node
            if children == "lr":
                to_swap = (
                    (node.l, "l") if self.compare(node.l, node.r) else (node.r, "r")
                )
                if not self.compare(node, to_swap[0]):
                    return swap(node, *to_swap)
                return node
            if children == "l":
                if not self.compare(node, node.l):
                    return swap(node, node.l, "l")
                return node
            # A complete tree will have no nodes with a right child but no left

        self.root = rec_heapify(self.root)

    def is_heap(self):
        for node in self.preorder():
            if node.l:
                if self.max_or_min == "max" and node.key < node.l.key:
                    return False
                if self.max_or_min == "min" and node.key > node.l.key:
                    return False
            if node.r:
                if self.max_or_min == "max" and node.key < node.r.key:
                    return False
                if self.max_or_min == "min" and node.key > node.r.key:
                    return False
        return True
