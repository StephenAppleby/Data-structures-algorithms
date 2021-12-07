

# STACK push, pop, is_empty, is_full, peek
class Stack():
    def __init__(self, data=[], max_size=-1):
        if len(data) > max_size and max_size != -1:
            raise Exception("Array size out of bounds")
        self.max_size = max_size
        self.data = data
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
    def __str__(self):
        return str(self.data)

# QUEUE, enqueue, dequeue, is_empty, is_full, peek
class Queue():
    def __init__(self, data=[], max_size=-1):
        if len(data) > max_size and max_size != -1:
            raise Exception("Array size out of bounds")
        self.data = data
        self.max_size = max_size
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
    def __str__(self):
        return str(self.data)

# CIRCULAR QUEUE, enqueue, dequeue, is_empty, is_full, peek, extend
class CircularQueue():
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size
        self.head = self.tail = -1
    def is_empty(self):
        if self.head == -1:
            return True
        return False
    def is_full(self):
        if self.size == 0:
            return True
        if self.head == -1:
            return False
        # something - size maybe
        return self.head + self.tail + 1 == self.size
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
        pass    
    





















