# Satsudoku
A sudoku SAT solver

## sud2sat
Converts a sudoku puzzle read from stdin into CNF format and outputs to stdout.
Can parse sudoku puzzles in any format where empty cells are denoted by a consistent character (e.g. `0`, `.`, or `_`), and cells are not separated by anything other than whitespace. `sud2sat` assumes the first non-digit character or `0` it encounters after stripping all whitespace is the empty cell character. Only 9x9 puzzles are supported. Since a large portion of the CNF encoding is identical for every sudoku puzzle, `sud2sat` looks for files containing this portion in `data/`, creating them if not found, and then concatenates them with the puzzle-specific CNF. This means that the first time `sud2sat` is run on a puzzle, it will take longer if `data/` is deleted.
## sat2sud
Converts the satisfiability output from `minisat`, read from stdin, into a solved sudoku puzzle.
Only 9x9 puzzles are supported. The input must be in the format output by `minisat` ran on a CNF file generated by `sud2sat`, and it must be a satisfying assignment. (i.e the starting sudoku puzzle had a solution) A solved puzzle will look like this:  

483 921 657  
967 345 821   
251 876 493   

548 132 976  
729 564 138   
136 798 245   
 
372 689 514   
814 253 769   
695 417 382  

## Benchmarking
The `benchmark` script runs the same encoding functions in `src/` as sud2sat on puzzles from `data/puzzles` and gathers benchmarking data from `minisat` solving these puzzles. It also optionally decodes the solutions from `minisat` into markdown tables and outputs them to files.
### Usage
-  `-s --silent` prevents printing to stdout.
- `-t=[] --test=[]` specify testing standard or hard puzzles, defaults to standard when not specified
- `-e=[] --enc=[]` specify the CNF encoding to use, will default to the minimal encoding when not specified. Can be either minimal, efficient, or extended. (e.g `-e=min` or `-e=extended`)
- `-a --all` tests all encodings with both standard and hard puzzles. Outputs results to `[output]` directory specified in the config.
- `-k --keep` keeps the CNF files generated by sud2sat and the solution encodings from `minisat`. By default, these files are deleted after `minisat` has finished solving them. These will be stored in the `[output]/encodings` and `[output]/solutions` directories, respectively.
- `-S --summarize` can only be used with `-a`. Outputs a summary of the benchmarking results to `[output]/summary.md`. This will contain the averages of decisions, decision rates, propagations, propagation rates, and CPU time for each encoding, for both standard and hard puzzles.
- `-d --decode` decodes the solution encodings from `minisat` into markdown tables and outputs them to `[output]/solutions`. Will output one solution for every solvable input puzzle.
- `-m --markdown` toggles formatting solved sudoku puzzles as markdown tables. This will only work if `-d` is specified.
- `-A --All` is `-a` with `-k -d -S -m` implicitly set, runs the full benchmarking suite, with all outputs generated for all test and encoding types. Specifying any of the other flags will exclude their respective outputs from being generated.
- `-c --clean` deletes all files in the `[output]` directory and exits immediately.
- `-h --help` prints the help message.

### Output
While running, files generated by `sud2sat` and `minisat` will be stored in the `.working` directory. These will be deleted when the script finishes unless the `-k` flag is specified, in which case they will be stored in the `[output]` directory, specified by the config file. The default is `benchmarks`.
All of the output files described below are stored under the `[output]` directory.
- When `-k` is specified, the `encodings` directory will contain CNF encodings for puzzles under `[encoding_type]/[test_type]/`; where `[encoding_type]` is either `minimum` or `efficient` or `extended`, and `[test_type]` is either `standard` or `hard`; the solution encodings from `minisat` will be stored in `sat/[test_type]`. Solution encodings are not generated for each encoding type, as the encoding type does not affect the solution.
- When `-d` is specified, the `solutions` directory will contain the decoded solutions from `minisat`. When `-S` is specified, the `summary.md` file will contain the summary of the benchmarking results.
- When `-a` is specified, a file `[##]-[test_type]-[encoding_type].md` file will be created for each test type and encoding type, numbered in the order the tests were run. These files will contain select output from `minisat` for each puzzle, and the summary of the benchmarking results for each test. The `summary.md` file will contain the summary of the benchmarking results for each encoding and test type when `-S` is specified. Additionally, the `encodings` directory will contain `[encoding_type]/[test_type]/` and `sat/[test_type]` for each encoding and test type when `-k` is specified.
- If `-d` is specified, the decoded solutions for each test can be found in the `solutions/[test_type]` directory. Solutions are not generated for each encoding, as the encoding type does not affect the solution.
- If `-S` is specified, the `summary.md` file will contain the summary of the benchmarking results for each encoding and test type.
- If `-m` is specified, the decoded solutions will be formatted as markdown tables. This will only work if `-d` is specified.
- When `-A` is specified, all the outputs from `-a -k -d -S -m` will be generated, unless any of these flags other than `-a` are specified. In this case, the outputs from those flags will not be generated. For example `-A -d` will generate all outputs except the decoded solutions, while `-d` will generate only the decoded solutions. Similar to when called without `-A`, specifying `-A -d` will not generate the decoded solutions even though `-m` is implicitly specified by `-C`, because `-m` only applies when solutions are being decoded. `-a` cannot be negated with `-A`, as `-A` is an extension of `-a`.

### Configuration
The configuration file is located at `config.json`. The following options are available:
- `resultsDir` is the directory where benchmarking results will be stored. Defaults to `benchmarks`.
- `puzzleDir` is the directory where puzzle files are stored. Defaults to `data/puzzles`.
- `cacheDir` is the directory where CNF encodings will be temporarily stored while benchmarking. Defaults to `.cache`.
- `round` is the number of decimal places to round benchmarking results to. Defaults to 2.
- `defaultPuzzleSet` specifies the default puzzle set to use when running `benchmark` with no arguments. Defaults to `standard`.
- `puzzleSets` for defining test parameters for puzzle sets. See below for more information.

### Custom Tests

Tests may be added by adding a new file containing puzzles to the `data/puzzles/` directory and configuring it in `config.json` by adding it to the `puzzles` array, with the key being the name of the test. A puzzle entry is of the following format:
```
"test_name": {
    "path": "path/to/puzzle/file",
    "numPuzzles": 100,
    "size": 9,
    "offset": 0
}
```
- `test_name` is the name of the test to be used as an identifier internally and in the output. Tests must have unique names.
- `path` is the path to the puzzle file, relative to the `puzzleDir` directory specified in `config.json`.
- `numPuzzles` is the number of puzzles in the file.
- `size` is how many lines the puzzle occupies in the file. This should be either 1 or 9, as any other way of storing puzzles has not been tested, and probably won't work. (I.e, 1-line puzzles have a full 9x9 sudoku puzzle but with no whitespace, and 9-line puzzles are a 9x9 sudoku puzzle with each row on a separate line.) 
- `offset` is the number of lines between the puzzles. Useful for puzzles that have a line between each puzzle, or puzzles that have a header line. Note that this is only lines between puzzles, not lines between rows of a puzzle. It is best to have 9-line puzzles formatted so that the 9 lines are sequential, with no lines in between; even though whitespace is ignored, unexpected behavior may occur if there are lines in between the rows, as the parser has not been tested with this format.

In theory, any set of 1-line or 9-line puzzles should work; the "medium" tests were added after the benchmarker was reworked to generalize over any puzzle sets and it worked without issue, but no other sets have been tested yet, so look out for potential bugs when adding puzzle sets.
  
## Dependencies
- python3.11 or later (may work with earlier versions, but has not been tested)
- [minisat](http://minisat.se/) (tested with version 2.2.1). The scripts in this repo just call `minisat` as a shell command, so it must be installed and available in `$PATH`
## Sources
Puzzles in /data/puzzles taken from:
- https://projecteuler.net/project/resources/p096_sudoku.txt

- http://magictour.free.fr/top95

- https://github.com/grantm/sudoku-exchange-puzzle-bank
