from .cqueue import CircularQueue


class DynamicCircularQueue(CircularQueue):
    """Dynamic implementation of CircularQueue.

    >>> dcqueue = DCQueue(size=3)
    >>> dcqueue.enqueue(3)
    >>> print(dcqueue)
    [3, None, None]
    >>> dcqueue.extend([x for x in range(4)])
    >>> print(dcqueue)
    [3, 0, 1, 2, 3, None]
    """

    def __init__(self, data=[]):
        super().__init__(data=data, max_size=8)

    def handle_full(self, x):
        old_data = []
        old_max = self.max_size
        while len(self) > 0:
            old_data.append(self.dequeue())
        self.max_size = old_max * 2
        self.data = [None] * self.max_size
        self.head = self.tail = -1
        for d in old_data:
            self.enqueue(d)

    def initialise_empty(self):
        self.max_size = 8
        self.data = [None] * self.max_size
        self.head = self.tail = -1
