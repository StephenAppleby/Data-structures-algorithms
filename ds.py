"""
This file contains my own versions of all the common data structures which \
I am writing for my own personal study. I'm following the programiz tutorial \
at https://www.programiz.com/dsa
"""

import util
from math import ceil

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
    """
    Recursive binary tree base class.

    This base class implements a breadth first add method which adds the new
    node at the first location in left -> right, top -> bottom order. This
    leads to the simple creation of perfect trees. Classes which extend this
    base class will define their own add methods. The extend method uses the
    class specific add method to add multiple nodes at once.

    The default deletion method assigns the node it is called on to None. This 
    ensures that the parent of the child deleted has None as a child instead of 
    removing it's child attribute, which would happen with del self. Classes 
    that extend BTNode will implement their own deletion methods 
    as appropriate.

    Basic usage:
    >>> tree = BTNode(data=[x for x in range(7)])
    >>> print(tree)
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6
    >>> tree.r.delete()
    >>> print(tree)
           0
       ┌───┘
       1
     ┌─┴─┐
     3   4
    >>> tree.add(2)
    1
    >>> print(tree)
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐
     3   4
    >>> tree.extend([5, 6])
    >>> print(tree)
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6
    """
    def __init__(self, value=None, data=None, side=None, depth=0, parent=None):
        self.l = self.r = None
        self.depth = depth
        self.parent = parent
        self.side = side
        self.set_defaults()
        if value != None:
            self.value = value
            if data:
                self.extend(data)
        elif data:
            self.value = data[0]
            self.extend(data[1:])
        else:
            self.value = None
    def set_defaults(self):
        """
        Assign class specific insertion and deletion methods.

        This method is called during __init__(). Classes which inherit this
        base class can override this method to set the default insertion and
        deletion behaviour to whatever is appropriate.
        """
        self.add = self.add_breadth_first
        self.delete = self.delete_default
        self.extend = self.extend_default
    def add_breadth_first(self, value):
        """
        Default insertion method for binary trees.

        Inserts a node into the first available place using breadth-first
        search.

        All insertion methods return the depth of the node inserted

        >>> tree = BTNode(0)
        >>> for x in range(1, 5):
        ...     tree.add(x)
        ...     print(tree)
        1
           0
         ┌─┘
         1
        1
           0
         ┌─┴─┐
         1   2
        2
               0
           ┌───┴───┐
           1       2
         ┌─┘
         3
        2
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4
        
        """
        for node in self.breadth_first():
            if not node.l:
                node.l = BTNode(
                        value, 
                        depth=node.depth + 1, 
                        side='l', 
                        parent=node)
                return node.depth + 1
            if not node.r:
                node.r = BTNode(
                        value, 
                        depth=node.depth + 1, 
                        side='r', 
                        parent=node)
                return node.depth + 1
    def add_l(self, value):
        """
        Manually insert a node to the left of self.

        This convenience method is primarily for testing. You generally won't
        be adding elements to a binary tree by hand.
        """
        if not self.l:
            self.l = BTNode(
                    value, 
                    depth=self.depth + 1, 
                    side='l',
                    parent=self)
            return self.depth + 1
        return self.l.add_l(value)
    def add_r(self, value):
        """
        Manually insert a node to the right of self.

        This convenience method is primarily for testing. You generally won't
        be adding elements to a binary tree by hand.
        """
        if not self.r:
            self.r = BTNode(
                    value, 
                    depth=self.depth + 1, 
                    side='r', 
                    parent=self)
            return self.depth + 1
        return self.r.add_r(value)
    def extend_default(self, values):
        """
        Add each value in values to the tree in sequence.

        This method utilises the .add method, meaning that as long as the
        binary tree class which is inheriting this base class has properly
        initialised it's own .add method, .extend will work in every case.

        Example using the default breadth-first add method:
        >>> tree = BTNode(0)
        >>> tree.extend([x for x in range(1, 7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        """
        for v in values:
            self.add(v)
    def delete_default(self):
        if self.side == 'l':
            self.parent.l = None
        if self.side == 'r':
            self.parent.r = None
    def get_height(self):
        """
        Returns maximum distance from self to a leaf (external) node.

        Visits every child node recursively to find the maximum distance. This
        approach calculates the height when needed instead of storing the
        height of a node as an attribute. This is because the height of a node
        can change dynamically when children are added or deleted. While this
        could be handled and height values recalculated every time a node is
        inserted or deleted, this approach seems simpler.

        >>> tree = BTNode(data=[x for x in range(5)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4
        >>> tree.get_height()
        2
        >>> tree.r.get_height()
        0
        >>> tree.l.get_height()
        1
        """
        if not self.l and not self.r:
            return 0
        lh = rh = 0
        if self.l:
            lh = 1 + self.l.get_height()
        if self.r:
            rh = 1 + self.r.get_height()
        return max(lh, rh)
    def is_perfect(self):
        """
        Returns true if self satisfies the definition of a perfect binary tree.

        A perfect binary tree is any binary tree where each internal node has
        exactly two children and each external node has the same depth.

        >>> tree = BTNode(data=[x for x in range(6)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┘
         3   4   5
        >>> tree.is_perfect()
        False
        >>> tree.add(6)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.is_perfect()
        True
        """
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
        """
        Returns true if self is a full binary tree.

        A full binary is defined as any tree in which every node has either
        two or no children.

        >>> tree = BTNode(data=[0, 1, 2])
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        >>> tree.is_full()
        True
        >>> tree.add(3)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┘
         3
        >>> tree.is_full()
        False
        >>> tree.add(4)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4
        >>> tree.is_full()
        True
        """
        # No children
        if not self.l and not self.r:
            return True
        # 2 children
        if self.l and self.r:
            return self.l.is_full() and self.r.is_full()
        # Default case: 1 child
        return False
    def is_complete(self):
        """
        Returns true if self is a complete binary tree.

        A tree is defined as complete if each level of the tree is full except
        possibly the last level, which must be filled from the left. A tree
        which is constructed only with .add_breadth_first with no nodes
        removed will always be complete.

        >>> tree = BTNode(data=[x for x in range(6)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┘
         3   4   5
        >>> tree.is_complete()
        True
        >>> tree.r.add_r(6)
        2
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.is_complete()
        True
        >>> tree.r.l.delete()
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐     └─┐
         3   4       6
        >>> tree.is_complete()
        False
        >>> tree.r.delete()
        >>> print(tree)
               0
           ┌───┘
           1
         ┌─┴─┐
         3   4
        >>> tree.is_complete()
        False
        """
        # Nodes in a perfect tree when iterated over breadth-first will all
        # have 2 children (internal) until the last or second last level. After
        # finding a node with one (left) or zero children, every following node
        # will have no children.

        # Track state
        state = "internal"
        # Iterate over nodes breadth-first
        for node in self.breadth_first():
            # Only right child
            if node.r and not node.l:
                return False
            if state == "internal":
                # One or zero children -> change state
                if not node.r:
                    state = "external"
                    continue
            if state == "external":
                # Any child
                if node.r or node.l:
                    return False
        return True
    def is_balanced(self):
        """
        Returns True if self is a balanced binary tree.

        A binary tree is defined as balanced if the difference in height of 
        each child of each node is no more than 1. Height is defined as the
        maximum distance to a leaf (external) node where leaf nodes have a
        height of 0.

        >>> tree = BTNode(data=[x for x in range(5)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐
         3   4

        The left subtree of the root has a height of 1. The right subtree
        is a leaf and so has a height of 0. Therefore it is considered 
        balanced.

        >>> tree.is_balanced()
        True
        >>> tree.r.delete()
        >>> print(tree)
               0
           ┌───┘
           1
         ┌─┴─┐
         3   4

        This time, the right subtree of the root doesn't exist and so is
        considered to have a height of -1. The difference between -1 and 1 is
        greater than 1, therefore this tree is not balanced.

        >>> tree.is_balanced()
        False
        """
        for node in self.flatten():
            rh = node.r.get_height() if node.r else -1
            lh = node.l.get_height() if node.l else -1
            if (diff := rh - lh) < -1 or diff > 1:
                return False
        return True
    def __str__(self):
        """
        Renders to console in a readable format.

        For more information, see util.display
        """
        return util.display(self)
    def breadth_first(self):
        """
        Returns a left -> right, top -> bottom iterator.

        This iteration method, while slightly more complex than preorder,
        inorder and postorder operations, is needed for binary search tree and
        complete tree operations.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.value for node in tree.breadth_first())
        [0, 1, 2, 3, 4, 5, 6]
        """
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
        """
        Returns an inorder iterator for the children of self.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.value for node in tree.flatten())
        [3, 1, 4, 0, 5, 2, 6]
        """
        if self.l:
            for n in self.l.flatten():
                yield n
        yield self
        if self.r:
            for n in self.r.flatten():
                yield n
    def preorder(self):
        """
        Returns a preorder iterator for the children of self.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.value for node in tree.preorder())
        [0, 1, 3, 4, 2, 5, 6]
        """
        yield self
        if self.l:
            for n in self.l.preorder():
                yield n
        if self.r:
            for n in self.r.preorder():
                yield n
    def postorder(self):
        """
        Returns a postorder iterator for the children of self.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> list(node.value for node in tree.postorder())
        [3, 4, 1, 5, 6, 2, 0]
        """
        if self.l:
            for n in self.l.postorder():
                yield n
        if self.r:
            for n in self.r.postorder():
                yield n
        yield self
    def fill(self, value):
        """
        Adds nodes to self until perfect.
        
        Assigns the value argument as the value for each node added this way.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> tree.l.delete()
        >>> print(tree)
               0
               └───┐
                   2
                 ┌─┴─┐
                 5   6
        
        >>> tree.fill(7)
        >>> print(tree)
               0
           ┌───┴───┐
           7       2
         ┌─┴─┐   ┌─┴─┐
         7   7   5   6
        """
        while not self.is_perfect():
            self.add_breadth_first(value)
    def get_levels(self):
        """
        Returns the children of the tree grouped in arrays by depth.

        >>> tree = BTNode(data=[x for x in range(7)])
        >>> print(tree)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> print([[n.value for n in level] for level in tree.get_levels()])
        [[0], [1, 2], [3, 4, 5, 6]]

        """
        output = [[]]
        level = 0
        for node in self.breadth_first():
            if node.depth > level:
                output.append([])
                level += 1
            output[level].append(node)
        return output
    def copy(self):
        """
        Returns a shallow copy of self.

        >>> tree = BTNode(data=[0, 1, 2])
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        >>> copy = tree.copy()
        >>> print(copy)
           0
         ┌─┴─┐
         1   2
        >>> copy.extend([3, 4, 5, 6])
        >>> print(copy)
               0
           ┌───┴───┐
           1       2
         ┌─┴─┐   ┌─┴─┐
         3   4   5   6
        >>> print(tree)
           0
         ┌─┴─┐
         1   2
        """
        def copy_children(original_node, copy_node):
            if original_node.l:
                copy_node.l = BTNode(
                        original_node.l.value,
                        depth=copy_node.depth + 1,
                        side='l',
                        parent=copy_node)
                copy_children(original_node.l, copy_node.l)
            if original_node.r:
                copy_node.r = BTNode(
                        original_node.r.value,
                        depth=copy_node.depth + 1,
                        side='r',
                        parent=copy_node
                        )
                copy_children(original_node.r, copy_node.r)
        c = BTNode(self.value)
        copy_children(self, c)
        return c

class BSTNode(BTNode):
    """
    I will write this later
    Does not accept duplicates
    """
    def set_defaults(self):
        self.add = self.add_bst
        self.delete = self.delete_default
        self.extend = self.balance
    def add_bst(self, value):
        if value == self.value:
            raise Exception("Duplicates not allowed in binary search tree")
        if value < self.value:
            if self.l:
                return self.l.add_bst(value)
            else:
                self.l = BSTNode(value=value,
                        side='l',
                        depth=self.depth + 1,
                        parent=self)
                return self.depth + 1
        if value > self.value:
            if self.r:
                return self.r.add_bst(value)
            else:
                self.r = BSTNode(value=value,
                        side='r',
                        depth=self.depth + 1,
                        parent=self)
                return self.depth + 1
    def balance(self, data=[]):
        """
        If self is not balanced, rearrange nodes such that it is balanced.

        This implementation will lean towards the left.

        >>> bst = BSTNode(data=[3, 1, 2, 0, 4, 5, 6, 7])
        >>> print(bst)
                                       3
                       ┌───────────────┴───────────────┐
                       1                               4
               ┌───────┴───────┐                       └───────┐
               0               2                               5
                                                               └───┐
                                                                   6
                                                                   └─┐
                                                                     7
        >>> bst.is_balanced()
        False
        >>> bst.balance()
        >>> print(bst)
                       4
               ┌───────┴───────┐
               2               6
           ┌───┴───┐       ┌───┴───┐
           1       3       5       7
         ┌─┘
         0
        >>> bst.is_balanced()
        True
        """
        nodes = sorted(data + [node.value for node in self.flatten()])
        self.value = nodes.pop(len(nodes) // 2)
        self.l = None
        self.r = None
        def build(node, values):
            if (vals_len := len(values)) == 0:
                return
            left_vals = values[0:(half_vals_len := ceil(vals_len / 2))]
            right_vals = values[half_vals_len:]
            if len(left_vals) > 0:
                node.l = BSTNode(
                        value=left_vals.pop(len(left_vals) // 2),
                        side='l',
                        depth=node.depth + 1,
                        parent=node)
                build(node.l, left_vals)
            if len(right_vals) > 0:
                node.r = BSTNode(
                        value=right_vals.pop(len(right_vals) // 2),
                        side='r',
                        depth=node.depth + 1,
                        parent=node)
                build(node.r, right_vals)
        build(self, nodes)
    def delete_bst(self):
        pass
    def is_bst(self):
        """
        Returns True if self satisfies the definition of a binary search tree.

        """
        nodes = list(self.flatten())
        return all(nodes[i] <= nodes[i+1] for i in range(len(nodes)-1))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    




















