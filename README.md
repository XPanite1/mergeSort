# Python3 merge sort for big files

usage: merge_sort.py [-h]
                     input output [max_line_merge_count] [line_count]
                     [line_length]

Sort big files

positional arguments:
  input                 input file path, generate if it's not exists
  output                output file path
  max_line_merge_count  max lines count that fit in memory
  line_count            line count for generating
  line_length           line length for generating

optional arguments:
  -h, --help            show this help message and exit