import ds
import random
import traceback
from util import display
from test_util import expect, example

from time import sleep

assertions = 0


def expected(got, expect, raw=False):
    return "Expected:\n{}\nGot:\n{}".format(
        repr(expect) if raw else expect,
        repr(got) if raw else got,
    )


def test(got, exp, raw=False):
    global assertions
    assertions += 1
    assert got == exp, expected(got, exp, raw)


def get_bt(count):
    return ds.BinaryTree(data=[x for x in range(count)])


def get_bst(count):
    return ds.BinarySearchTree(data=[x for x in range(count)])


def get_avl(count):
    return ds.AVLTree(data=[x for x in range(count)])


# Binary Tree


def bt_init():
    test(isinstance(ds.BinaryTree(), ds.BinaryTree), True)
    got = display(get_bt(3))
    exp = expect["bt"]["3"]
    test(got, exp)


def bt_add():
    tree = get_bt(1)
    got = display(tree)
    exp = expect["bt"]["1"]
    test(got, exp)
    for x in range(1, 7):
        tree.add(x)
        got = display(tree)
        exp = expect["bt"][str(x + 1)]
        test(got, exp)


def bt_get():
    tree = get_bt(7)
    test(isinstance(tree.get(2), ds.BinaryTree.BTNode), True)
    test(tree.get(1).key, 1)
    try:
        tree.get(9)
    except KeyError as e:
        test(str(e), "'9 not in tree'")
    test(tree.get(0).key, 0)


def bt_delete():
    tree = get_bt(7)
    tree.delete(1)
    test(display(tree), expect["bt"]["4d"])
    tree.delete(6)
    test(display(tree), expect["bt"]["3d"])
    tree.delete(0)
    test(tree.root, None)


def bt_is_perfect():
    tree = get_bt(0)
    test(tree.is_perfect(), None)
    tree = get_bt(7)
    test(tree.is_perfect(), True)
    tree.delete(6)
    test(tree.is_perfect(), False)
    tree = get_bt(7)
    tree.delete(1)
    test(tree.is_perfect(), False)


def bt_is_full():
    tree = get_bt(0)
    test(tree.is_full(), None)
    tree = get_bt(3)
    test(tree.is_full(), True)
    tree.add(3)
    test(tree.is_full(), False)
    tree.add(4)
    test(tree.is_full(), True)


def bt_is_complete():
    tree = get_bt(0)
    test(tree.is_complete(), None)
    for x in range(7):
        tree.add(x)
        test(tree.is_complete(), True)
    tree.delete(5)
    test(tree.is_complete(), False)
    tree.delete(6)
    tree.delete(1)
    test(tree.is_complete(), False)


def bt_is_balanced():
    tree = get_bt(0)
    test(tree.is_balanced(), None)
    for x in range(8):
        tree.add(x)
        test(tree.is_balanced(), True)
    tree.delete(5)
    tree.delete(6)
    test(tree.is_balanced(), False)
    tree.delete(2)
    test(tree.is_balanced(), False)


def bt_breadth_first():
    tree = get_bt(0)
    test(list(tree.breadth_first()), [])
    tree = get_bt(7)
    got = [n.key for n in get_bt(7).breadth_first()]
    exp = [0, 1, 2, 3, 4, 5, 6]
    test(got, exp)


def bt_flatten():
    tree = get_bt(0)
    test(list(tree.flatten()), [])
    tree = get_bt(7)
    got = [n.key for n in get_bt(7).flatten()]
    exp = [3, 1, 4, 0, 5, 2, 6]
    test(got, exp)


def bt_preorder():
    tree = get_bt(0)
    test(list(tree.preorder()), [])
    tree = get_bt(7)
    got = [n.key for n in get_bt(7).preorder()]
    exp = [0, 1, 3, 4, 2, 5, 6]
    test(got, exp)


def bt_postorder():
    tree = get_bt(0)
    test(list(tree.postorder()), [])
    tree = get_bt(7)
    got = [n.key for n in get_bt(7).postorder()]
    exp = [3, 4, 1, 5, 6, 2, 0]
    test(got, exp)


# Binary Tree Node


def btn_init():
    node = ds.BinaryTree.BTNode()
    test(isinstance(node, ds.BinaryTree.BTNode), True)
    tree = get_bt(3)
    node = tree.get(2)
    test(node.key, 2)


def btn_get_height():
    tree = get_bt(10)
    test(tree.get(0).get_height(), 3)
    test(tree.get(9).get_height(), 0)
    test(tree.get(1).get_height(), 2)


# Binary Search Tree


def bst_init():
    test(isinstance(ds.BinarySearchTree(), ds.BinarySearchTree), True)
    test(display(get_bst(1)), " 0")


def bst_balance_add():
    bst = get_bst(0)
    for x in range(7):
        bst.add(x)
        bst.balance()
        test(display(bst), expect["bst"][str(x + 1)])


def bst_delete():
    bst = get_bst(7)
    bst.delete(3)
    test(display(bst), expect["bst"]["6d"])
    bst.delete(0)
    test(display(bst), expect["bst"]["5d"])
    bst.delete(1)
    test(display(bst), expect["bst"]["4d"])
    bst.delete(2)
    test(display(bst), expect["bst"]["3d"])


def bst_get():
    bst = get_bst(7)
    try:
        bst.get(7)
    except KeyError as e:
        test(str(e), "'7 not in tree'")
    test(bst.get(3).key, 3)
    test(bst.get(6).key, 6)
    test(bst.get(0).key, 0)


def avlnode_left_rotate():
    avl = get_avl(7)
    avl.delete(0)
    avl.delete(2)
    avl.get(3).left_rotate()
    test(avl.inspect(), expect["avl"]["5lri"])


def avlnode_right_rotate():
    avl = get_avl(7)
    avl.root.right_rotate()
    test(avl.inspect(), expect["avl"]["7rri"])


def avl_add():
    avl = get_avl(0)
    numbers = [x for x in range(1000)]
    for x in range(10):
        y = numbers.pop(random.randint(0, len(numbers) - 1))
        avl.add(y)
        test(avl.is_balanced(), True)


def avl_delete():
    avl = get_avl(0)
    numbers = [x for x in range(1000)]
    contents = []
    for x in range(80):
        y = numbers.pop(random.randint(0, len(numbers) - 1))
        avl.add(y)
        contents.append(y)
    for x in range(78):
        y = contents.pop(random.randint(0, len(contents) - 1))
        avl.delete(y)
        test(avl.is_balanced(), True)


def suites():
    return {
        "BinaryTree": [
            ("Init", bt_init),
            ("Add", bt_add),
            ("Get", bt_get),
            ("Delete", bt_delete),
            ("Is perfect", bt_is_perfect),
            ("Is full", bt_is_full),
            ("Is complete", bt_is_complete),
            ("Is balanced", bt_is_balanced),
            ("Breadth first", bt_breadth_first),
            ("Flatten", bt_flatten),
            ("Preorder", bt_preorder),
            ("Postorder", bt_postorder),
        ],
        "BTNode": [
            ("Init", btn_init),
            ("Get height", btn_get_height),
        ],
        "BinarySearchTree": [
            ("Init", bst_init),
            ("Balance and Add", bst_balance_add),
            ("Delete", bst_delete),
            ("Get", bst_get),
        ],
        "AVLTree": [("Add", avl_add), ("Delete", avl_delete)],
        "AVLNode": [
            ("Left rotate", avlnode_left_rotate),
            ("Right rotate", avlnode_right_rotate),
        ],
    }


if __name__ == "__main__":
    all_pass = True
    for suite, tests in suites().items():
        total = 0
        passed = 0
        for name, func in tests:
            total += 1
            try:
                func()
                passed += 1
            except AssertionError as e:
                all_pass = False
                print(suite, "->", name, "failed\n" + str(e))

            except Exception as e:
                all_pass = False
                print(suite, "->", name, "failed")
                traceback.print_exc()
        print(f"{suite:25}{passed:3} / {total:<3}")
    if all_pass:
        print(f"{assertions} assertions")
        print("All tests passed. Congrats =D")
