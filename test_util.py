from ds import BinaryTree


expect = {
    "bt": {
        "1": """ 0""",
        "2": """\
   0
 ┌─┘
 1""",
        "2m": """\
   0
 ┌─┘
 2""",
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
        "15h": """\
               3
       ┌───────┴───────┐
       2               2
   ┌───┴───┐       ┌───┴───┐
   1       1       1       1
 ┌─┴─┐   ┌─┴─┐   ┌─┴─┐   ┌─┴─┐
 0   0   0   0   0   0   0   0""",
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
        "3d": """\
       4
       └───┐
           5
           └─┐
             6""",
        "4": """\
       2
   ┌───┴───┐
   1       3
 ┌─┘
 0""",
        "4d": """\
       4
   ┌───┴───┐
   2       5
           └─┐
             6""",
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
    "avl": {
        "5lr": """\
       5
   ┌───┴───┐
   3       6
 ┌─┴─┐
 1   4""",
        "5lri": """\
Key: 1        Left: None    Right: None   Parent: 3     Side: l       Height: 0
Key: 3        Left: 1       Right: 4      Parent: 5     Side: l       Height: 1
Key: 4        Left: None    Right: None   Parent: 3     Side: r       Height: 0
Key: 5        Left: 3       Right: 6      Parent: None  Side: None    Height: 2
Key: 6        Left: None    Right: None   Parent: 5     Side: r       Height: 0\n""",
        "7rri": """\
Key: 0        Left: None    Right: None   Parent: 1     Side: l       Height: 0
Key: 1        Left: 0       Right: 3      Parent: None  Side: None    Height: 3
Key: 2        Left: None    Right: None   Parent: 3     Side: l       Height: 0
Key: 3        Left: 2       Right: 5      Parent: 1     Side: r       Height: 2
Key: 4        Left: None    Right: None   Parent: 5     Side: l       Height: 0
Key: 5        Left: 4       Right: 6      Parent: 3     Side: r       Height: 1
Key: 6        Left: None    Right: None   Parent: 5     Side: r       Height: 0\n""",
    },
}

example = {"bt": {}}
