# Penyelesaian N queen problem dengan algoritma random restart hill climbing
#%%
import os
import time
import psutil
import random
import numpy as np
from plot import plot

#%%
# class NQueen digunakan untuk merepresentasikan keadaan n-queen.
class NQueen:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    # posisi baris ratu
    def get_row(self):
        return self.row

    # posisi kolom ratu
    def get_column(self):
        return self.column

    # pindahkan ratu satu baris ke bawah
    def move(self):
        self.row += 1

    # memeriksa apakah terdapat saling serang antara ratu ini dengan ratu lain
    def is_conflict(self, queen):
        # periksa baris dan kolom
        if self.row == queen.get_row() or self.column == queen.get_column():
            return True
        # periksa diagonal
        elif abs(self.column - queen.get_column()) == abs(self.row - queen.get_row()):
            return True

        return False


# class utama yang memiliki algoritma hill climbing dengan random restart
class HillClimbingRandomRestart:
    def __init__(self, n):
        self.n = n
        self.status = False
        self.steps_climbed_after_last_restart = 0
        self.steps_climbed = 0
        self.heuristic = 0
        self.random_restarts = 0

    # method untuk membuat board baru dan mengisinya dengan n-queens secara acak.
    # method ini digunakan di awal untuk menghasilkan board awal dan dipanggil
    # untuk setiap random restart setelahnya.
    def generate_board(self):
        start_board = []

        for i in range(self.n):
            start_board.append(NQueen(random.randint(0, self.n - 1), i))

        return start_board

    # method untuk menemukan heuristik suatu state
    # method ini berguna untuk menemukan jumlah konflik antar ratu.
    def find_heuristic(self, state):
        heuristic = 0

        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i].is_conflict(state[j]):
                    heuristic += 1

        return heuristic

    # method untuk memperoleh board berikutnya dengan heuristik terendah
    # method ini menemukan konfigurasi berikutnya (langkah yang harus dinaiki jika ada).
    def next_board(self, present_board):
        next_board = []
        temp_board = []

        # nilai heuristik dari board/state saat ini
        present_heuristic = self.find_heuristic(present_board)
        # inisialisasi heuristik terbaik dengan nilai heuristic saat ini
        best_heuristic = present_heuristic
        # inisialisasi heuristik sementara
        temp_heuristic = 0

        for i in range(self.n):
            # salin board saat ini sebagai next board dan temp board
            next_board.append(
                NQueen(present_board[i].get_row(), present_board[i].get_column())
            )
            temp_board.append(next_board[i])

        # iterasi tiap kolom
        for i in range(self.n):
            if i > 0:
                temp_board[i - 1] = NQueen(
                    present_board[i - 1].get_row(), present_board[i - 1].get_column()
                )

            temp_board[i] = NQueen(0, temp_board[i].get_column())

            # iterasi tiap baris
            for j in range(self.n):
                # ambil nilai heuristik dari temp board
                temp_heuristic = self.find_heuristic(temp_board)
                # periksa apakah temp board lebih baik dari best board
                if temp_heuristic < best_heuristic:
                    best_heuristic = temp_heuristic
                    # salin temp board sebagai best board
                    for k in range(self.n):
                        next_board[k] = NQueen(
                            temp_board[k].get_row(), temp_board[k].get_column()
                        )

                # pindahkan queen
                if temp_board[i].get_row() != self.n - 1:
                    temp_board[i].move()

        # periksa apakah present board dan best board yang ditemukan memiliki
        # nilai heuristik yang sama
        if best_heuristic == present_heuristic:
            # jika ya, buat board baru secara acak dan tetapkan ke best board
            next_board = self.generate_board()
            self.random_restarts += 1
            self.steps_climbed_after_last_restart = 0
            self.heuristic = self.find_heuristic(next_board)
        else:
            # jika tidak, maka didapatkan heuristik terbaik
            self.heuristic = best_heuristic

        self.steps_climbed += 1
        self.steps_climbed_after_last_restart += 1

        return next_board

    # metode untuk mencetak board berdasarkan keadaan saat ini
    def get_state(self, state):
        # buat board sementara berdasarkan state saat ini
        temp_board = np.zeros([self.n, self.n], dtype=int)
        temp_board = temp_board.tolist()

        for i in range(self.n):
            # dapatkan posisi ratu dari board saat ini dan atur posisi tersebut
            # sebagai angka 1 pada board solusi
            temp_board[state[i].get_row()][state[i].get_column()] = 1

        return temp_board

    # method untuk menjalankan solusi
    def solve(self):
        if self.n == 2 or self.n == 3:
            print(f"No Solution possible for {self.n} queens.")
            return

        # buat board awal
        present_board = self.generate_board()
        # buat nilai heuristik awal
        present_heuristic = self.find_heuristic(present_board)
        # test apakah board saat ini adalah board solusi
        while present_heuristic != 0:
            # update ke board selanjutnya
            present_board = self.next_board(present_board)
            # reset nilai heuristik saat ini
            present_heuristic = self.heuristic
        # kembalikan keadaan dari board sekarang
        self.status = True
        return self.get_state(present_board)

    # method untuk mencetak hasil dan keterangan status
    def print_solution_and_status(self):
        print(f"Solving {self.n} queen problem with random restart hill climbing")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get solution
        solution = self.solve()
        # print solution
        print()
        print(np.matrix(solution))
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        print(f"Total number of steps climbed\t : {self.steps_climbed}")
        print(f"Number of random restarts\t : {self.random_restarts}")
        print(
            f"Steps climbed after last restart : {self.steps_climbed_after_last_restart}"
        )
        # return solution
        return solution


#%%
if __name__ == "__main__":
    n_queen_hc = HillClimbingRandomRestart(int(input("Masukkan jumlah queen : ")))
    solution = n_queen_hc.print_solution_and_status()

    plot(solution)
