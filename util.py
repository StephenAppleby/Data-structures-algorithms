def format_nodes(nodes, chars_width):
    # Cull copied nodes with no key. The nodes given here include the empties provided
    # by the fill method
    return (f"{str(n.key):^3}" if n.key != None else " " * chars_width for n in nodes)


def display(tree):
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

    def copy_nodes(original_node, copy_node):
        if original_node.l:
            copy_node.l = tree.BTNode(original_node.l.key)
            copy_nodes(original_node.l, copy_node.l)
        if original_node.r:
            copy_node.r = tree.BTNode(original_node.r.key)
            copy_nodes(original_node.r, copy_node.r)

    copy_root = tree.BTNode(tree.root.key)
    copy_nodes(tree.root, copy_root)
    copy = tree.get_tree(root=copy_root)
    while not copy.is_perfect():
        copy.add(None)

    def depth_node_pairs(depth, node):
        if node.l:
            for d, n in depth_node_pairs(depth + 1, node.l):
                yield (d, n)
        yield (depth, node)
        if node.r:
            for d, n in depth_node_pairs(depth + 1, node.r):
                yield (d, n)

    def lvls(tr):
        output = [[]]
        for depth, node in depth_node_pairs(0, tr.root):
            while len(output) <= depth:
                output.append([])
            output[depth].append(node)
        return output

    levels = lvls(copy)

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
        formatted_nodes = format_nodes(nodes, chars_width)
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
    return format_inspection([inspect_node(node) for node in tree.flatten()])


def inspect_node(node):
    return {
        "Key": node.key,
        "Left": node.l.key if node.l else None,
        "Right": node.r.key if node.r else None,
    }


def format_inspection(insp):
    output = ""
    for node in insp:
        output += "".join([f"{k}: {v}".ljust(14) for k, v in node.items()])
        output = output.strip()
        output += "\n"
    return output
