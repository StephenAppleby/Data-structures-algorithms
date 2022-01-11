import ds
import util

bt_expect = [
    """\
   0
 ┌─┴─┐
 1   2""",
    """\
       0
   ┌───┴───┐
   1       1
 ┌─┴─┐   ┌─┴─┐
 2   2   2   2""",
]


def expected(expect, got, raw=False):
    return "Expected:\n{}\nGot:\n{}".format(
        epxect if not raw else repr(expect), got if not raw else repr(got)
    )


suites = dict()

suites["BinaryTree"] = []


def bt_init():
    tree = ds.BinaryTree(data=[x for x in range(3)])
    assert util.display(tree) == (bt_expect[0]), expected(
        bt_expect[0], util.display(tree), raw=True
    )


suites["BinaryTree"].append(("Init", bt_init))


def bt_display_depths():
    tree = ds.bt_example(0)
    assert util.display(tree, item="depths") == bt_expect[1], expected(
        bt_expect[1], util.display(tree, item="depths"), raw=True
    )


suites["BinaryTree"].append(("Dispaly depths", bt_display_depths))


if __name__ == "__main__":
    all_pass = True
    for suite, tests in suites.items():
        total = 0
        failed = 0
        for name, test in tests:
            total += 1
            try:
                test()
            except Exception as e:
                failed += 1
                all_pass = False
                print(suite, "->", name, "failed\n" + str(e))
        print(suite, total - failed, "out of", total, "passed")
    if all_pass:
        print("All tests passed. Congrats =D")
