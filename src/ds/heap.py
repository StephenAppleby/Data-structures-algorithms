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
        for i in range(size - 1, -1, -1):
            top = i
            l = (2 * i) + 1
            r = (2 * i) + 2
            if l < size and not self.compare(self.data[i], self.data[l]):
                top = l
            if r < size and not self.compare(self.data[i], self.data[r]):
                top = r
            if top != i:
                self.data[i], self.data[top] = self.data[top], self.data[i]
                # HEAPIFY BAMBAMBAM
