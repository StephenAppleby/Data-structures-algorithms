import sys
import unittest
from pathlib import Path

import ds
from ds.stack import Stack
from ds.queue import Queue
from ds.cqueue import CircularQueue
from ds.dcqueue import DynamicCircularQueue


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


if __name__ == "__main__":
    unittest.main()
