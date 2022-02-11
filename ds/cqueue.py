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

    def __init__(self, data=[], max_size=8):
        self.max_size = max_size
        self.initialise_empty()
        self.extend(data)

    def is_full(self):
        return (self.tail + 1) % self.max_size == self.head

    def is_empty(self):
        return self.head == -1

    def handle_full(self, x):
        raise Exception("Queue full, cannot enqueue", x)

    def handle_empty(self):
        self.head = self.tail = -1

    def initialise_empty(self):
        self.data = [None] * self.max_size
        self.head = self.tail = -1

    def enqueue(self, x):
        if self.is_full():
            self.handle_full(x)
        if self.tail == -1:
            self.head = self.tail = 0
        else:
            self.tail = (self.tail + 1) % self.max_size
        self.data[self.tail] = x

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot dequeue")
        output = self.data[self.head]
        self.data[self.head] = None
        if self.head == self.tail:
            self.initialise_empty()
        else:
            self.head = (self.head + 1) % self.max_size
        return output

    def peek(self):
        if self.is_empty():
            raise Exception("Queue empty, cannot peek")
        return self.data[self.head]

    def extend(self, data):
        for x in data:
            self.enqueue(x)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        if self.head == -1:
            return 0
        return ((self.tail - self.head) % self.max_size) + 1

    def __iter__(self):
        if self.head != -1:
            i = self.head
            while i != self.tail:
                yield self.data[i]
                i = (i + 1) % self.max_size
