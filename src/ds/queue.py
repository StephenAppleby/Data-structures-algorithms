class Queue:
    """
    FIFO Queue.

    This representation of the queue handles enqueue, dequeue, is_empty, \
    is_full, peek, extend, __str__ and __iter__ methods. For example:

    >>> queue = Queue(max_size = 3)
    >>> queue.is_empty()
    True
    >>> queue.enqueue(2)
    >>> print(queue)
    [2]
    >>> queue.extend([4, 6])
    >>> print(queue)
    [2, 4, 6]
    >>> queue.is_full()
    True
    >>> queue.dequeue()
    2
    >>> print(queue)
    [4, 6]
    >>> queue.peek()
    4
    >>> for x in queue: print(x * 2)
    8
    12
    """

    def __init__(self, data=[], max_size=-1):
        self.data = []
        self.max_size = max_size
        self.extend(data)

    def is_empty(self):
        return len(self.data) == 0

    def is_full(self):
        return len(self.data) == self.max_size

    def enqueue(self, x):
        if self.is_full():
            raise Exception("Queue full, cannot enqueue", x)
        self.data.append(x)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        return self.data.pop(0)

    def peek(self):
        return self.data[0]

    def extend(self, arr):
        for x in arr:
            self.enqueue(x)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        return (x for x in self.data)
