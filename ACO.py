import numpy as np
from typing import List
from copy import deepcopy


class ACOGameOfLife:
    def __init__ (self, board_dimension: int, n_ants: int = 10, max_live_cells_proportion: float = 0.6, alpha: float = 1, beta: float = 5, rho: float = 0.8):
        self.board_dimension = board_dimension
        self.board_dimension_squared = board_dimension ** 2

        self.n_ants = n_ants
        self.max_live_cells_proportion = max_live_cells_proportion
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.pheromone = None
        self.best_solution = None
        self.best_fitness = None

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []


    def _initialize(self):
        print("Inicialización")

        self.pheromone = np.ones(self.board_dimension_squared)
        self.best_solution = None
        self.best_fitness = float('-inf')

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []

    def optimize(self, max_evaluations: int = 100):
        self._initialize()


        n_evaluations = 0
        iter_fitness = 1e-10
        while n_evaluations < max_evaluations:
            print("Evaluación ",n_evaluations)
            trails = []
            for _ in range(self.n_ants):

                solution = self._construct_solution_2()

                fitness = self._evaluate(solution)[0]
                solution = self._evaluate(solution)[1]

                #pruebas


                n_evaluations += 1
                trails.append((solution, fitness))

                if fitness >= self.best_fitness:
                    self.best_solution = solution
                    self.best_fitness = fitness

                #print("Hormiga ",_, " propone solución con fitness ",fitness, " (",self.best_fitness,")")

            iter_fitness = self.best_fitness
            self._update_pheromone(trails, iter_fitness)


            self.trails_history.append(deepcopy(trails))
            self.best_fitness_history.append(self.best_fitness)

        return self.best_solution



    def _construct_solution_2(self) -> List[int]:
        solution = np.zeros(self.board_dimension_squared)

        while True:

            candidates = self._get_candidates(solution)

            if len(candidates) == 0:
                break
            elif len(candidates) == 1:
                solution[candidates[0]] = 1
                break

            pheromones = self.pheromone[candidates]**self.alpha
            heuristic = self._heuristic_2(candidates, solution)**self.beta

            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total
            #print(probabilities)
            solution[np.random.choice(candidates, p=probabilities)] = 1


        return solution

    def _get_candidates(self, solution: List[int]) -> np.ndarray:

        max_live_cells = self.board_dimension_squared * self.max_live_cells_proportion
        selected = np.argwhere(solution == 1).flatten()

        candidates = [i for i in range(self.board_dimension_squared) if i not in selected and len(selected) <= max_live_cells]
        return np.array(candidates)

    def _evaluate(self, solution: List[int]) -> float:
        solution_value = -10
        gol_results = self._game_of_life(solution)
        if gol_results[0]:
            gol_iterations = gol_results[1]
            gol_live_cells = gol_results[2]
            #solution_value = gol_live_cells * 10 / gol_iterations * 0.1
            solution_value = gol_live_cells
        optimized_solution = gol_results[3]

        return solution_value, optimized_solution

    def _heuristic_2(self, candidates: List[int], board) -> np.ndarray:
        board_matrix = np.reshape(board, (self.board_dimension, self.board_dimension))

        heuristics = np.zeros(len(candidates))
        current_cell = 0
        for cell in candidates:
            n_neighbours = self._count_neighbours(board_matrix, cell)
            if n_neighbours < 3:
                heuristics[current_cell] = 0.5 + 0.25 * n_neighbours
            else:
                heuristics[current_cell] = 0.5 / n_neighbours

            current_cell += 1

        return heuristics



    def _count_neighbours(self, board: np.ndarray, cell: int):

        dimension = board.shape[0]

        # Obtiene la columna y la fila en la matriz de la cell
        col = cell % dimension
        row = cell // dimension

        # Usa slicing para obtener los vecinos que rodean la cell indicada
        row_start, row_end = max(0, row - 1), min(dimension, row + 2)
        col_start, col_end = max(0, col - 1), min(dimension, col + 2)

        # Suma los vecinos y resta el valor de la casilla central
        return np.sum(board[row_start:row_end, col_start:col_end]) - board[row, col]

    def _game_of_life(self, board: List[int]):

        current_board = np.reshape(board, (self.board_dimension, self.board_dimension))

        still_life_found = False
        iteration = 0
        final_live_cells = 0
        max_iterations = 100
        still_life_iterations = max_iterations

        while iteration < max_iterations and not still_life_found:
            new_board = np.zeros_like(current_board)

            for cell in range(self.board_dimension_squared):
                cell_row = cell // self.board_dimension
                cell_col = cell % self.board_dimension
                n_neighbours = self._count_neighbours(current_board, cell)

                if current_board[cell_row, cell_col] == 1:
                    if n_neighbours < 2 or n_neighbours > 3:
                        new_board[cell_row, cell_col] = 0
                    else:
                        new_board[cell_row, cell_col] = 1
                else:
                    if n_neighbours == 3:
                        new_board[cell_row, cell_col] = 1
                    else:
                        new_board[cell_row, cell_col] = 0

            if np.array_equal(current_board, new_board):
                if np.sum(new_board) > 0:
                    still_life_found = True
                    still_life_iterations = iteration
                    final_live_cells = np.sum(current_board)
                else:
                    still_life_found = False
                    still_life_iterations = max_iterations
                    break

            current_board = new_board.copy()
            iteration += 1
        final_board = new_board.copy().flatten().tolist()
        return still_life_found, still_life_iterations, final_live_cells, final_board

    def _update_pheromone(self, trails: List[List[int]], best_fitness):
        self.pheromone_history.append(self.pheromone.copy())
        print("Best fitness: ",best_fitness)
        evaporation = 1 - self.rho
        self.pheromone *= evaporation
        for solution, fitness in trails:
            delta_fitness = 1.0/(1.0 + (best_fitness - fitness) / best_fitness)
            new_pheromones = np.array(solution) * delta_fitness

            self.pheromone = np.add(self.pheromone, new_pheromones)

dim = 16
aco = ACOGameOfLife(dim, alpha = 1, max_live_cells_proportion = 0.5)
best_solution = aco.optimize(1000)


def count_neighbours(board, cell: int):

        dimension = board.shape[0]

        # Obtiene la columna y la fila en la matriz de la cell
        col = cell % dimension
        row = cell // dimension

        # Usa slicing para obtener los vecinos que rodean la cell indicada
        row_start, row_end = max(0, row - 1), min(dimension, row + 2)
        col_start, col_end = max(0, col - 1), min(dimension, col + 2)

        # Suma los vecinos y resta el valor de la casilla central
        return np.sum(board[row_start:row_end, col_start:col_end]) - board[row, col]


def game_of_life(board: List[int]):

        current_board = np.reshape(board, (dim, dim))

        still_life_found = False
        iteration = 0
        max_iterations = 100
        still_life_iterations = max_iterations

        while iteration < max_iterations and not still_life_found:
            new_board = np.zeros_like(current_board)

            print(current_board)

            for cell in range(dim**2):
                cell_row = cell // dim
                cell_col = cell % dim
                n_neighbours = count_neighbours(current_board, cell)

                if current_board[cell_row, cell_col] == 1:
                    if n_neighbours < 2 or n_neighbours > 3:
                        new_board[cell_row, cell_col] = 0
                    else:
                        new_board[cell_row, cell_col] = 1
                else:
                    if n_neighbours == 3:
                        new_board[cell_row, cell_col] = 1
                    else:
                        new_board[cell_row, cell_col] = 0

                if np.array_equal(current_board, new_board):
                    if np.sum(new_board) > 0:
                        still_life_found = True
                        still_life_iterations = iteration
                        final_live_cells = np.sum(current_board)
                    else:
                        still_life_found = False
                        still_life_iterations = max_iterations
                        break







            current_board = new_board.copy()
            iteration += 1

        return still_life_found, still_life_iterations

print("Mejor solución: ",best_solution)
game_of_life(best_solution)

#======================================== Visualizar =====================================
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

fitness = np.array([[ant[1] for ant in trails] for trails in aco.trails_history ])
best_fitness = np.array(aco.best_fitness_history)

fig, axs = plt.subplots(figsize=(5,5))
axs.set_title('Fitness evolution')
axs.set_xlabel('Iterations')
axs.set_ylabel('Fitness')

axs.plot(best_fitness, label='best_high')

median = np.median(fitness, axis=1)
min = np.min(fitness, axis=1)
max = np.max(fitness, axis=1)
axs.plot(median, label='iterations_high')
axs.fill_between(np.arange(len(median)), min, max, alpha=0.3, color='orange')

plt.legend()