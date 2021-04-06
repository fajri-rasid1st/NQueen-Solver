# Penyelesaian N queen problem dengan algoritma genetika
#%%
import os
import time
import psutil
import random
import numpy as np
from plot import plot

#%%
class GeneticAlgorithm:
    def __init__(self, n=int, max_fitness=float, population=list, generation=int):
        self.n = n
        self.max_fitness = max_fitness
        self.population = population
        self.generation = generation
        self.status = False

    # method untuk membuat kromosom secara random
    @classmethod
    def random_chromosome(cls, size):
        return [random.randint(1, size) for _ in range(size)]

    # method untuk menentukan jumlah pasangan ratu yang tidak saling menyerang
    def fitness(self, chromosome):
        n = len(chromosome)

        horizontal_conflicts = (
            sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
        )

        left_diagonal = [0] * 2 * n
        right_diagonal = [0] * 2 * n

        for i in range(n):
            left_diagonal[i + chromosome[i] - 1] += 1
            right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

        diagonal_conflicts = 0

        for i in range(2 * n - 1):
            counter = 0

            if left_diagonal[i] > 1:
                counter += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i] - 1

            diagonal_conflicts += counter / (n - abs(i - n + 1))

        # example: for n = 8, 28 - (2 + 3) = 23
        return int(self.max_fitness - (horizontal_conflicts + diagonal_conflicts))

    # method untuk menentukan probabilitas yang akan dipilih (dari fungsi fitness)
    def probability(self, chromosome, fitness):
        return fitness(chromosome) / self.max_fitness

    # method untuk memilih pasangan secara acak untuk direproduksi
    # berdasarkan probabilitas
    def random_pick(self, population, probabilities):
        population_with_probability = zip(population, probabilities)
        total = sum(w for c, w in population_with_probability)
        r = random.uniform(0, total)
        upto = 0

        for c, w in zip(population, probabilities):
            if upto + w >= r:
                return c

            upto += w

        assert False, "Unreachable code"

    # method untuk melakukan persilangan antara dua kromosom untuk
    # menghasilkan keturunan baru
    def reproduce(self, x, y):
        n = len(x)
        c = random.randint(0, n - 1)

        return x[0:c] + y[c:n]

    # mengubah satu nilai gen dalam kromosom dari keadaan awal atau
    # mengubah nilai indeks random dari sebuah kromosom.
    def mutate(self, x):
        n = len(x)
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        x[c] = m

        return x

    # method untuk menentukan sifat genetik dari ratu
    def genetic_queen(self, population, fitness):
        new_population = []
        mutation_probability = 0.05
        probabilities = [self.probability(i, fitness) for i in population]

        for i in range(len(population)):
            # kromosom terbaik 1
            x = self.random_pick(population, probabilities)
            # kromosom terbaik 2
            y = self.random_pick(population, probabilities)
            # lakukan persilangan antara dua kromosom untuk menghasilkan keturunan baru
            child = self.reproduce(x, y)

            # terjadi mutasi ketika
            if random.random() < mutation_probability:
                child = self.mutate(child)

            self.print_chromosome(child)
            new_population.append(child)

            if fitness(child) == self.max_fitness:
                break

        return new_population

    # method untuk mencetak kromosom dan nilai fitnessnya
    def print_chromosome(self, chromosome):
        print(f"Chromosome = {str(chromosome)},  fitness = {self.fitness(chromosome)}")

    # method untuk membuat board solusi
    def get_state(self, chrom_out):
        # buat board baru diisi dengan 0
        board = np.zeros(shape=[self.n, self.n], dtype=int)
        board = board.tolist()

        # isi index pada board dengan 1 sesuai dengan index pada kromosom solusi
        for i in range(self.n):
            board[self.n - chrom_out[i]][i] = 1

        return board

    # method untuk menjalankan solusi
    def solve(self):
        if self.n == 2 or self.n == 3:
            print(f"No solution possible for {self.n} queens.")
            return

        # saat nilai fitness dari kromosom tiap populasi tidak sama dengan max fitness
        while not self.max_fitness in [
            self.fitness(chromosome) for chromosome in self.population
        ]:
            print(f"------------- Generation {self.generation} -------------")
            # lakukan proses genetika queen dan kembalikan populasi baru
            self.population = self.genetic_queen(self.population, self.fitness)
            print("")
            print(f"Max. fitness = {max([self.fitness(i) for i in self.population])}")
            print("")
            # generasi bertambah 1
            self.generation += 1

        # sampai di sini, berarti terdapat kromosom pada populasi yang menjadi solusi
        # dengan nilai fitness = max fitness
        chrom_out = []

        print(f"Solved in generation {self.generation - 1}")

        # lakukan iterasi pada populasi saat ini
        for chrom in self.population:
            # jika kromosom solusi telah didapat
            if self.fitness(chrom) == self.max_fitness:
                print("")
                print("One of the solutions: ")
                # ganti chrom_out menjadi chrom solusi
                chrom_out = chrom
                self.print_chromosome(chrom)

        # return chrom out
        self.status = True
        return self.get_state(chrom_out)

    def print_solution_and_status(self):
        print(f"Solving {self.n} queen problem with genetic algorithm")
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
        # return solution
        return solution


#%%
if __name__ == "__main__":
    n = int(input("Masukkan jumlah queen : "))
    max_fitness = (n * (n - 1)) / 2
    population = [GeneticAlgorithm.random_chromosome(n) for _ in range(100)]
    generation = 1

    n_queen_ga = GeneticAlgorithm(n, max_fitness, population, generation)
    solution = n_queen_ga.print_solution_and_status()

    plot(solution)