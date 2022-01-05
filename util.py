 
def display(tree):
    """
    Renders a binary tree to the console in a human readable format.

    This function is designed to display small binary trees for demonstration
    purposes only. It assumes that the value of each node will be no more than
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
    # We'll be iterating over each level of the tree starting from depth = 0
    levels = copy_with_gaps.get_levels()
    for level, nodes in enumerate(levels):
        # The amount of padding is inversely proportional to level depth
        inv_row = len(levels) - (level + 1)
        gap = 2 ** inv_row
        # We assume that each value to be represented will be no more than
        # three chars long
        chars_width = 3
        pad = " " if inv_row == 0 else " " * (((gap - 1) * chars_width) + gap)
        # We will need to add half of the padding between each node to the
        # front of the row to space it out correctly
        half_pad = pad[:len(pad) // 2]
        output += half_pad
        # Ensure that we have the string value of each node to three chars
        # or the same amount of spaces
        formatted_values = (
                f"{str(n.value):^3}" 
                if n.value != None 
                else " " * chars_width
                for n in nodes)
        output += pad.join(formatted_values)
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
            output += '\n'
            # We'll need to do a similar process for padding as before but
            # with the inv_row value of the following level
            inv_row -= 1
            if inv_row == -1: inv_row = 0
            gap = 2 ** inv_row
            pad = " " if inv_row == 0 else \
                    " " * (((gap - 1) * chars_width) + gap)
            half_pad = pad[:len(pad) // 2]
            output += half_pad
            # Assign the appropriate pipes if child present and spaces if not
            for n, node in enumerate(nodes):
                if node.l.value != None:
                    output += " " + '┌' + '─'
                    output += len(half_pad) * '─'
                else:
                    output += "   "
                    output += len(half_pad) * " "
                if node.l.value != None and not node.r.value != None:
                    output += '┘'
                if node.l.value != None and node.r.value != None:
                    output += '┴'
                if not node.l.value != None and node.r.value != None:
                    output += '└'
                if not node.l.value != None and not node.r.value != None:
                    output += " "
                if node.r.value != None:
                    output += len(half_pad) * '─'
                    output += '─' + '┐' + " "
                else:
                    output += len(half_pad) * " "
                    output += "   "
                # Add padding to each set of pipes except the last
                if n != len(nodes) - 1:
                    output += pad
            output = output.rstrip()
            output += '\n'
    return output
