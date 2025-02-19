#!/usr/bin/env python3
# This Code is for the first Article and contains the strategies naked single and hidden single

class Sudoku:
	def __init__(self, board):
		self.board = board
		self.candidates = self.find_all_candidates()

	def evaluate_Sudoku(self):
		score = {"Naked Single":0, "Hidden Single":0}
		original_empty_cells = self.count_empty_cells()

		while(self.count_empty_cells() > 0):
			progress = False

			# Versuche offensichtliche Single
			solved_count = self.find_naked_single()
			if solved_count > 0:
				score["Naked Single"] += solved_count
				progress = True

			# Dann probiere versteckte Single
			if not progress:
				solved_count = self.find_hidden_single()
				if solved_count > 0:
					score["Hidden Single"] += solved_count
					progress = True

			# wenn kein Fortschritt erzielt wurde, abbrechen
			if not progress:
				print(self.candidates)
				print("Unknown Strategy needed to solve Sudoku")
				break

		# Kalkuliere score
		print(score)
		return (score["Naked Single"] + (score["Hidden Single"] * 2))/original_empty_cells

	# method solves every cell with a single candidate
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

	# checks if candidate string f.e('1') is unique in a row, column or cell
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
	def print_Sudoku(self):
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

	sudoku_string = '040000080007000060000010000410000200000005000030000000006007003005806000000000001' # example for article 1
	board_import = [[int(num) for num in sudoku_string[i:i+9]] for i in range(0, 81, 9)]

	sudoku = Sudoku(board_import)
	print(f"Score: {sudoku.evaluate_Sudoku()}")
	sudoku.print_Sudoku()


if __name__ == "__main__":
	main()
