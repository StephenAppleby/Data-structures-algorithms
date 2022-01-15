from ds import BinaryTree


expect = {
    "bt": {
        "1": """ 0""",
        "2": """\
   0
 ┌─┘
 1""",
        "2d": """\
   0
   └─┐
     2""",
        "3": """\
   0
 ┌─┴─┐
 1   2""",
        "3d": """\
       0
       └───┐
           2
         ┌─┘
         5""",
        "4": """\
       0
   ┌───┴───┐
   1       2
 ┌─┘
 3""",
        "4m": """\
       2
   ┌───┘
   1
 ┌─┴─┐
 3   4""",
        "4d": """\
       0
       └───┐
           2
         ┌─┴─┐
         5   6""",
        "5": """\
       0
   ┌───┴───┐
   1       2
 ┌─┴─┐
 3   4""",
        "6": """\
       0
   ┌───┴───┐
   1       2
 ┌─┴─┐   ┌─┘
 3   4   5""",
        "6ma": """\
       0
   ┌───┴───┐
   1       3
   └─┐   ┌─┴─┐
     4   5   6""",
        "6mb": """\
       5
   ┌───┴───┐
   1       2
 ┌─┴─┐     └─┐
 3   4       6""",
        "7": """\
       0
   ┌───┴───┐
   1       2
 ┌─┴─┐   ┌─┴─┐
 3   4   5   6""",
        "7f": """\
       0
   ┌───┴───┐
   7       2
 ┌─┴─┐   ┌─┴─┐
 7   7   5   6""",
        "7d": """\
       0
   ┌───┴───┐
   1       1
 ┌─┴─┐   ┌─┴─┐
 2   2   2   2""",
    },
    "bst": {
        "1": """ 0""",
        "2": """\
   1
 ┌─┘
 0""",
        "3": """\
   1
 ┌─┴─┐
 0   2""",
        "4": """\
       2
   ┌───┴───┐
   1       3
 ┌─┘
 0""",
        "5": """\
       2
   ┌───┴───┐
   1       4
 ┌─┘     ┌─┘
 0       3""",
        "5d": """\
       4
   ┌───┴───┐
   1       5
   └─┐     └─┐
     2       6""",
        "6": """\
       3
   ┌───┴───┐
   1       5
 ┌─┴─┐   ┌─┘
 0   2   4""",
        "6d": """\
       4
   ┌───┴───┐
   1       5
 ┌─┴─┐     └─┐
 0   2       6""",
        "7": """\
       3
   ┌───┴───┐
   1       5
 ┌─┴─┐   ┌─┴─┐
 0   2   4   6""",
    },
}

example = {"bt": {}}
