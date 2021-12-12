"""
This file contains my own versions of all the common data structures which \
I am writing for my own personal study. I'm following the programiz tutorial \
at https://www.programiz.com/dsa
"""

class Stack():
    """
    LIFO Stack.

    This representation of the stack handles push, pop, is_empty, is_full, \
    peek, __str__ and extend methods. For example:

    >>> stack = Stack(max_size=3)
    >>> stack.is_empty()
    True
    >>> stack.push(5)
    >>> print(stack)
    [5]
    >>> stack.extend([7, 9])
    >>> stack.is_full()
    True
    >>> stack.pop()
    9
    >>> print(stack)
    [5, 7]
    >>> stack.peek()
    7
    """
    def __init__(self, data=[], max_size=-1):
        self.max_size = max_size
        self.data = []
        self.extend(data)
    def is_full(self):
        return len(self.data) == self.max_size
    def is_empty(self):
        return len(self.data) == 0
    def push(self, x):
        if self.is_full():
            raise Exception("Stack full, cannot push", x)
        self.data.append(x)
    def pop(self):
        if self.is_empty():
            raise Exception("Stack empty, cannot pop")
        return self.data.pop()
    def peek(self):
        return self.data[-1]
    def extend(self, data):
        for x in data: self.push(x)
    def __str__(self):
        return str(self.data)

class Queue():
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
        for x in arr: self.enqueue(x)
    def __str__(self):
        return str(self.data)
    def __iter__(self):
        return (x for x in self.data)

class CircularQueue():
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
        return (self.head - self.tail) % self.size == 1
    def enqueue(self, x):
        if self.is_full():
            raise Exception("Queue full, cannot enqueue")
        if self.head == -1:
            self.head = self.tail = 0
            self.data[self.tail] = x
        else:
            self.tail = (self.tail + 1) % self.size
            self.data[self.tail] = x
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
        for x in arr: self.enqueue(x)
    def __str__(self):
        return str(self.data)
    def __iter__(self):
        i = self.head
        for x in range(self.size):
            if self.data[i] != None:
                yield self.data[i]
            i = (i + 1) % self.size

class BTNode():
    def __init__(self, value, depth, parent):
        self.value = value
        self.l = self.r = None
        self.depth = depth
        self.parent = parent
    def add(self, value):
        # Adds nodes in a way which tends towards perfect trees such that 
        # as long as nodes are only added and not removed, a tree constructed
        # with this method will always be complete
        if self.l == None:
            self.l = BTNode(value, self.depth + 1, self)
            return self.depth + 1
        elif self.r == None:
            self.r = BTNode(value, self.depth + 1, self)
            return self.depth + 1
        elif self.is_perfect():
            return self.l.add(value)
        elif self.l.is_perfect():
            return self.r.add(value)
        else:
            return self.l.add(value)
    def extend(self, values):
        for v in values:
            self.add(v)
    def get_height(self):
        if self.l == None and self.r == None:
            return 0
        lh = rh = 0
        if self.l != None:
            lh = 1 + self.l.get_height()
        if self.r != None:
            rh = 1 + self.r.get_height()
        return max(lh, rh)
    def is_perfect(self):
        # Height of 0
        if self.l == None and self.r == None:
            return True
        # Only one child
        if self.l == None or self.r == None:
            return False
        # Both children have same height
        if self.l.get_height() == self.get_height() -1 \
                and self.r.get_height() == self.get_height() -1:
            return self.l.is_perfect() and self.r.is_perfect()
        return False
    def is_full(self):
        if self.l == None and self.r == None:
            return True
        if self.l != None and self.r != None:
            return is_f(self.l) and is_f(self.r)
        return False
    def is_complete(self):
        if self.l == None and self.r == None:
            return True
        if self.l == None and self.r != None:
            return False
        rc = self.r.is_complete() if self.r != None else True
        return self.l.is_complete() and rc
    def __str__(self):
        return str(self.value)
    def to_dict(self):
        d = {"v": self.value}
        if self.l != None:
            d["l"] = self.l.to_dict()
        if self.r != None:
            d["r"] = self.r.to_dict()
        return d
    def flatten(self):
        if self.l != None:
            for n in self.l.flatten():
                yield n
        yield self
        if self.r != None:
            for n in self.r.flatten():
                yield n
    def preorder(self):
        yield self
        if self.l != None:
            for n in self.l.preorder():
                yield n
        if self.r != None:
            for n in self.r.preorder():
                yield n
    def postorder(self):
        if self.l != None:
            for n in self.l.postorder():
                yield n
        if self.r != None:
            for n in self.r.postorder():
                yield n
        yield self

def get_levels(node):
    output = [[] for _ in range(node.get_height() + 1)]
    for n in node.flatten():
        output[n.depth].append(n)
    return output

def display_crude(node):
    for level in get_levels(node):
        print(" ".join(str(node) for node in level))

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    tree = BTNode(0, 0, None)
    for x in range(1, 8):
        tree.add(x)
        display_crude(tree)
        print()











