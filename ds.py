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
        return (self.head - self.tail) % self.size == 1
    def enqueue(self, x):
        if self.is_full():
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
        for x in arr: self.enqueue(x)
    def __str__(self):
        return str(self.data)
    def __len__(self):
        return len([x for x in self if x != None])
    def __iter__(self):
        i = self.head
        for x in range(self.size):
            if self.data[i]:
                yield self.data[i]
            i = (i + 1) % self.size

class DCQueue(CircularQueue):
    """Dynamic implementation of CircularQueue.

    >>> dcqueue = DCQueue(size=3)
    >>> dcqueue.enqueue(3)
    >>> print(dcqueue)
    [3, None, None]
    >>> dcqueue.extend([x for x in range(4)])
    >>> print(dcqueue)
    [3, 0, 1, 2, 3, None]
    """
    def handle_full(self):
        old_data = []
        while len(self) > 0:
            old_data.append(self.dequeue())
        self.size *= 2
        self.data = [None] * self.size
        self.head = self.tail = -1
        for d in old_data:
            self.enqueue(d)

class BTNode():
    def __init__(self, value, depth=0, parent=None):
        self.value = value
        self.l = self.r = None
        self.depth = depth
        self.parent = parent
    def add(self, value):
        for node in self.breadth_first():
            if not node.l:
                node.l = BTNode(value, depth=node.depth + 1, parent=node)
                return node.depth + 1
            if not node.r:
                node.r = BTNode(value, depth=node.depth + 1, parent=node)
                return node.depth + 1
    def add_l(self, value):
        if not self.l:
            self.l = BTNode(value, depth=self.depth + 1, parent=self)
            return self.depth + 1
        return self.l.add_l(value)
    def add_r(self, value):
        if not self.r:
            self.r = BTNode(value, depth=self.depth + 1, parent=self)
            return self.depth + 1
        return self.r.add_r(value)
    def extend(self, values):
        for v in values:
            self.add(v)
    def get_height(self):
        if not self.l and not self.r:
            return 0
        lh = rh = 0
        if self.l:
            lh = 1 + self.l.get_height()
        if self.r:
            rh = 1 + self.r.get_height()
        return max(lh, rh)
    def is_perfect(self):
        # Height of 0
        if not self.l and not self.r:
            return True
        # Only one child
        if not self.l or not self.r:
            return False
        # Both children have same height
        if self.l.get_height() == self.get_height() -1 \
                and self.r.get_height() == self.get_height() -1:
            return self.l.is_perfect() and self.r.is_perfect()
        # Default case
        return False
    def is_full(self):
        if not self.l and not self.r:
            return True
        if self.l and self.r:
            return is_f(self.l) and is_f(self.r)
        return False
    def is_complete(self):
        if not self.l and not self.r:
            return True
        if not self.l and self.r:
            return False
        rc = self.r.is_complete() if self.r else True
        return self.l.is_complete() and rc
    def __str__(self):
        return str(self.value)
    def to_dict(self):
        d = {"v": self.value}
        if self.l:
            d["l"] = self.l.to_dict()
        if self.r:
            d["r"] = self.r.to_dict()
        return d
    def breadth_first(self):
        queue = DCQueue()
        yield self
        if self.l:
            queue.enqueue(self.l)
        if self.r:
            queue.enqueue(self.r)
        while len(queue) > 0:
            node = queue.dequeue()
            yield node
            if node.l:
                queue.enqueue(node.l)
            if node.r:
                queue.enqueue(node.r)
    def flatten(self):
        if self.l:
            for n in self.l.flatten():
                yield n
        yield self
        if self.r:
            for n in self.r.flatten():
                yield n
    def preorder(self):
        yield self
        if self.l:
            for n in self.l.preorder():
                yield n
        if self.r:
            for n in self.r.preorder():
                yield n
    def postorder(self):
        if self.l:
            for n in self.l.postorder():
                yield n
        if self.r:
            for n in self.r.postorder():
                yield n
        yield self
    def fill(self, value):
        while not self.is_perfect():
            self.add(value)
    def get_levels(self):
        output = [[] for _ in range(self.get_height() + 1)]
        for n in self.flatten():
            output[n.depth].append(n)
        return output
    def display_crude(self):
        for level in self.get_levels():
            print(" ".join(str(node) for node in level))
    def copy(self):
        # Returns a shallow copy of the node
        def copy_children(original_node, copy_node):
            if original_node.l:
                copy_node.l = BTNode(
                        original_node.l.value,
                        depth=copy_node.depth + 1,
                        parent=copy_node)
                copy_children(original_node.l, copy_node.l)
            if original_node.r:
                copy_node.r = BTNode(
                        original_node.r.value,
                        depth=copy_node.depth + 1,
                        parent=copy_node
                        )
                copy_children(original_node.r, copy_node.r)
        c = BTNode(self.value)
        copy_children(self, c)
        return c
    def display(self):
        copy_with_gaps = self.copy()
        copy_with_gaps.fill(None)
        levels = copy_with_gaps.get_levels()
        for level, nodes in enumerate(levels):
            pad = " "
            row = len(levels) - (level + 1)
            if row != 0:
                pad = " " * ((((2 ** row) - 1) * 3) + (2 ** row))
            half_pad = pad[:len(pad) // 2]
            output = half_pad
            formatted_values = (f"{str(n):^3}" if n.value != None else "   " 
                    for n in nodes)
            output += pad.join(formatted_values)
            print(output)
            if row != 0:
                # ┘ = "\u2518"
                # └ = "\u2514"
                # ┴ = "\u2534"
                # ─ = "\u2500"
                # ┌ = "\u250C"
                # ┐ = "\u2510"
                pad_next = " "
                row -= 1
                if row == -1: row = 0
                if row != 0:
                    pad_next = " " * ((((2 ** row) - 1) * 3) + (2 ** row))
                half_pad_next_len = len(pad_next[:len(pad_next) // 2])
                pipes = half_pad_next_len * " "
                for node in nodes:
                    if node.l.value:
                        pipes += " " + '┌' + '─'
                        pipes += half_pad_next_len * '─'
                    else:
                        pipes += "   "
                        pipes += half_pad_next_len * " "
                    if node.l.value and not node.r.value:
                        pipes += '┘'
                    if node.l.value and node.r.value:
                        pipes += '┴'
                    if not node.l.value and node.r.value:
                        pipes += '└'
                    if not node.l.value and not node.r.value:
                        pipes += " "
                    if node.r.value:
                        pipes += half_pad_next_len * '─'
                        pipes += '─' + '┐' + " "
                    else:
                        pipes += half_pad_next_len * " "
                        pipes += "   "
                    pipes += pad_next
                print(pipes)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    tree = BTNode(0)
    tree.extend([x for x in range(1, 31)])
    tree.l.r = None
    tree.r.l.r = None
    tree.r.l.l.l = None
    tree.display()
    print()
    tree2 = BTNode("A")
    tree2.extend("BC")
    tree2.l.add_r("D")
    tree2.r.add_l("E")
    tree2.display()








