# from debug import snoop


def parse_csv_line(s, sep=","):
    """
    一个更健壮的CSV行解析器，能够处理字段结束后、分隔符前的额外字符。
    返回一个元组列表，每个元组为 (start_index, end_index, kind)。
    kind >= 0 代表数据字段的索引，kind < 0 代表分隔符。
    """
    res = []
    i = 0
    n = len(s)
    field_index = 0

    while i <= n:
        if i == n:
            # 处理行尾可能存在的空字段
            if s.endswith(sep):
                res.append((n, n, field_index))
            break

        start_field = i
        field_has_quotes = False

        # 检查字段是否以引号开头
        if s[i] == '"':
            field_has_quotes = True
            current_pos = i + 1
            while current_pos < n:
                if s[current_pos] == '"':
                    # 检查是否为转义引号 ""
                    if current_pos + 1 < n and s[current_pos + 1] == '"':
                        current_pos += 2  # 跳过转义引号
                    else:
                        # 找到结束引号，跳出内部循环
                        current_pos += 1
                        break
                else:
                    current_pos += 1
            # 找到字段的实际结尾，即下一个分隔符
            next_sep_pos = s.find(sep, current_pos)
        else:
            # 非引用字段，直接找到下一个分隔符
            next_sep_pos = s.find(sep, i)

        if next_sep_pos == -1:
            # 这是最后一个字段
            end_field = n
            i = n + 1  # 结束主循环
        else:
            end_field = next_sep_pos
            i = next_sep_pos + 1

        res.append((start_field, end_field, field_index))
        field_index += 1

        if next_sep_pos != -1:
            res.append((end_field, i, -1))  # 添加分隔符

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
