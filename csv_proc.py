# from debug import snoop


def parse_csv_line(s, sep=","):
    """
    A more robust CSV line parser that can handle extra characters between the end of fields and the preceding delimiter.
    Returns a list of tuples, each being (start_index, end_index, kind).
    kind >= 0 represents the index of a data field, and kind < 0 represents a delimiter.
    """
    res = []
    i = 0
    n = len(s)
    field_index = 0

    while i <= n:
        if i == n:
            # Handle any possible empty fields at the end of the line
            if s.endswith(sep):
                res.append((n, n, field_index))
            break

        start_field = i
        field_has_quotes = False

        # Check if the field starts with a quotation mark
        if s[i] == '"':
            field_has_quotes = True
            current_pos = i + 1
            while current_pos < n:
                if s[current_pos] == '"':
                    # Check if it is an escaped quote ""
                    if current_pos + 1 < n and s[current_pos + 1] == '"':
                        current_pos += 2  # Skip the escaped quotes
                    else:
                        # Find the closing quotation mark and exit the inner loop.
                        current_pos += 1
                        break
                else:
                    current_pos += 1
            # Find the actual end of the field, i.e., the next delimiter.
            next_sep_pos = s.find(sep, current_pos)
        else:
            # Non-quoted field, directly find the next delimiter
            next_sep_pos = s.find(sep, i)

        if next_sep_pos == -1:
            # This is the last field
            end_field = n
            i = n + 1  # End the main loop
        else:
            end_field = next_sep_pos
            i = next_sep_pos + 1

        res.append((start_field, end_field, field_index))
        field_index += 1

        if next_sep_pos != -1:
            res.append((end_field, i, -1))  # Add delimiter

    if not s and n == 0:
        res.append((0, 0, 0))

    return res


# @snoop()
def parse_csv_line_as_dict(s, sep=",", quote='"'):
    """
    Parses one CSV line
    Gets fragments as dict of lists: kind: [offset_start, offset_end]
    Gets {} for incorrect line
    """
    if not s:
        return {}
    # disable quote for TSV
    if sep == "\t":
        quote = chr(1)
    res = {}
    col, x0, b = 0, 0, True
    for x1, c in enumerate(s):
        if c == sep and b:
            res[col] = [x0, x1]
            x0 = x1 + 1
            col += 1
            if x1 + 1 == len(s):
                res[col] = [x1 + 1, x1 + 1]
        elif c == quote:
            b = not b
    if x0 != len(s):
        res[col] = [x0, len(s)]
    if not b:
        return {}
    else:
        return res
    return {}


if __name__ == "__main__":
    print(parse_csv_line_as_dict("aa,,cc"))
    print(parse_csv_line_as_dict(",aa,,cc"))
    print(parse_csv_line_as_dict('"14  aa",,cc,'))
