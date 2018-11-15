#!/usr/bin/python
"""Python script that takes input.txt as input, parses it, and
produces output.txt as output.

Usage: cat input.txt | python script.py > output.txt
"""
from __future__ import print_function
import re
import sys
from collections import OrderedDict

DOT_REGEX = re.compile(r'^(\.+)')
ASTERISK_REGEX = re.compile(r'^(\*+)')


def parse_input_data(data, begins_with='* '):
    """Parses and structures the input ``data`` into an OrderedDict.

    :param iterable data: The input data that needs to be parsed.
    :param str begins_with: A string to identify the begin for line in data.
    :return dict:
    """
    data = iter(data)
    data_dict = OrderedDict()
    values = []
    for raw_line in data:
        if raw_line.startswith(begins_with):
            values = []
            data_dict[raw_line] = values
        else:
            values.append(raw_line)

    return data_dict


def generate_sub_heading(asterisk_count, prev_heading):
    """Generate a sub heading index based on asterisk_count and previous
    heading.

    :param int asterisk_count: Number of asterisk in heading line.
    :param str prev_heading: Previous heading.
    :return str:
    """
    indexes = prev_heading.split('.')
    index_len = len(indexes)

    if index_len < asterisk_count:
        indexes += ['1'] * (asterisk_count - len(indexes))
    elif index_len == asterisk_count:
        indexes[-1] = str(int(indexes[-1]) + 1)

    return '.'.join(indexes)



if __name__ == '__main__':
    stdin_data = [line for line in sys.stdin.readlines() if line.strip()]
    parsed_data = parse_input_data(stdin_data)

    for index, key in enumerate(parsed_data, start=1):
        sys.stdout.write('{}'.format(key.replace('*', str(index))))
        sub_index_count = 1

        if isinstance(parsed_data[key], list):
            d_iter = iter(parsed_data[key])
            prev_count = 0
            prev_sub_index = '{}.{}'.format(index, sub_index_count)

            for i, line in enumerate(d_iter, start=0):
                start_str = ''
                replace_str = ''

                try:
                    next_line = parsed_data[key][i + 1]
                except IndexError:
                    next_line = None

                if line.startswith('.'):
                    start_str = re.search(DOT_REGEX, line).group()
                    count = len(start_str)
                    replace_str = '+' if next_line and next_line.startswith('.') and len(
                        re.search(DOT_REGEX, next_line).group()) > count else '-'
                    prev_count = count
                    indent = '  ' * count

                elif line.startswith('*'):
                    start_str = re.search(ASTERISK_REGEX, line).group()
                    as_count = len(start_str)
                    if as_count == 2:
                        replace_str = '{}.{}'.format(index, sub_index_count)
                        sub_index_count += 1
                    elif as_count > 2:
                        replace_str = generate_sub_heading(
                            as_count, prev_sub_index)
                    prev_sub_index = replace_str
                    indent = ''

                else:
                    indent = '  ' * prev_count * 2

                sys.stdout.write('{}{}'.format(
                    indent, line.replace(start_str, replace_str)))
