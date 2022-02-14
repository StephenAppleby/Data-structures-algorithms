import random
import unittest

from test_expectations import expectations
import ds
from ds.stack import Stack
from ds.queue import Queue
from ds.cqueue import CircularQueue
from ds.dcqueue import DynamicCircularQueue
from ds.bt import BinaryTree
from ds.bst import BinarySearchTree
from ds.avl import AVLTree
from ds.btheap import BTHeap
from ds.heap import Heap


class TestStack(unittest.TestCase):
    def test_init(self):
        stack = Stack()
        self.assertIsInstance(stack, ds.stack.Stack)
        self.assertEqual(stack.max_size, -1)

    def test_full(self):
        stack = Stack(max_size=3)
        stack.extend([0, 1])
        self.assertFalse(stack.is_full())
        stack.push(2)
        self.assertTrue(stack.is_full())
        with self.assertRaises(Exception):
            stack.push(3)

    def test_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(0)
        self.assertFalse(stack.is_empty())
        stack.pop()
        self.assertTrue(stack.is_empty())
        with self.assertRaises(Exception):
            stack.pop()

    def test_integration(self):
        stack = Stack(data=[x for x in range(5)])
        self.assertEqual(stack.data, [0, 1, 2, 3, 4])
        stack.push(5)
        self.assertEqual(stack.data, [0, 1, 2, 3, 4, 5])
        x = stack.pop()
        self.assertEqual(x, 5)
        self.assertEqual(stack.data, [0, 1, 2, 3, 4])
        self.assertEqual(stack.peek(), 4)


class TestQueue(unittest.TestCase):
    def test_init(self):
        queue = Queue()
        self.assertIsInstance(queue, ds.queue.Queue)
        self.assertEqual(queue.max_size, -1)

    def test_full(self):
        queue = Queue(max_size=3)
        queue.extend([0, 1])
        self.assertFalse(queue.is_full())
        queue.enqueue(2)
        self.assertTrue(queue.is_full())
        with self.assertRaises(Exception):
            self.enqueue(3)

    def test_empty(self):
        queue = Queue()
        self.assertTrue(queue.is_empty())
        queue.enqueue(0)
        self.assertFalse(queue.is_empty())
        queue.dequeue()
        self.assertTrue(queue.is_empty())
        with self.assertRaises(Exception):
            self.dequeue()

    def test_integration(self):
        queue = Queue(data=[x for x in range(5)])
        self.assertEqual(queue.data, [0, 1, 2, 3, 4])
        queue.enqueue(5)
        self.assertEqual(queue.data, [0, 1, 2, 3, 4, 5])
        x = queue.dequeue()
        self.assertEqual(x, 0)
        self.assertEqual(queue.data, [1, 2, 3, 4, 5])
        self.assertEqual(queue.peek(), 1)


class TestCQueue(unittest.TestCase):
    def test_init(self):
        cqueue = CircularQueue()
        self.assertIsInstance(cqueue, ds.cqueue.CircularQueue)
        self.assertEqual(cqueue.max_size, 8)

    def test_full(self):
        cqueue = CircularQueue(data=[0, 1, 2], max_size=3)
        self.assertTrue(cqueue.is_full())
        cqueue.dequeue()
        self.assertFalse(cqueue.is_full())
        cqueue.enqueue(3)
        self.assertTrue(cqueue.is_full())
        with self.assertRaises(Exception):
            cqueue.enqueue(3)

    def test_empty(self):
        cqueue = CircularQueue()
        self.assertTrue(cqueue.is_empty())
        cqueue.enqueue(0)
        self.assertFalse(cqueue.is_empty())
        cqueue.dequeue()
        self.assertTrue(cqueue.is_empty())
        with self.assertRaises(Exception):
            cqueue.dequeue()

    def test_integration(self):
        cqueue = CircularQueue(data=[0, 1, 2, 3], max_size=4)
        self.assertEqual(cqueue.peek(), 0)
        for _ in range(3):
            cqueue.dequeue()
        self.assertEqual(cqueue.data, [None, None, None, 3])
        cqueue.extend([4, 5])
        self.assertEqual(cqueue.data, [4, 5, None, 3])
        for _ in range(3):
            cqueue.dequeue()
        self.assertTrue(cqueue.is_empty())
        self.assertEqual(cqueue.data, [None, None, None, None])
        cqueue.enqueue(0)
        self.assertEqual(cqueue.data, [0, None, None, None])

    def test_stree(self):
        cqueue = CircularQueue(max_size=100)
        for x in range(20):
            for y in range(100):
                cqueue.enqueue(y)
            for z in range(100):
                cqueue.dequeue()


class TestDCQueue(unittest.TestCase):
    def test_handle_full(self):
        dcqueue = DynamicCircularQueue(data=[x for x in range(8)])
        self.assertEqual(dcqueue.data, [0, 1, 2, 3, 4, 5, 6, 7])
        dcqueue.dequeue()
        self.assertEqual(dcqueue.data, [None, 1, 2, 3, 4, 5, 6, 7])
        dcqueue.extend([8, 9, 10, 11])
        self.assertEqual(
            dcqueue.data,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, None, None, None, None, None],
        )
        for _ in range(11):
            dcqueue.dequeue()
        self.assertTrue(dcqueue.is_empty())
        self.assertEqual(dcqueue.data, [None] * 8)

    def test_stress(self):
        dcqueue = DynamicCircularQueue()
        for x in range(20):
            for y in range(90):
                dcqueue.enqueue(y)
            for z in range(90):
                dcqueue.dequeue()


class TestBT(unittest.TestCase):
    def test_init(self):
        tree = BinaryTree().preset(7)
        self.assertEqual(str(tree), expectations["bt_preset7"])

    def test_is_perfect(self):
        check_true = lambda x: self.assertTrue(BinaryTree().preset(x).is_perfect())
        check_false = lambda x: self.assertFalse(BinaryTree().preset(x).is_perfect())
        check_true(1)
        check_false(2)
        check_true(3)
        check_false(4)
        check_false(5)
        check_false(6)
        check_true(7)

    def test_is_full(self):
        check_true = lambda x: self.assertTrue(BinaryTree().preset(x).is_full())
        check_false = lambda x: self.assertFalse(BinaryTree().preset(x).is_full())
        check_true(1)
        check_false(2)
        check_true(3)
        check_false(4)
        check_true(5)
        check_false(6)
        check_true(7)
        check_false(8)
        check_true(9)

    def test_is_complete(self):
        for x in range(1, 15):
            self.assertTrue(BinaryTree().preset(x).is_complete())

    def test_is_balanced(self):
        tree = BinaryTree().preset(4)
        self.assertTrue(tree.is_balanced())
        tree.add(4)
        self.assertTrue(tree.is_balanced())
        tree.root.del_node("r")
        self.assertFalse(tree.is_balanced())
        tree.add(2)
        tree.get(3).add_node(5, "l")
        self.assertFalse(tree.is_balanced())
        tree.get(2).add_node(6, "r")
        self.assertTrue(tree.is_balanced())

    def test_breadth_first(self):
        nodes = list(BinaryTree().preset(7).breadth_first())
        keys = [node.key for node in nodes]
        self.assertEqual(keys, [0, 1, 2, 3, 4, 5, 6])

    def test_flatten(self):
        nodes = list(BinaryTree().preset(7).flatten())
        keys = [node.key for node in nodes]
        self.assertEqual(keys, [3, 1, 4, 0, 5, 2, 6])

    def test_preorder(self):
        nodes = list(BinaryTree().preset(7).preorder())
        keys = [node.key for node in nodes]
        self.assertEqual(keys, [0, 1, 3, 4, 2, 5, 6])

    def test_postorder(self):
        nodes = list(BinaryTree().preset(7).postorder())
        keys = [node.key for node in nodes]
        self.assertEqual(keys, [3, 4, 1, 5, 6, 2, 0])


class TestBST(unittest.TestCase):
    def test_init(self):
        bst = BinarySearchTree().preset(7)
        self.assertEqual(str(bst), expectations["bst_preset7"])

    def test_add_bst(self):
        bst = BinarySearchTree(data=[x * 10 for x in range(5)])
        self.assertEqual(str(bst), expectations["bst_add_A"])
        bst.add(15)
        bst.add(60)
        self.assertEqual(str(bst), expectations["bst_add_B"])
        bst.add(80)
        bst.add(8)
        self.assertEqual(str(bst), expectations["bst_add_C"])

    def test_balance(self):
        bst = BinarySearchTree().preset(7)
        bst.add(7)
        bst.add(8)
        bst.balance()
        self.assertEqual(str(bst), expectations["bst_balance_A"])
        bst.balance([10, 20, 30, 40])
        self.assertEqual(str(bst), expectations["bst_balance_B"])

    def test_delete(self):
        bst = BinarySearchTree().preset(15)
        # Case 1: leaf
        bst.delete(10)
        self.assertEqual(str(bst), expectations["bst_delete_A"])
        # Case 2: One child
        bst.delete(9)
        self.assertEqual(str(bst), expectations["bst_delete_B"])
        # Case 3: Two children with complex successor
        bst.delete(3)
        self.assertEqual(str(bst), expectations["bst_delete_C"])
        # Case 4: Two children with simple successor
        bst.delete(4)
        self.assertEqual(str(bst), expectations["bst_delete_D"])


class TestAVL(unittest.TestCase):
    def test_init(self):
        avl = AVLTree().preset(7)
        self.assertEqual(str(avl), expectations["bst_preset7"])

    def test_left_rotate(self):
        avl = AVLTree(data=[0])
        avl.root.add_node(1, "r")
        avl.get(1).add_node(2, "r")
        self.assertEqual(str(avl), expectations["avl_left_rotate"])
        avl.root = avl.root.left_rotate()
        self.assertEqual(str(avl), expectations["bst_preset3"])

    def test_right_rotate(self):
        avl = AVLTree(data=[2])
        avl.root.add_node(1, "l")
        avl.get(1).add_node(0, "l")
        self.assertEqual(str(avl), expectations["avl_right_rotate"])
        avl.root = avl.root.right_rotate()
        self.assertEqual(str(avl), expectations["bst_preset3"])

    def test_left_right_rotate(self):
        avl = AVLTree(data=[2])
        avl.root.add_node(0, "l")
        avl.get(0).add_node(1, "r")
        self.assertEqual(str(avl), expectations["avl_left_right_rotate"])
        avl.root = avl.root.left_right_rotate()
        self.assertEqual(str(avl), expectations["bst_preset3"])

    def test_right_left_rotate(self):
        avl = AVLTree(data=[0])
        avl.root.add_node(2, "r")
        avl.get(2).add_node(1, "l")
        self.assertEqual(str(avl), expectations["avl_right_left_rotate"])
        avl.root = avl.root.right_left_rotate()
        self.assertEqual(str(avl), expectations["bst_preset3"])

    def test_integration(self):
        avl = AVLTree()
        candidates = [x for x in range(1000)]
        contents = []
        for x in range(200):
            y = candidates.pop(random.randint(0, len(candidates) - 1))
            avl.add(y)
            contents.append(y)
            self.assertTrue(avl.is_balanced())
            self.assertTrue(avl.is_bst())
        for x in range(200):
            y = contents.pop(random.randint(0, len(contents) - 1))
            avl.delete(y)
            self.assertTrue(avl.is_balanced())
            self.assertTrue(avl.is_bst())


class TestBTHeap(unittest.TestCase):
    def test_init(self):
        heap = BTHeap()

    def test_heapify(self):
        repetitions = 40
        heap_size = 50
        for x in range(repetitions):
            candidates = [i for i in range(1000)]
            contents = []
            for y in range(heap_size):
                contents.append(candidates.pop(random.randint(0, len(candidates) - 1)))
            heap = BTHeap(data=contents)
            self.assertTrue(heap.is_complete())
            self.assertTrue(heap.is_heap())

    def test_add(self):
        repetitions = 50
        heap = BTHeap()
        candidates = [i for i in range(1000)]
        for x in range(repetitions):
            heap.add(candidates.pop(random.randint(0, len(candidates) - 1)))
            self.assertTrue(heap.is_complete())
            self.assertTrue(heap.is_heap())


class TestHeap(unittest.TestCase):
    def test_heapify(self):
        repetitions = 100
        heap_size = 68
        for x in range(repetitions):
            candidates = [i for i in range(1000)]
            contents = []
            for y in range(heap_size):
                contents.append(candidates.pop(random.randint(0, len(candidates) - 1)))
            heap = Heap(data=contents)
            self.assertTrue(heap.is_heap())

    def test_stress(self):
        repetitions = 20
        heap_size = 70
        for x in range(repetitions):
            heap = Heap()
            candidates = [i for i in range(1000)]
            contents = []
            for y in range(heap_size):
                y = candidates.pop(random.randint(0, len(candidates) - 1))
                contents.append(y)
                heap.add(y)
                self.assertTrue(heap.is_heap())
            for z in range(heap_size):
                heap.pop()
                self.assertTrue(heap.is_heap())


if __name__ == "__main__":
    unittest.main()
