# Sudoku-evaluating-program

This project was developed as part of a two-part article that appeared in c't and on heise+. The basic idea is to evaluate Sudokus based on the used Strategies.

There are two files:

- `evaluate_sudoku.py` contains the whole Project. Implemented are naked Single, hidden Single, naked Pair, hidden Pair, pointing Pair and X-Wing. To evaluate a Sudoku, call the programm and pass the Sudoku as a string as follows: `python3 evaluate_sudoku.py 040300000000000100007000546000702419080400020000009000000030060500006081030500000`
- `evaluate_sudoku_small.py` is a smaller version that contains just naked Single and hidden Single, that are the Topic from the first Article. To evaluate a Sudoku you can change the `board`-variable inside the Program oder use `board-import` to convert a string to a 2D-array. 

## Copyright

Copyright ©️ 2025 Wilhelm Drehling, Heise Medien GmbH & Co. KG

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
