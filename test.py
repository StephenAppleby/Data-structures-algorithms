import ds

bt_expect = [
    """\
   0
 ┌─┴─┐
 1   2""",
    """
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6
    """,
]


def expected(expect, got, raw=False):
    return "\nExpected:\n{}\nGot:\n{}".format(
        epxect if not raw else repr(expect), got if not raw else repr(got)
    )


def binary_tree():
    tree = ds.BinaryTree(data=[x for x in range(3)])
    assert tree.root is not None
    assert tree.display() == (bt_expect[0]), expected(
        bt_expect[0], tree.display(), raw=True
    )


if __name__ == "__main__":
    binary_tree()
