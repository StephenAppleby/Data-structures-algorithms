# Data structures and algorithms

<img src="/avl.gif" width="500" height="240"/>

A collection of data structures and algorithms implemented in Python to demonstrate my understanding of core computer science concepts.

So far, the focus has been on data structures, with the plan to look further at common algorithms in the future.

### Contains working examples of:
- Stack
- Queue
- Circular queue
- Dynamic circular queue
- Heap
- Binary tree
- Binary search tree
- AVL tree

### Visualising binary trees

The binary tree can be rendered to the console with the display() method. The logic for this implementation can be found in ./util/util.py.

Example:

    >>> tree = BinaryTree().preset(7)
    >>> tree.display()
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6

The project also includes a visualising tool for AVL trees. This tool runs in the console and shows a series of slides demonstrating the steps taken for adding and deleting nodes from an AVL tree. Running the script in src/avlslideshow.py will run an infinite sequence while the script in src/avl_gif.py produces the looping sequence shown in the gif above.
