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


def is_bold(node):
    output = False
    try:
        output = node and style.BOLD in node.style
    except AttributeError:
        pass
    return output


def format_nodes(nodes, chars_width):
    # Cull copied nodes with no key. The nodes given here include the empties provided
    # by the fill method
    return (f"{str(n.key):^3}" if n else " " * chars_width for n in nodes)


def format_nodes_slideshow(nodes, chars_width):
    # print([node.inspect() if node else "NA" for node in nodes])
    return (
        f"{n.style if n.style else ''}{str(n.key):^3}\033[0m"
        if n
        else " " * chars_width
        for n in nodes
    )


def display(tree, is_slideshow=False):
    """
    Renders a binary tree to the console in a human readable format.

    This function is designed to display small binary trees for demonstration
    purposes only. It assumes that the key of each node will be no more than
    three characters in width and will break otherwise. Trees of height 6 or
    less are reccommended, less for smaller screens

    Example:
           0
       ┌───┴───┐
       1       2
     ┌─┴─┐   ┌─┴─┐
     3   4   5   6
    """
    if not tree.root:
        return
    output = ""
    levels = []

    def get_levels(node, depth, width):
        if len(levels) <= depth:
            levels.append([None for x in range(2 ** depth)])
        levels[depth][width] = node
        if node.l:
            get_levels(node.l, depth + 1, width * 2)
        if node.r:
            get_levels(node.r, depth + 1, (width * 2) + 1)

    get_levels(tree.root, 0, 0)

    for level, nodes in enumerate(levels):
        # The amount of padding is inversely proportional to level depth
        inv_row = len(levels) - (level + 1)
        gap = 2 ** inv_row
        # We assume that each key to be represented will be no more than
        # three chars long
        chars_width = 3
        pad = " " if inv_row == 0 else " " * (((gap - 1) * chars_width) + gap)
        # We will need to add half of the padding between each node to the
        # front of the row to space it out correctly
        half_pad = pad[: len(pad) // 2]
        output += half_pad
        # Ensure that we have the string key of each node to three chars
        # or the same amount of spaces
        formatted_nodes = []
        if is_slideshow:
            formatted_nodes = format_nodes_slideshow(nodes, chars_width)
        else:
            formatted_nodes = format_nodes(nodes, chars_width)
        output += pad.join(formatted_nodes)
        output = output.rstrip()
        # Add the pipes after each level except the last
        if inv_row != 0:
            # ┘ = "\u2518"
            # ┛ = "\u251B"
            # └ = "\u2514"
            # ┗ = "\u2517"
            # ┴ = "\u2534"
            # ┹ = "\u2539"
            # ┺ = "\u253A"
            # ─ = "\u2500"
            # ━ = "\u2501"
            # ┌ = "\u250C"
            # ┏ = "\u250F"
            # ┐ = "\u2510"
            # ┓ = "\u2513"
            # Make sure pipes are on a new line
            output += "\n"
            # We'll need to do a similar process for padding as before but
            # with the inv_row key of the following level
            inv_row -= 1
            if inv_row == -1:
                inv_row = 0
            gap = 2 ** inv_row
            pad = " " if inv_row == 0 else " " * (((gap - 1) * chars_width) + gap)
            half_pad = pad[: len(pad) // 2]
            output += half_pad
            # Assign the appropriate pipes if child present and spaces if not
            for n, node in enumerate(nodes):
                if not node:
                    output += (
                        "   "
                        + (" " * len(half_pad))
                        + " "
                        + (" " * len(half_pad))
                        + "   "
                    )
                else:
                    if node.l and is_bold(node.l):
                        output += " " + "┏" + "━"
                        output += len(half_pad) * "━"
                    if node.l and not is_bold(node.l):
                        output += " " + "┌" + "─"
                        output += len(half_pad) * "─"
                    if not node.l:
                        output += "   " + (len(half_pad) * " ")
                    if node.l and not node.r and is_bold(node.l):
                        output += "┛"
                    if node.l and not node.r and not is_bold(node.l):
                        output += "┘"
                    if (
                        node.l
                        and node.r
                        and not is_bold(node.l)
                        and not is_bold(node.r)
                    ):
                        output += "┴"
                    if node.l and node.r and is_bold(node.l):
                        output += "┹"
                    if node.l and node.r and is_bold(node.r):
                        output += "┺"
                    if not node.l and node.r and is_bold(node.r):
                        output += "┗"
                    if not node.l and node.r and not is_bold(node.r):
                        output += "└"
                    if not node.l and not node.r:
                        output += " "
                    if node.r and is_bold(node.r):
                        output += len(half_pad) * "━"
                        output += "━" + "┓" + " "
                    if node.r and not is_bold(node.r):
                        output += len(half_pad) * "─"
                        output += "─" + "┐" + " "
                    if not node.r:
                        output += "   " + (len(half_pad) * " ")
                # Add padding to each set of pipes except the last
                if n != len(nodes) - 1:
                    output += pad
            output = output.rstrip()
            output += "\n"
    return output


def inspect(tree):
    return format_inspection([inspect_node(node) for node in tree.flatten()])


def inspect_node(node):
    output = {
        "Key": node.key,
        "Left": node.l.key if node.l else "NA",
        "Right": node.r.key if node.r else "NA",
    }
    try:
        output["Height"] = node.height
    except AttributeError:
        pass
    try:
        output["Style"] = node.style
    except AttributeError:
        pass
    return output


def format_inspection(insp):
    output = ""
    for node in insp:
        output += "".join([f"{k}: {v}".ljust(18) for k, v in node.items()])
        output = output.strip()
        output += "\n"
    return output
