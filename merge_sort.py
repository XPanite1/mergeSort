import itertools
import heapq
import numpy as np
import os
import string
import tempfile
import typing as tp


def merge_generators(rows1: tp.Iterator[str], rows2: tp.Iterator[str]) -> tp.Iterator[str]:
    """
    Merge sort
    :param rows1: sorted lines by first iterator
    :param rows2: sorted lines by second iterator
    :return:  merged sorted lines
    """
    row1 = next(rows1, None)
    row2 = next(rows2, None)
    while row1 is not None and row2 is not None:
        if row1 < row2:
            yield row1
            row1 = next(rows1, None)
        else:
            yield row2
            row2 = next(rows2, None)
    if row1 is not None:
        yield row1
    if row2 is not None:
        yield row2
    yield from itertools.chain(rows1, rows2)
    return


def merge_sort(filepath1: str, filepath2: str, res_filepath: str):
    """
    Sort two files using merge sort to third file
    :param filepath1: path of first file
    :param filepath2: path of second file
    :param res_filepath: result file
    :return:
    """
    with open(filepath1) as rows1:
        with open(filepath2) as rows2:
            with open(res_filepath, 'w') as res_f:
                for line in merge_generators(rows1, rows2):
                    res_f.write(line)


def merge_several_files(file_path_to_length: tp.Dict[str, int], res_filepath: str) -> None:
    """
    Merge several sorted files to one using merge sort
    :param file_path_to_length: dict from file paths to their length (all files are sorted)
    :param res_filepath: output file with sorted lines
    :return:
    """
    assert len(file_path_to_length) > 0
    file_length_with_paths = [(length, name) for name, length in file_path_to_length.items()]
    heapq.heapify(file_length_with_paths)
    with tempfile.TemporaryDirectory() as tmp_dir:
        max_file_id = 0
        while len(file_length_with_paths) >= 2:
            length_with_path1 = heapq.heappop(file_length_with_paths)
            length_with_path2 = heapq.heappop(file_length_with_paths)
            join_filepath = tmp_dir + "/" + str(max_file_id)
            max_file_id += 1
            merge_sort(length_with_path1[1], length_with_path2[1], join_filepath)
            heapq.heappush(file_length_with_paths, (length_with_path1[0] + length_with_path2[0], join_filepath))
        os.rename(file_length_with_paths[0][1], res_filepath)


def sort_file(input_file: str, output_file: str, max_lines_in_memory=2) -> None:
    """
    Sort big file in O(N*log N)
    :param input_file: input file without order
    :param output_file: output file with sorted lines
    :param max_lines_in_memory: max number of lines fit in memory
    :return:
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        max_file_id = 0
        file_lengths = {}
        with open(input_file, 'r') as f:
            iter_for_files = itertools.groupby(
                map(lambda x: (x[0] // max_lines_in_memory, x[1]), enumerate(f)),
                key=lambda x: x[0])
            for num, iterByNum in enumerate(iter_for_files):
                lines_for_small_file = [numWithLine[1] for numWithLine in iterByNum[1]]
                small_filename = tmp_dir + "/" + str(max_file_id)
                max_file_id += 1
                file_lengths[small_filename] = len(lines_for_small_file)
                with open(small_filename, 'w') as small_f:
                    for line in sorted(lines_for_small_file):
                        small_f.write(line)
            merge_several_files(file_lengths, output_file)


def generate_file(path, line_count=1000, line_length=100):
    letters = string.ascii_lowercase
    with open(path, 'w') as f:
        for line in range(line_count):
            rand = np.random.randint(low=0, high=len(letters), size=line_length)
            line = "".join(letters[r] for r in rand)
            print(line, file=f)
