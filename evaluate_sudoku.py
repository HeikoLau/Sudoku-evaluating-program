#!/usr/bin/env python3

import itertools
from collections import Counter

class Sudoku:
    def __init__(self, board):
        self.board = board
        self.candidates = self.find_all_candidates()

    # main evaluate function
    def evaluate(self):
        score = {"Naked Single":0, "Hidden Single":0, "Naked Pair":0, "Hidden Pair":0, "Pointing Pair":0, "X-Wing":0}
        original_empty_cells = self.count_empty_cells()
        print(self.candidates)

        # solve Sudoku until no more strategies can be applied
        while(self.count_empty_cells() > 0):
            # To track if any progress is made
            progress = False

            # First try Naked Single
            solved_count = self.find_naked_single()
            if solved_count > 0:
                score["Naked Single"] += solved_count
                progress = True

            # Then try Hidden Single
            if not progress:
                solved_count = self.find_hidden_single()
                if solved_count > 0:
                    score["Hidden Single"] += solved_count
                    progress = True

            # If no progress was made, try Naked Pair
            if not progress:
                solved_count = self.find_naked_pair()
                if solved_count > 0:
                    score["Naked Pair"] += solved_count
                    progress = True

            # If no progress was made, try Hidden Pair
            if not progress:
                solved_count = self.find_hidden_pair()
                if solved_count > 0:
                    score["Hidden Pair"] += solved_count
                    progress = True

            # If no progress was made, try pointing pairs
            if not progress:
                solved_count = self.find_pointing_pair()
                if solved_count > 0:
                    score["Pointing Pair"] += solved_count
                    progress = True

            # If no progress was made, try x-wing
            if not progress:
                solved_count = self.find_x_wing()
                if solved_count > 0:
                    score["X-Wing"] += solved_count
                    progress = True

            # If no progress is made by any strategy, break out of the loop
            if not progress:
                print(self.candidates)
                print("Unknown Strategy needed to solve Sudoku")
                break

        # calculate score
        print(score)
        return (score["Naked Single"] + (score["Hidden Single"] * 2) + (score["Naked Pair"] * 15) + (score["Hidden Pair"] * 25) + (score["Pointing Pair"] * 25) + (score["X-Wing"] * 40))/original_empty_cells

    # method solves cells with a hidden unique single
    def find_hidden_single(self):
        solved = 0
        for row in range(9):
            for column in range(9):
                for number in self.candidates[row][column]:
                    if self.number_is_unique(row, column, number):
                        print(f"Hidden Single found: {number} at [{row}, {column}]")
                        self.board[row][column] = number
                        #remove candidates from other cells because of the addition of a number
                        self.candidates[row][column] = ''
                        self.remove_candidates_after_number_set(row, column, number)
                        solved += 1
                        # number found so try to continue with naked single
                        break
        return solved

    # Solve every cell with a single candidate
    def find_naked_single(self):
        solved = 0
        for row in range(9):
            for column in range(9):
                if len(self.candidates[row][column]) == 1:
                    print(f"Single found: {self.candidates[row][column]} at [{row}, {column}]")
                    self.board[row][column] = int(self.candidates[row][column])
                    #remove candidates because of the addition of a number
                    self.remove_candidates_after_number_set(row, column, self.candidates[row][column])
                    solved += 1
        return solved

    # Find naked pairs that delete candidates
    def find_naked_pair(self):
        for row in range(9):
            for column in range(9):
                # find first naked pair
                if len(self.candidates[row][column]) == 2:
                    # find a second pair
                    pair_row, pair_col = self.get_second_naked_pair(self.candidates[row][column], row, column)
                    # if no second pair is found, skip
                    if pair_row is None:
                        continue
                    # trying to remove candidates
                    removed = self.remove_candidates_naked_pair(row, column, pair_row, pair_col, self.candidates[row][column])
                    # only if candidates could be deleted because of a naked pair it counts to the difficulty 
                    if removed > 0:
                        print(f"Naked Pair {self.candidates[row][column]} found at [{row}, {column}] and [{pair_row}, {pair_col}], removed {removed} candidates")
                        return 1
        return 0

    # finds a hidden pair
    def find_hidden_pair(self):
        # Generate all possible pairs
        pairs = [''.join(pair) for pair in itertools.combinations('123456789', 2)]
        # try to find one hidden pair
        for row in range(9):
            for column in range(9):
                for pair in pairs:
                    if self.pair_is_in_cell(pair, row, column) and self.pair_is_unique(pair, row, column):
                        # try to find a potential second pair to form a hidden pair
                        row_pair, col_pair = self.get_second_hidden_pair(pair, row, column)
                        # if no second pair is found continue with the next cell
                        if row_pair is None:
                            continue

                        # if second pair to form the hidden pair isn't unique continue with next cell
                        if not self.pair_is_unique(pair, row_pair, col_pair):
                            continue

                        # check if the potential hidden pair is not accidently a naked pair
                        if len(self.candidates[row][column]) == 2 and len(self.candidates[row_pair][col_pair]) == 2:
                            continue

                        # remove candidates from hidden pair cell, so hidden pair is transformed to a naked pair
                        removed = len(self.candidates[row][column]) + len(self.candidates[row_pair][col_pair]) - 4
                        self.candidates[row][column] = pair
                        self.candidates[row_pair][col_pair] = pair
                        # continue like it is a normal naked pair
                        removed += self.remove_candidates_naked_pair(row, column, row_pair, col_pair, pair)
                        print(f"Hidden Pair {self.candidates[row][column]} found at [{row}, {column}] and [{row_pair}, {col_pair}], removed {removed} candidates")
                        return 1
        return 0

    # finds pointing pairs so it can delete candidates in a row or column (intersection method)
    def find_pointing_pair(self):
        removed = 0
        # iterate through every box
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                # create a smaller list just for the box
                box_values = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        box_values.append(self.candidates[r][c])
                # flatten the box to see easier how often numbers appear in a box
                box_values = ''.join(box_values)

                # 1. search every row in a box
                for r in range(box_row, box_row + 3):
                    # flatten the row and count how often a number appear in a row
                    row_values = ''.join(self.candidates[r][box_col:box_col + 3])
                    count = Counter(row_values)
                    # check every number
                    for num in '123456789':
                        # if the number just appears two times in a row, but not in the rest of the box
                        if count[num] == 2 and count[num] == box_values.count(num):
                            # track coordinates of all occurrences of num in the row
                            positions = []
                            for position_col in range(9):
                                if num in self.candidates[r][position_col]:
                                    positions.append(position_col)

                            # delete this number from the rest of the row (outside our box)
                            for position_col in positions:
                                if position_col < box_col or position_col >= box_col + 3:
                                    self.candidates[r][position_col] = self.candidates[r][position_col].replace(num, '')
                                    removed += 1
                            # check if candidates could be deleted because of the pointing pair
                            if removed > 0:
                                print(f"Pointing Pair '{num}' found at {positions} in row {r}, removed {removed} candidates")
                                return 1
                                
                            
                # 2. search for column
                for c in range(box_col, box_col + 3):
                    # flatten the column
                    col_values = ''.join(self.candidates[r][c] for r in range(box_row, box_row + 3))
                    count = Counter(col_values)
                    # checking every number in column
                    for num in '123456789':
                        # if the number just appears two times in a column, bot not in the rest of the box
                        if count[num] == 2 and count[num] == box_values.count(num):
                            # track coordinates of all occurrences of num in the row
                            positions = []
                            for position_row in range(9):
                                if num in self.candidates[position_row][c]:
                                    positions.append(position_row)

                            # delete this number from the rest of the column (outside our box)
                            for position_row in positions:
                                if position_row < box_row or position_row >= box_row + 3:
                                    self.candidates[position_row][c] = self.candidates[position_row][c].replace(num, '')
                                    removed += 1
                            # check if candidates could be deleted because of the pointing pair
                            if removed > 0:
                                print(f"Pointing Pair '{num}' found at {positions} in column {c}, removed {removed} candidates")
                                return 1                        

        return removed

    def find_x_wing(self):
        removed = 0
        # iterate over all possible numbers (1-9)
        for num in '123456789':
            # 1. Search for a row-based X-Wing
            for row1 in range(9):
                for row2 in range(row1 + 1, 9):  # Make sure we're looking at two different rows
                # find columns where num appears in both row1 and row2
                    cols_row1 = []
                    cols_row2 = []
                
                    # scan col1
                    for col in range(9):
                        if num in self.candidates[row1][col]:
                            cols_row1.append(col)
                                
                    # scan col2
                    for col in range(9):
                        if num in self.candidates[row2][col]:
                            cols_row2.append(col)

                    # If num appears exactly twice in both rows and in the same columns
                    if len(cols_row1) == 2 and len(cols_row2) == 2:
                    # Check for X-Wing pattern: same columns in both rows
                        if cols_row1 == cols_row2:
                            for r in range(9):
                                if r != row1 and r != row2:
                                    # We have found an X-Wing, now eliminate the number from other places in the columns
                                    # Eliminate num from other rows in the same columns
                                    for col in cols_row1:
                                        if num in self.candidates[r][col]:
                                            self.candidates[r][col] = self.candidates[r][col].replace(num, '')
                                            removed += 1
                                    for col in cols_row2:
                                        if num in self.candidates[r][col]:
                                            self.candidates[r][col] = self.candidates[r][col].replace(num, '')
                                            removed += 1

                    # Check if any candidates were removed
                    if removed > 0:
                        print(f"X-Wing found for number {num} between rows {row1} and {row2}, removed {removed} candidates.")
                        return 1  # Indicating that we found and applied the X-Wing

            # 2. Search for column-based X-Wing
            for col1 in range(9):
                for col2 in range(col1 + 1, 9):  # Make sure we're looking at two different columns
                    # Find rows where num appears in both col1 and col2
                    rows_col1 = []
                    rows_col2 = []
                    
                    # Scan col1
                    for row in range(9):
                        if num in self.candidates[row][col1]:
                            rows_col1.append(row)
                                
                    # Scan col2
                    for row in range(9):
                        if num in self.candidates[row][col2]:
                            rows_col2.append(row)

                    # If num appears exactly twice in both columns and in the same rows
                    if len(rows_col1) == 2 and len(rows_col2) == 2:
                        # Check for X-Wing pattern: same rows in both columns
                        if rows_col1 == rows_col2:
                            for c in range(9):
                                if c != col1 and c != col2:
                                    # We have found an X-Wing, now eliminate the number from other places in the rows
                                    # Eliminate num from other columns in the same rows
                                    for row in rows_col1:
                                        if num in self.candidates[row][c]:
                                            self.candidates[row][c] = self.candidates[row][c].replace(num, '')
                                            removed += 1
                                    for row in rows_col2:
                                        if num in self.candidates[row][c]:
                                            self.candidates[row][c] = self.candidates[row][c].replace(num, '')
                                            removed += 1

                        # Check if any candidates were removed
                        if removed > 0:
                            print(f"X-Wing found for number {num} in columns {col1} and {col2}, removed {removed} candidates.")
                            return 1  # Indicating that we found and applied the X-Wing
        return 0  # No X-Wing pattern found or no X-Wing with deletion of candidates

    # function tries to find a viable candidate pair to form a naked pair
    def get_second_naked_pair(self, pair, row, column): 
        # second list to find the coordinates from the second pair
        row_pair = column_pair = None
        row_count = col_count = box_count = 0
        # search for a pair in row or column except of our first pair, save the find
        for i in range(9):
            if i != column and self.candidates[row][i] == pair:
                row_count += 1
                row_pair = row
                column_pair = i
        if row_count == 1:
            return row_pair, column_pair
        
        for i in range(9):
            if i != row and self.candidates[i][column] == pair:
                col_count += 1
                row_pair = i
                column_pair = column
        if col_count == 1:
            return row_pair, column_pair


        # Check if the pair is maybe in the 3x3 box and not in a row or column
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                # check all cells except the one from the pair
                if self.candidates[i + start_row][j + start_column] == pair and ((i + start_row != row) and (j + start_column != column)):
                    box_count += 1
                    row_pair = i + start_row
                    column_pair = j + start_column
        if box_count == 1:
            return row_pair, column_pair

        return row_pair, column_pair

    # remove candidates because of a naked pair
    def remove_candidates_naked_pair(self, row1, col1, row2, col2, pair):
        removed = 0
        # Remove the naked pair digits from other cells in the same row and column
        for r in range(9):
            for c in range(9):
                # Skip the naked pair cells
                if (r == row1 and c == col1) or (r == row2 and c == col2):
                    continue

                # Check row and column
                if (r == row1 and r == row2) or (c == col1 and c == col2):
                    for digit in pair:
                        if digit in self.candidates[r][c]:
                            self.candidates[r][c] = self.candidates[r][c].replace(digit, '')
                            removed += 1

        # Only remove from the 3x3 subgrid if the naked pair cells are in the same box
        box_row_start1 = (row1 // 3) * 3
        box_col_start1 = (col1 // 3) * 3
        box_row_start2 = (row2 // 3) * 3
        box_col_start2 = (col2 // 3) * 3
        if (box_row_start1 == box_row_start2) and (box_col_start1 == box_col_start2):
        # Cells are in the same 3x3 box, so we can remove candidates from this box
            for r in range(box_row_start1, box_row_start1 + 3):
                for c in range(box_col_start1, box_col_start1 + 3):
                    # Skip the naked pair cells
                    if (r == row1 and c == col1) or (r == row2 and c == col2):
                        continue

                    # Remove candidates from the subgrid
                    for digit in pair:
                        if digit in self.candidates[r][c]:
                            self.candidates[r][c] = self.candidates[r][c].replace(digit, '')
                            removed += 1

        return removed


    def get_second_hidden_pair(self, pair, row, column):    
        # second list to find the coordinates from the second pair
        row_pair = column_pair = None
        row_count = col_count = box_count = 0
        # search for a pair in row or column except of our first pair, save the find
        for i in range(9):
            if (i != column and self.pair_is_in_cell(pair, row, i)):
                col_count += 1
                row_pair = row
                column_pair = i
        if col_count == 1:
            return row_pair, column_pair

        for i in range(9):
            if (i != row and self.pair_is_in_cell(pair, i, column)):
                row_count += 1
                row_pair = i
                column_pair = column
        if row_count == 1:
            return row_pair, column_pair

        # Check if the pair is maybe in the 3x3 box and not in a row or column
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if (((i + start_row != row) and (j + start_column != column)) and self.pair_is_in_cell(pair, i + start_row, j + start_column)):
                    box_count += 1
                    row_pair = i + start_row
                    column_pair = j + start_column

        if box_count == 1:
            return row_pair, column_pair

        return None, None

    # helper function to identify if the pair occur in the cell
    def pair_is_in_cell(self, pair, row, column):
        if pair[0] in self.candidates[row][column] and pair[1] in self.candidates[row][column]:
            return True
        return False

    # helper function to identify if digits of the pair occur in the cell
    def digit_of_pair_is_in_cell(self, pair, row, column):
        if pair[0] in self.candidates[row][column] or pair[1] in self.candidates[row][column]:
            return True
        return False

    # helper function to identify if a pair is truly unique in a row, column or box
    def pair_is_unique(self, pair, row, column):
        # check row and column
        row_count = col_count = box_count = 0
        for i in range(9):
            if self.digit_of_pair_is_in_cell(pair, row, i):
                row_count += 1
        if row_count == 2:
            return True

        for i in range(9):
            if self.digit_of_pair_is_in_cell(pair, i, column):
                col_count += 1
        if col_count == 2:  
            return True

        # Check if the number is unique in the 3x3 box
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.digit_of_pair_is_in_cell(pair,i + start_row, j + start_column):
                    box_count += 1
        if box_count == 2:  
            return True

        # If the pair is not unique in row, column, or box
        return False        

    # check if candidate string is unique in a row, column or cell
    def number_is_unique(self, row, column, number):
        # check if the number is unique in a row or in a column
        row_count = col_count = box_count = 0
        for i in range(9):
            if number in self.candidates[row][i]:
                row_count += 1
        if row_count == 1:
            return True

        for i in range(9):
            if number in self.candidates[i][column]:
                col_count += 1
        if col_count == 1:  
            return True

        # Check if the number is unique in the 3x3 box
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if number in self.candidates[i + start_row][j + start_column]:
                    box_count += 1
        if box_count == 1:  
            return True

        # If the number is not unique in row, column, or box
        return False        

    # Removes candidates from row, box or column    
    def remove_candidates_after_number_set(self, row, column, number):
        # Remove number from the same row or column
        for i in range(9):
            if number in self.candidates[row][i]:
                self.candidates[row][i] = self.candidates[row][i].replace(number, '')
            if number in self.candidates[i][column]:
                self.candidates[i][column] = self.candidates[i][column].replace(number, '')

        # Remove number from the same 3x3 box
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if number in self.candidates[i + start_row][j + start_column]:
                    self.candidates[i + start_row][j + start_column] = self.candidates[i + start_row][j + start_column].replace(number, '')


    # function checks if given number is legal for a certain cell
    def number_is_valid(self, row, column, number):
        # check row and column
        for i in range(9):
            if self.board[row][i] == number or self.board[i][column] == number:
                return False

        # check square
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_column] == number:
                    return False
        return True

    # method to find all legal candidates for an empty cell 
    def find_all_candidates(self):
        # generate empty 9*9 Matrix full of empty strings
        candidates = [["" for i in range(9)] for j in range(9)]

        # find legal candidates for all empty squares
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    for n in range(1,10):
                        if self.number_is_valid(r, c, n) and str(n) not in candidates[r][c]:
                            candidates[r][c] += str(n)
        return candidates

    # goes through a sudoku and counts all cells that needs to be filled
    def count_empty_cells(self):
        return sum(1 for row in range(9) for column in range(9) if self.board[row][column] == 0)


    # print board in console
    def print(self):
        for i in range(9):
            print(" ".join([str(x)if x != 0 else "." for x in self.board[i]]))


def main():
    # test board that can be solved easily with just naked Singles and Hidden Singles
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 7, 8, 3, 0, 9, 0, 0],
             [0, 0, 5, 0, 0, 2, 6, 4, 0],
             [0, 0, 2, 6, 0, 0, 0, 7, 0],
             [0, 4, 0, 0, 0, 0, 0, 8, 0],
             [0, 6, 0, 0, 0, 3, 2, 0, 0],
             [0, 2, 8, 4, 0, 0, 5, 0, 0],
             [0, 0, 0, 0, 9, 6, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    #example board that must be solved with naked pairs, hidden pairs, pointing pairs and Skyscraper
    # board = [[0, 0, 4, 0, 0, 0, 0, 0, 0],
    #       [0, 9, 0, 0, 7, 0, 4, 0, 0],
    #       [0, 8, 0, 0, 0, 0, 0, 3, 5],
    #       [0, 0, 5, 0, 0, 9, 1, 0, 6],
    #       [7, 3, 0, 0, 0, 0, 9, 0, 4],
    #       [0, 0, 0, 0, 8, 6, 0, 0, 0],
    #       [0, 0, 0, 9, 0, 0, 7, 4, 1],
    #       [6, 0, 0, 5, 0, 0, 0, 0, 0],
    #       [0, 0, 0, 0, 0, 8, 0, 0, 0]]

    # test board with a naked pair in a difficult box
    # board = [[0, 1, 7, 0, 8, 9, 0, 2, 0],
    #       [0, 8, 6, 0, 0, 0, 7, 0, 9],
    #       [9, 2, 5, 7, 6, 3, 0, 8, 0],
    #       [8, 6, 9, 3, 0, 0, 2, 7, 0],
    #       [1, 5, 3, 0, 7, 0, 8, 9, 0],
    #       [2, 7, 4, 0, 9, 8, 0, 0, 0],
    #       [7, 3, 2, 9, 1, 4, 0, 0, 8],
    #       [0, 9, 1, 8, 2, 0, 0, 0, 7],
    #       [0, 4, 8, 0, 3, 7, 9, 1, 2]]

    # example board from the old article
    # board = [[0, 0, 3, 0, 7, 0, 0, 6, 0],
    #       [0, 0, 0, 0, 0, 0, 0, 8, 0],
    #       [0, 0, 0, 0, 0, 0, 0, 2, 3],
    #       [0, 0, 0, 7, 0, 0, 0, 0, 4],
    #       [0, 0, 0, 2, 0, 0, 0, 0, 0],
    #       [5, 0, 6, 0, 0, 0, 0, 0, 9],
    #       [9, 0, 0, 0, 4, 0, 0, 0, 5],
    #       [0, 8, 0, 3, 0, 0, 0, 0, 0],
    #       [2, 0, 0, 0, 0, 8, 0, 0, 0]]

    # import string from sudoku.coach or other sites
    # sudoku_string = '050000420008000030900000080820500300060009000000600209200300000040008000500907600' # difficult sudoku with pointing pairs, hidden pairs and unknown techniques
    # sudoku_string = '000060800000900002678000009300800006000420000700000020107058000000100605002030090' # x wing necessary and one skyscraper (not implemented)
    sudoku_string = '040300000000000100007000546000702419080400020000009000000030060500006081030500000' # 4 naked pairs, 3 hidden pairs, 1 pointing pair
    board_import = [[int(num) for num in sudoku_string[i:i+9]] for i in range(0, 81, 9)]

    sudoku = Sudoku(board_import)
    print(f"Score: {sudoku.evaluate()}")
    sudoku.print()



if __name__ == "__main__":
    main()
