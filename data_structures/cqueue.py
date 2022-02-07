class CircularQueue:
    """
    FIFO Queue with circular implementation.

    To make the best use of memory, the circular queue reuses the memory at \
    the start of the queue when items overflow the size and there is space. \
    This has the added benefit of bypassing the need to remake the array \
    every time an item is dequeued.

    This implementation is statically sized.

    Supported methods are enqueue, dequeue, is_empty, is_full, peek, extend, \
    __iter__ and __str__. For usage examples, see Queue above

    >>> queue = CircularQueue(size = 3)
    >>> queue.is_empty()
    True
    >>> queue.enqueue(2)
    >>> print(queue)
    [2, None, None]
    >>> queue.extend([4, 6])
    >>> print(queue)
    [2, 4, 6]
    >>> queue.is_full()
    True
    >>> queue.dequeue()
    2
    >>> queue.dequeue()
    4
    >>> queue.enqueue(8)
    >>> print(queue)
    [8, None, 6]
    >>> print(len(queue))
    2
    >>> queue.peek()
    6
    >>> for x in queue: print(x * 2)
    12
    16
    """

    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size
        self.head = self.tail = -1

    def is_empty(self):
        return self.head == -1

    def is_full(self):
        output = (self.head - self.tail) % self.size == 1
        print("Is_full", self.head, self.tail, self.size, output)
        return output

    def enqueue(self, x):
        print("Enqueueing", self, self.head, self.tail, x)
        if self.is_full():
            print("Full", self, self.head, self.tail)
            self.handle_full()
        if self.head == -1:
            self.head = self.tail = 0
            self.data[self.tail] = x
        else:
            self.tail = (self.tail + 1) % self.size
            self.data[self.tail] = x

    def handle_full(self):
        raise Exception("Queue full, cannot enqueue")

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        output = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.size
        return output

    def peek(self):
        return self.data[self.head]

    def extend(self, arr):
        for x in arr:
            self.enqueue(x)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len([x for x in self if x != None])

    def __iter__(self):
        i = self.head
        for x in range(self.size):
            if self.data[i] is not None:
                yield self.data[i]
            i = (i + 1) % self.size
