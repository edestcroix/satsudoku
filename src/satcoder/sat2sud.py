import fileinput
import sys

from . import decode


def main():
    try:
        fileinput.filename()
        # get the sudoku from stdin
        sudoku = "".join(list(fileinput.input())[1:])
    except (FileNotFoundError, RuntimeError):
        # get from arguments if no input is given
        sudoku = " ".join(sys.argv[1:])

    # print the solved sudoku to stdout
    print(decode(sudoku))


if __name__ == "__main__":
    main()
