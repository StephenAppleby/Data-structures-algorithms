 
def display(tree):
    copy_with_gaps = tree.copy()
    copy_with_gaps.fill(None)
    levels = copy_with_gaps.get_levels()
    output = ""
    for level, nodes in enumerate(levels):
        pad = " "
        row = len(levels) - (level + 1)
        if row != 0:
            pad = " " * ((((2 ** row) - 1) * 3) + (2 ** row))
        half_pad = pad[:len(pad) // 2]
        output += half_pad
        formatted_values = (f"{str(n.value):^3}" if n.value != None else "   " 
                for n in nodes)
        output += pad.join(formatted_values)
        output += '\n'
        if row != 0:
            # ┘ = "\u2518"
            # └ = "\u2514"
            # ┴ = "\u2534"
            # ─ = "\u2500"
            # ┌ = "\u250C"
            # ┐ = "\u2510"
            pad_next = " "
            row -= 1
            if row == -1: row = 0
            if row != 0:
                pad_next = " " * ((((2 ** row) - 1) * 3) + (2 ** row))
            half_pad_next_len = len(pad_next[:len(pad_next) // 2])
            output += half_pad_next_len * " "
            for node in nodes:
                if node.l.value:
                    output += " " + '┌' + '─'
                    output += half_pad_next_len * '─'
                else:
                    output += "   "
                    output += half_pad_next_len * " "
                if node.l.value and not node.r.value:
                    output += '┘'
                if node.l.value and node.r.value:
                    output += '┴'
                if not node.l.value and node.r.value:
                    output += '└'
                if not node.l.value and not node.r.value:
                    output += " "
                if node.r.value:
                    output += half_pad_next_len * '─'
                    output += '─' + '┐' + " "
                else:
                    output += half_pad_next_len * " "
                    output += "   "
                output += pad_next
            output += '\n'
    return output
