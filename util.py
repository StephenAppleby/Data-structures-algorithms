def format_nodes(nodes, chars_width, item="key"):
    # Cull copied nodes with no key. The nodes given here include the empties provided
    # by the fill method
    if item == "key":
        return (
            f"{str(n.key):^3}" if n.key != None else " " * chars_width for n in nodes
        )
    if item == "depths":
        return (
            f"{str(n.depth):^3}" if n.key != None else " " * chars_width for n in nodes
        )
    if item == "heights":
        return (
            f"{str(n.height):^3}" if n.key != None else " " * chars_width for n in nodes
        )


def display(tree, item="key"):
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
    output = ""
    # Copy the tree and fill
    copy_with_gaps = tree.copy()
    # Fill with empties. The fill method returns a perfect tree
    # which makes it much easier to format later
    copy_with_gaps.fill(None)
    # Now we have to carefully recalculate the height of each node to make sure that
    # our full tree still looks empty
    if item == "heights":
        leaves = []
        for node in copy_with_gaps.flatten():
            is_leaf = True
            if not node.key:
                is_leaf = False
            if node.l:
                if node.l.key:
                    is_leaf = False
            if node.r:
                if node.r.key:
                    is_leaf = False
            if is_leaf:
                leaves.append(node)
        for leaf in leaves:
            leaf.height = 0
            leaf.recalc_parent_heights()
    # We'll be iterating over each level of the tree starting from depth = 0
    levels = copy_with_gaps.get_levels()
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
        formatted_nodes = format_nodes(nodes, chars_width, item)
        output += pad.join(formatted_nodes)
        output = output.rstrip()
        # Add the pipes after each level except the last
        if inv_row != 0:
            # ┘ = "\u2518"
            # └ = "\u2514"
            # ┴ = "\u2534"
            # ─ = "\u2500"
            # ┌ = "\u250C"
            # ┐ = "\u2510"
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
                if node.l.key != None:
                    output += " " + "┌" + "─"
                    output += len(half_pad) * "─"
                else:
                    output += "   "
                    output += len(half_pad) * " "
                if node.l.key != None and not node.r.key != None:
                    output += "┘"
                if node.l.key != None and node.r.key != None:
                    output += "┴"
                if not node.l.key != None and node.r.key != None:
                    output += "└"
                if not node.l.key != None and not node.r.key != None:
                    output += " "
                if node.r.key != None:
                    output += len(half_pad) * "─"
                    output += "─" + "┐" + " "
                else:
                    output += len(half_pad) * " "
                    output += "   "
                # Add padding to each set of pipes except the last
                if n != len(nodes) - 1:
                    output += pad
            output = output.rstrip()
            output += "\n"
    return output


def inspect(tree):
    return [inspect_node(node) for node in tree.flatten()]


def inspect_node(node):
    return {
        "Key": node.key,
        "Left": node.l.key if node.l else None,
        "Right": node.r.key if node.r else None,
        "Parent": node.parent.key if node.parent else None,
        "Side": node.side,
        "Height": node.height,
        # "Depth": node.depth,
    }
