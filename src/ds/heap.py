from .bt import BinaryTree


class Heap:
    def __init__(self, data=[], max_or_min="max"):
        if max_or_min == "max":
            self.compare = lambda a, b: a > b
        if max_or_min == "min":
            self.compare = lambda a, b: a < b
        self.data = data
        self.heapify()

    def heapify(self):
        size = len(self.data)
        if size < 1:
            return

        def rec_heapify(i):
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
                rec_heapify(top)

        last_non_leaf = (size // 2) - 1
        for i in range(last_non_leaf, -1, -1):
            rec_heapify(i)

    def is_heap(self):
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
        tree = BinaryTree(data=self.data)
        tree.display()
