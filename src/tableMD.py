'''This module contains a function to format output as markdown tables.'''

'''This function creates a markdown table.
Args:
    title (str): The title of the table. This is printed once as a level 1 header at the top of the table.
    rows (list): A list of lists. Each inner list represents a row in the table. Each element in the inner list is a cell in the table.
    col_titles (list): A list of strings. Each string is the title of a column in the table.
    sep_every (int): The number of rows between separators. At each interval, a separator is printed, used in
                     combination with sep_func to break data into multiple tables. (I.e instead of calling this function
                     multiple times, call it once and use sep_every and sep_func to break the data into multiple tables.)
                     For best results, data in rows should have 'sep_every' rows per desired table.
    sep_func (function): A function to generate table separators. The function should take a single argument, the number
                         of the separator, and return a string. (E.g if outputting multiple test results, the function
                         could be lambda n: f"Test {n}"). Do not put markdown header tags in the output:
                         they are added automatically.
    new_line (bool): Whether to add a new line after the last line of the output.
    sep (bool): Whether to add separators between rows. If False, col_titles, sep_every, and sep_func are ignored
                and the first row is used as the column titles.
                
Returns:
    a formatted markdown table, or a sequence of markdown tables, as a string.
'''


def create(title, rows, col_titles=None, sep_every=3, sep_func=None, new_line=True, sep=True):
    # find the longest string in each column
    col_widths = [max(len(str(x)) for x in col)
                  for col in zip(*rows + [col_titles])] \
        if sep else [max(len(str(x)) for x in col) for col in zip(*rows)]
    out = f"# {title}\n"
    sep_count = 0
    sep_line = "|-" + "-|-".join("-" * n for n in col_widths) + "-|" + "\n"

    for i, row in enumerate(rows):
        if sep and i % sep_every == 0:
            sep_count += 1
            out += __table_sep(sep_count, sep_func,
                               sep_line, col_widths, col_titles)
        elif not sep and i == 1:
            out += sep_line

        out += "| " + " | ".join((str(x).ljust(col_widths[j])
                                  for j, x in enumerate(row))) + " |\n"

    if new_line:
        out += "\n"
    return out


def __table_sep(sep_count, sep_func, sep_line, col_widths, col_titles):
    out = ""
    # when a separator of some kind is defined
    # (either a header or a function)
    # print the separator at the interval specified by sep_every
    if sep_func != None:
        # the header is generated by the function
        # passed as an argument to sep_func
        # (this is so that the header can be dynamic)
        head = sep_func(sep_count)

        sep_header = (
            f"## {head.ljust(sum(col_widths) + 3 * (len(col_widths) - 1))}"
            + "\n\n"
        )
        out += "\n"+sep_header if sep_count > 1 else sep_header
    # if there are no column titles, and no separator function
    # a separator line needs to be printed
    if sep_func is None:
        out += sep_line

    out += "| " + " | ".join((str(x).ljust(col_widths[j])
                              for j, x in enumerate(col_titles))) + " |\n"
    out += sep_line
    return out
