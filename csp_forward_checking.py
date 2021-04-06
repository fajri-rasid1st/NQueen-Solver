# Penyelesaian N queen problem dengan algoritma CSP forward checking
#%%
import os
import time
import psutil
import numpy as np
from plot import plot

#%%
class Unassigned:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash(self.row) ^ hash(self.column)


class CSPForwardChecking:
    def __init__(self, n):
        self.n = n
        self.status = False

    # kriteria mengecek apakah baris berisi queen atau tidak
    def is_row_correct(self, board, row):
        for col in range(self.n):
            if board[row, col] == 1:
                return False

        return True

    # kriteria mengecek apakah kolom berisi queen atau tidak
    def is_column_correct(self, board, column):
        for row in range(self.n):
            if board[row, column] == 1:
                return False

        return True

    # kriteria mengecek apakah diagonal atas dari state berisi queen atau tidak
    def check_upper_diagonal(self, board, row, column):
        iter_row = row
        iter_col = column

        while iter_col >= 0 and iter_row >= 0:
            if board[iter_row, iter_col] == 1:
                return False

            iter_col -= 1
            iter_row -= 1

        return True

    # kriteria mengecek apakah diagonal bawah dari state berisi queen atau tidak
    def check_lower_diagonal(self, board, row, column):
        iter_row = row
        iter_col = column

        while iter_col >= 0 and iter_row < self.n:
            if board[iter_row, iter_col] == 1:
                return False

            iter_row += 1
            iter_col -= 1

        return True

    # cek apakah diagonal memenuhi kriteria
    def is_diagonal_correct(self, board, row, column):
        return self.check_upper_diagonal(
            board, row, column
        ) and self.check_lower_diagonal(board, row, column)

    # cek apakah baris, kolom, dan diagonal memenuhi kriteria
    def is_correct(self, board, row, column):
        return (
            self.is_row_correct(board, row)
            and self.is_column_correct(board, column)
            and self.is_diagonal_correct(board, row, column)
        )

    # get rows propostion
    def get_rows_proposition(self, board, queen):
        rows = []

        for row in range(self.n):
            if self.is_correct(board, row, queen):
                rows.append(row)

        return rows

    # get unassigned from constraint
    def get_unassigned_from_constraint(self, board, queen):
        result = []

        for row in range(self.n):
            for col in range(queen + 1, self.n):
                if board[row, col] == 0 and self.is_correct(board, row, col):
                    result.append(Unassigned(row, col))

        return result

    # forward checking
    def forward_check(self, board, row, queen):
        act_domain = self.get_rows_proposition(board, queen)
        tmp_domain = list(act_domain)

        for proposition_row in act_domain:
            if not self.is_correct(board, proposition_row, queen):
                tmp_domain.remove(proposition_row)

        return len(tmp_domain) == 0

    # method untuk menjalankan solusi
    def solve(self, board, queen):
        if self.n == 2 or self.n == 3:
            print(f"No Solution possible for {self.n} queens.")
            return

        if self.n == queen:
            self.status = True
            return True

        rows_proposition = self.get_rows_proposition(board, queen)

        for row in rows_proposition:
            board[row, queen] = 1
            domain_wipe_out = False

            for variable in self.get_unassigned_from_constraint(board, queen):
                if self.forward_check(board, variable.row, variable.column):
                    domain_wipe_out = True
                    break

            if not domain_wipe_out:
                if self.solve(board, queen + 1):
                    return True

            board[row, queen] = 0

    # method untuk mencetak hasil dan keterangan status
    def print_solution_and_status(self, board):
        print(f"Solving {self.n} queen problem with CSP forward checking")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get solution
        solution = self.solve(board, 0)
        # print solution
        print()
        print(np.matrix(board))
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        # return board
        return board


#%%
if __name__ == "__main__":
    n = int(input("Masukkan jumlah queen : "))
    board = np.array(np.zeros(shape=(n, n), dtype=int))

    n_queen_csp_fc = CSPForwardChecking(n)
    solution = n_queen_csp_fc.print_solution_and_status(board)

    plot(solution)