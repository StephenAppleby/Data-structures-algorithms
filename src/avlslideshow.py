from ds import avl, dcqueue, util
import os
import random
from time import sleep

log = []


def clear():
    os.system("clear")


class style:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class AVL_Slideshow(avl.AVLTree):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slides = dcqueue.DynamicCircularQueue()
        self.add = self.add_slideshow
        self.delete = self.delete_slideshow

    class AVL_Slideshow_Node(avl.AVLTree.AVLNode):
        def __init__(self, key=None, tree=None, style=""):
            super().__init__(key)
            self.style = style
            self.tree = tree

        def add_node(self, key, side, style=""):
            if side == "l":
                self.l = AVL_Slideshow.AVL_Slideshow_Node(key, self.tree, style)
            if side == "r":
                self.r = AVL_Slideshow.AVL_Slideshow_Node(key, self.tree, style)
            self.set_height()

    def display(self):
        print(util.util.display(self, True))

    def add_root(self, key, style=""):
        self.root = AVL_Slideshow.AVL_Slideshow_Node(key, self, style=style)

    def add_slide(self, title="", pause=1):
        def copy_children(original, copy):
            if original.l:
                copy.add_node(original.l.key, "l", original.l.style)
                copy_children(original.l, copy.l)
            if original.r:
                copy.add_node(original.r.key, "r", original.r.style)
                copy_children(original.r, copy.r)

        tree = AVL_Slideshow()
        if self.root:
            tree.add_root(self.root.key, style=self.root.style)
            copy_children(self.root, tree.root)
        self.slides.enqueue({"tree": tree, "title": title, "pause": pause})

    def get_slides(self):
        while len(self.slides) > 0:
            yield self.slides.dequeue()

    def add_slideshow(self, key):
        title = f"Add -> {key}\n"
        self.add_slide(title, 2)

        def process_node(node, side):
            node.style = style.BOLD + style.CYAN
            child = None
            if side == "l":
                self.add_slide(title + f"{key} < {node.key}")
                child = node.l
            if side == "r":
                self.add_slide(title + f"{key} > {node.key}")
                child = node.r
            new_node, return_case, pause = rec_add(child, key)
            node.attach_node(new_node, side)
            if return_case == "balanced_link":
                new_node.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Balanced node {new_node.key}", 2)
                new_node.style = ""
            if return_case == "link":
                new_node.style = style.BOLD + style.GREEN
                self.add_slide(
                    title + f"Node {new_node.key} is already balanced", pause
                )
                new_node.style = ""
            node.style = ""

        def found_leaf(node, side):
            node.style = style.BOLD + style.GREEN
            self.add_slide(title + f"Found leaf {node.key}")
            node.add_node(key, side)
            if side == "l":
                node.l.style = style.BOLD + style.PURPLE
                self.add_slide(title + f"Added node {key}")
                node.l.style = ""
            if side == "r":
                node.r.style = style.BOLD + style.PURPLE
                self.add_slide(title + f"Added node {key}")
                node.r.style = ""
            node.style = ""

        def rec_add(node, key):
            return_case = "link"
            if key == node.key:
                raise Exception("Duplicates not allowed in binary search tree")
            if key < node.key:
                if node.l:
                    process_node(node, "l")
                else:
                    found_leaf(node, "l")
            if key > node.key:
                if node.r:
                    process_node(node, "r")
                else:
                    found_leaf(node, "r")
            bal_fac = node.get_balance_factor()
            pause = 1
            if bal_fac < -1 or bal_fac > 1:
                node.style = style.BOLD + style.RED
                self.add_slide(title + f"Balancing node {node.key}", 2)
                node.style = ""
                return_case = "balanced_link"
                pause = 2
            return node.balance(), return_case, pause

        if not self.root:
            self.add_root(key, self)
        else:
            new_node, return_case, pause = rec_add(self.root, key)
            if return_case == "found":
                new_node.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Found leaf {new_node.key}", 2)
                new_node.style = ""
            if return_case == "balanced_link":
                new_node.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Balanced node {new_node.key}", 2)
                new_node.style = ""
            if return_case == "link":
                new_node.style = style.BOLD + style.GREEN
                self.add_slide(
                    title + f"Node {new_node.key} is already balanced", pause
                )
                new_node.style = ""
            self.root = new_node
        self.add_slide("Finish\n", 2)

    def delete_slideshow(self, key):
        title = f"Delete -> {key}\n"
        self.add_slide(title, 2)

        def process_node(node, side):
            node.style = style.BOLD + style.CYAN
            pause = 1
            return_case = None
            del_node = None
            if side == "l":
                self.add_slide(title + f"{key} < {node.key}")
                (del_node, return_case), pause = rec_del(node.l)
            if side == "r":
                self.add_slide(title + f"{key} > {node.key}")
                (del_node, return_case), pause = rec_del(node.r)
            node.attach_node(del_node, side)

            if return_case == "delete_leaf":
                self.add_slide(title + f"Deleted {key}", 2)
            if return_case in ["one_child", "one_successor", "successor"]:
                del_node.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Replaced {key} with {del_node.key}", 2)
                del_node.style = ""
            if return_case == "balanced_link":
                del_node.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Balanced node {del_node.key}", 2)
                del_node.style = ""
            if return_case == "link":
                del_node.style = style.BOLD + style.GREEN
                self.add_slide(
                    title + f"Node {del_node.key} is already balanced", pause
                )
                del_node.style = ""
            node.style = ""

        def rec_del(node):
            if key == node.key:
                node.style = style.BOLD + style.RED
                self.add_slide(title + f"{key} found", 2)
                return get_replacement(node), 2
            elif node.l and key < node.key:
                process_node(node, "l")
            elif node.r and key > node.key:
                process_node(node, "r")
            else:
                raise Exception("Attempted to delete missing key from tree:", key)
            bal_fac = node.get_balance_factor()
            if bal_fac < -1 or bal_fac > 1:
                node.style = style.BOLD + style.RED
                self.add_slide(title + f"Balancing node {node.key}", 2)
                node.style = ""
                return (node.balance(), "balanced_link"), 2
            else:
                return (node.balance(), "link"), 1

        def get_replacement(node):
            # Determine which children are present
            kids = ""
            if node.l:
                kids += "l"
            if node.r:
                kids += "r"
            # No children
            if kids == "":
                return None, "delete_leaf"
            # One child
            if kids == "l":
                return node.l, "one_child"
            if kids == "r":
                return node.r, "one_child"
            # Two children -> Find successor
            # Successor is node.r
            if not node.r.l:
                node.r.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Found successor {node.r.key}", 2)
                node.r.style = ""
                node.r.attach_node(node.l, "l")
                return node.r.balance(), "one_successor"
            # Successor is not node.r
            node.r.style = style.BOLD + style.CYAN
            self.add_slide(title + f"Looking for successor {node.r.key}")
            link, successor = get_successor(node.r)
            node.r.style = ""
            successor.attach_node(node.l, "l")
            successor.attach_node(link, "r")
            return successor.balance(), "successor"

        def get_successor(parent):
            successor = parent.l
            if successor.l:
                successor.style = style.BOLD + style.CYAN
                self.add_slide(title + f"Looking for successor {successor.key}")
                link, got = get_successor(successor)
                successor.style = ""
                parent.attach_node(link, "l")
                return (parent.balance(), got)
            else:
                successor.style = style.BOLD + style.GREEN
                self.add_slide(title + f"Found successor {successor.key}", 2)
                parent.attach_node(successor.r, "l")
                successor.style = ""
                return (parent.balance(), successor)

        (del_node, return_case), pause = rec_del(self.root)
        old_root = self.root
        self.root = del_node
        if return_case == "delete_leaf":
            self.add_slide(title + f"Deleted root", 2)
        if return_case in ["one_child", "one_successor", "successor"]:
            del_node.style = style.BOLD + style.GREEN
            self.add_slide(title + f"Replaced {old_root.key} with {del_node.key}", 2)
            del_node.style = ""
        if return_case == "balanced_link":
            del_node.style = style.BOLD + style.GREEN
            self.add_slide(title + f"Balanced node {del_node.key}", 2)
            del_node.style = ""
        if return_case == "link":
            del_node.style = style.BOLD + style.GREEN
            self.add_slide(title + f"Node {del_node.key} is already balanced", pause)
            del_node.style = ""
        self.add_slide("Finish\n", 2)

    def show(self, pause_factor=1, wait=False):
        for slide in self.get_slides():
            for _ in range(slide["pause"]):
                clear()
                if slide["title"]:
                    print(slide["title"])
                slide["tree"].display()
                print("\n".join(log))
                if wait:
                    input()
                else:
                    sleep(1 * pause_factor)

    def play(self, size=15, initial=5, pause_factor=1):
        numbers = [x for x in range(1000)]
        contents = []
        for x in range(initial):
            y = numbers.pop(random.randint(0, len(numbers) - 1))
            self.add_avl(y)
            contents.append(y)
        size = size - initial
        while True:
            for x in range(size):
                y = numbers.pop(random.randint(0, len(numbers) - 1))
                self.add(y)
                contents.append(y)
                self.show(pause_factor=pause_factor)
            for x in range(size):
                y = contents.pop(random.randint(0, len(contents) - 1))
                self.delete(y)
                numbers.append(y)
                self.show(pause_factor=pause_factor)


if __name__ == "__main__":
    tree = AVL_Slideshow()
    try:
        tree.play(size=29, initial=14, pause_factor=1)
    except Exception:
        print("\n".join(log))
        raise
