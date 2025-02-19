# Sudoku-evaluating-program

This project was developed as part of a two-part article that appeared in c't and on heise+. The basic idea is to evaluate Sudokus based on the used Strategies.

There are two files:

- `evaluate_sudoku.py` contains the whole Project. Implemented are naked Single, hidden Single, naked Pair, hidden Pair, pointing Pair and X-Wing.
- `evaluate_sudoku_small.py` is a smaller version that contains just naked Single and hidden Single, that are the Topic from the first Article.

## Usage

To evaluate a Sudoku you can change the `board`-variable inside the Program oder use `board-import` to convert a string like 040300000000000100007000546000702419080400020000009000000030060500006081030500000 to a 2D-array. The example Sudoku looks like that:

![sudoku-20250218T175248](https://github.com/user-attachments/assets/00e60298-b91f-4d69-be3f-16a7813620e7)

The Program always tries the easiest strategy before jumping to the next difficult one. When evaluating, it outputs a log of the solution like this one for the example sudoku:
```
Hidden Single found: 3 at [2, 0]
Hidden Single found: 3 at [3, 2]
Hidden Single found: 8 at [3, 4]
Hidden Single found: 3 at [4, 5]
Hidden Single found: 5 at [5, 7]
Hidden Single found: 5 at [6, 8]
Hidden Single found: 3 at [7, 6]
Hidden Single found: 4 at [8, 8]
Single found: 6 at [3, 0]
Single found: 5 at [3, 1]
Single found: 7 at [4, 8]
Single found: 6 at [4, 6]
Single found: 8 at [5, 6]
Single found: 3 at [5, 8]
Hidden Single found: 6 at [1, 1]
Hidden Single found: 3 at [1, 7]
Hidden Single found: 5 at [4, 4]
Hidden Single found: 6 at [5, 3]
Hidden Single found: 1 at [5, 4]
Hidden Single found: 6 at [8, 2]
Hidden Single found: 6 at [0, 4]
Naked Pair 28 found at [0, 8] and [1, 8], removed 1 candidates
Naked Pair 79 found at [0, 6] and [0, 7], removed 3 candidates
Hidden Pair 47 found at [1, 4] and [1, 5], removed 4 candidates
Hidden Single found: 5 at [0, 5]
Hidden Single found: 5 at [1, 2]
Hidden Pair 18 found at [8, 0] and [8, 5], removed 4 candidates
Naked Pair 18 found at [2, 5] and [8, 5], removed 2 candidates
Hidden Pair 47 found at [5, 0] and [6, 0], removed 5 candidates
Naked Pair 47 found at [6, 0] and [6, 5], removed 3 candidates
Pointing Pair '1' found at [1, 3, 5] in row 2, removed 1 candidates
Hidden Single found: 1 at [6, 1]
Hidden Single found: 1 at [8, 5]
Single found: 8 at [2, 5]
Single found: 8 at [8, 0]
Hidden Single found: 8 at [0, 2]
Hidden Single found: 8 at [1, 8]
Hidden Single found: 1 at [2, 3]
Hidden Single found: 1 at [4, 2]
Hidden Single found: 8 at [6, 3]
Single found: 2 at [0, 8]
Single found: 9 at [4, 0]
Single found: 1 at [0, 0]
Single found: 2 at [1, 0]
Single found: 9 at [1, 3]
Single found: 9 at [2, 1]
Single found: 2 at [2, 4]
Single found: 2 at [7, 3]
Single found: 7 at [7, 1]
Single found: 2 at [5, 1]
Single found: 4 at [5, 2]
Single found: 4 at [6, 0]
Single found: 7 at [6, 5]
Single found: 9 at [7, 2]
Single found: 4 at [7, 4]
Single found: 9 at [8, 4]
Single found: 7 at [8, 7]
Single found: 9 at [0, 7]
Single found: 7 at [1, 4]
Single found: 4 at [1, 5]
Single found: 7 at [5, 0]
Single found: 2 at [6, 2]
Single found: 9 at [6, 6]
Single found: 2 at [8, 6]
Single found: 7 at [0, 6]
{'Naked Single': 33, 'Hidden Single': 24, 'Naked Pair': 4, 'Hidden Pair': 3, 'Pointing Pair': 1, 'X-Wing': 0}
Score: 4.228070175438597
1 4 8 3 6 5 7 9 2
2 6 5 9 7 4 1 3 8
3 9 7 1 2 8 5 4 6
6 5 3 7 8 2 4 1 9
9 8 1 4 5 3 6 2 7
7 2 4 6 1 9 8 5 3
4 1 2 8 3 7 9 6 5
5 7 9 2 4 6 3 8 1
8 3 6 5 9 1 2 7 4
```

If it cant solve the Sudoku it outputs the current state of the Sudoku.

## Copyright


Copyright ©️ 2025 Wilhelm Drehling, Heise Medien GmbH & Co. KG

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
