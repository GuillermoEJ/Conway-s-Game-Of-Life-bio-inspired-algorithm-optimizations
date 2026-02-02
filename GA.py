# ===================== Imports y Constantes =====================
import numpy as np
import matplotlib.pyplot as plt
from random import Random
from time import time
from inspyred import ec
from scipy.signal import convolve2d

DIMENSION = 8
MAX_ITERACIONES_GOL = 100
PSEUDO_BEST = (DIMENSION**2)*0.6


KERNEL_VECINOS = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.uint8)

# ===================== Definición del Problema =====================

class GOL(object):
    def __init__(self, dimensions=DIMENSION**2, maximize=True):
        self.dimensions = dimensions
        self.maximize = maximize
        self.bounder = ec.DiscreteBounder([0, 1])

    def generator(self, random, args):
        return [random.choice([0,1]) for _ in range(self.dimensions)]

    def evaluator(self, candidates, args):
        fitness = []
        for candidate in candidates:
            tablero_inicial = np.array(candidate).reshape((DIMENSION,DIMENSION)).astype(np.uint8)
            iteraciones = 0
            estado = tablero_inicial.copy()
            estable = False

            for _ in range(MAX_ITERACIONES_GOL):
                iteraciones += 1
                vecinos = convolve2d(estado, KERNEL_VECINOS, mode='same', boundary='fill', fillvalue=0)
                nuevo_estado = np.where(
                    (estado == 1) & ((vecinos == 2) | (vecinos == 3)), 1,
                    np.where((estado == 0) & (vecinos == 3), 1, 0)
                ).astype(np.uint8)

                if np.array_equal(nuevo_estado, estado):
                    estable = True
                    break
                estado = nuevo_estado

            celulas = estado.sum()

            if not estable:
                fitness_calculated = (celulas / PSEUDO_BEST) * 0.1
            else:
                fitness_calculated = (celulas / PSEUDO_BEST) * 0.9 + (1 - (iteraciones / MAX_ITERACIONES_GOL)) * 0.1

            fitness.append(fitness_calculated)
        return fitness

# ===================== Herramientas =====================

def ejecutar_gol(estado):
    estado = estado.copy()
    iteraciones = 0
    for _ in range(MAX_ITERACIONES_GOL):
        iteraciones += 1
        vecinos = convolve2d(estado, KERNEL_VECINOS, mode='same', boundary='fill', fillvalue=0)
        nuevo_estado = np.where(
            (estado == 1) & ((vecinos == 2) | (vecinos == 3)), 1,
            np.where((estado == 0) & (vecinos == 3), 1, 0)
        ).astype(np.uint8)
        if np.array_equal(nuevo_estado, estado):
            return (nuevo_estado, iteraciones)
        estado = nuevo_estado
    return (nuevo_estado, iteraciones)

# Observer extendido
def best_matrix_observer_extended(population, num_generations, num_evaluations, args):
    best = max(population)
    matriz = np.array(best.candidate).reshape((DIMENSION, DIMENSION)).astype(np.uint8)
    _, iteraciones = ejecutar_gol(matriz)
    args.setdefault('best_individuals_info', []).append({
        'generation': num_generations,
        'fitness': best.fitness,
        'iterations': iteraciones,
        'matrix': matriz.copy()
    })
def mostrar(individuo):
  individuo = ejecutar_gol(np.array(individuo).reshape((DIMENSION,DIMENSION)).astype(np.uint8))
  plt.imshow(individuo[0], cmap='binary')
  plt.title("Iteraciones: "+str(individuo[1]))
  plt.axis("on")
  plt.show()

def diversity(population):
    return np.array([i.candidate for i in population]).std(axis=0).mean()

def fitness_diversity_observer(population, num_generations, num_evaluations, args):
    """Observer to track best fitness and diversity."""
    best = max(population).fitness
    div = diversity(population)

    args['best_fitness_historic'].append(best)
    args['diversity_historic'].append(div)

# ===================== GoL GA con parámetros personalizados =====================

def GoL_GA(selector_func, mutation_rate, num_selected):
    seed = time()
    prng = Random()
    prng.seed(seed)

    best_fitness_historic = []
    diversity_historic = []

    ga = ec.GA(prng)
    ga.selector = selector_func
    ga.variator = [ec.variators.n_point_crossover, ec.variators.bit_flip_mutation]
    ga.replacer = ec.replacers.generational_replacement
    ga.terminator = ec.terminators.generation_termination
    ga.observer = [fitness_diversity_observer, ec.observers.stats_observer]

    problem = GOL(dimensions = DIMENSION * DIMENSION)

    final_pop = ga.evolve(generator=problem.generator,
                          evaluator=problem.evaluator,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          pop_size=100,
                          max_generations=100,
                          num_elites=1,
                          num_selected=num_selected,
                          crossover_rate=1,
                          num_crossover_points=1,
                          mutation_rate=mutation_rate,
                          best_fitness_historic=best_fitness_historic,
                          diversity_historic=diversity_historic)

    best = max(ga.population)
    print('Best Solution: {0}: {1}'.format(str(best.candidate), best.fitness))
    mostrar(best.candidate)

    plt.figure(figsize=(10,5))
    plt.subplot(1, 2, 1)
    plt.plot(best_fitness_historic, label="Best Fitness")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(diversity_historic, label="Diversity", color='orange')
    plt.xlabel('Generation')
    plt.ylabel('Diversity')
    plt.title('Diversity over Generations')
    plt.legend()

    plt.tight_layout()
    plt.show()

# ===================== Hyperparameter Tuning =====================

def hyperparameter_tuning():
    mutation_rates = [0.01, 0.03, 0.05]
    num_selected_values = [50, 75, 100]
    selectors = {
        'fps': ec.selectors.fitness_proportionate_selection,
        'tournament': ec.selectors.tournament_selection,
        'truncation': ec.selectors.truncation_selection
    }

    best_config = None
    best_avg_fitness = -1

    for selector_name, selector_func in selectors.items():
        for mutation_rate in mutation_rates:
            for num_selected in num_selected_values:
                config_label = f"{selector_name}-mut{mutation_rate}-sel{num_selected}"
                print(f"\nTrying config: {config_label}")
                final_fitnesses = []

                for rep in range(3):
                    print(f"Repetition {rep+1}/3")
                    prng = Random()
                    prng.seed(time())
                    ga = ec.GA(prng)
                    ga.selector = selector_func
                    ga.variator = [ec.variators.n_point_crossover, ec.variators.bit_flip_mutation]
                    ga.replacer = ec.replacers.generational_replacement
                    ga.terminator = ec.terminators.generation_termination

                    best_fitness_historic = []
                    diversity_historic = []

                    problem = GOL(dimensions=DIMENSION * DIMENSION)

                    final_pop = ga.evolve(
                        generator=problem.generator,
                        evaluator=problem.evaluator,
                        bounder=problem.bounder,
                        maximize=problem.maximize,
                        pop_size=100,
                        max_generations=100,
                        num_elites=1,
                        num_selected=num_selected,
                        crossover_rate=1,
                        num_crossover_points=1,
                        mutation_rate=mutation_rate,
                        best_fitness_historic=best_fitness_historic,
                        diversity_historic=diversity_historic
                    )

                    best = max(final_pop)
                    final_fitnesses.append(best.fitness)
                    print(f"     → Fitness: {best.fitness:.4f}")

                avg_fitness = np.mean(final_fitnesses)
                print(f"Avg fitness for {config_label}: {avg_fitness:.4f}")

                if avg_fitness > best_avg_fitness:
                    best_avg_fitness = avg_fitness
                    best_config = (selector_func, mutation_rate, num_selected)

    selector_func, mutation_rate, num_selected = best_config
    print(f"\nBest config: {selector_func.__name__} - mut={mutation_rate} - sel={num_selected} with avg fitness {best_avg_fitness:.4f}")
    GoL_GA(selector_func, mutation_rate, num_selected)

#==================== Estadistico ==================
def ejecutar_GA_config(config_id):
    prng = Random()
    prng.seed(time())

    ga = ec.GA(prng)
    ga.variator = [ec.variators.n_point_crossover, ec.variators.bit_flip_mutation]
    ga.replacer = ec.replacers.generational_replacement
    ga.terminator = ec.terminators.generation_termination

    if config_id == 'A':
        ga.selector = ec.selectors.fitness_proportionate_selection
        mutation_rate = 0.01
        num_selected = 100
    elif config_id == 'B':
        ga.selector = ec.selectors.tournament_selection
        mutation_rate = 0.05
        num_selected = 100
    elif config_id == 'C':
        ga.selector = ec.selectors.truncation_selection
        mutation_rate = 0.02
        num_selected = 100
    elif config_id == 'Mejor':
        ga.selector = ec.selectors.fitness_proportionate_selection
        mutation_rate = 0.01
        num_selected = 100

    problem = GOL(dimensions = DIMENSION * DIMENSION)
    info = []

    ga.observer = [best_matrix_observer_extended]
    final_pop = ga.evolve(
        generator=problem.generator,
        evaluator=problem.evaluator,
        bounder=problem.bounder,
        maximize=problem.maximize,
        pop_size=100,
        max_generations=100,
        num_elites=1,
        num_selected=num_selected,
        crossover_rate=1,
        num_crossover_points=1,
        mutation_rate=mutation_rate,
        best_individuals_info=info
    )

    best = max(final_pop)
    return best.fitness, info

def estadístico_GA(): # opción analaisis estadistico
    resultados_A = []
    resultados_B = []
    resultados_C = []
    info_guardada_A = []
    info_guardada_B = []
    info_guardada_C = []

    
    resultados_MejorGA = []
    info_guardada_MejorGA = []

    for i in range(31):
        '''
        fit_A, info_A = ejecutar_GA_config('A')
        resultados_A.append(fit_A)
        info_guardada_A.append(info_A)

        fit_B, info_B = ejecutar_GA_config('B')
        resultados_B.append(fit_B)
        info_guardada_B.append(info_B)

        fit_C, info_C = ejecutar_GA_config('C')
        resultados_C.append(fit_C)
        info_guardada_C.append(info_C)

        print("Iteración: "+str(i))
        '''
        fit_M, info_M = ejecutar_GA_config('Mejor')
        resultados_MejorGA.append(fit_M)
        info_guardada_MejorGA.append(info_M)

        print("Iteración: "+str(i))

    np.save("fitness_M.npy", np.array(resultados_MejorGA))
    np.save("mejores_individuos_M.npy", info_guardada_MejorGA)
   
    '''
    np.save("fitness_A.npy", np.array(resultados_A))
    np.save("fitness_B.npy", np.array(resultados_B))
    np.save("fitness_C.npy", np.array(resultados_C))

    np.save("mejores_individuos_A.npy", info_guardada_A)
    np.save("mejores_individuos_B.npy", info_guardada_B)
    np.save("mejores_individuos_C.npy", info_guardada_C)
    '''

def ejecutar_varias_veces_gol():
    resultados = []

    for i in range(31):
        print(f"\nEjecución {i+1}/31")
        prng = Random()
        prng.seed(time())

        ga = ec.GA(prng)
        ga.selector = ec.selectors.fitness_proportionate_selection
        ga.variator = [ec.variators.n_point_crossover, ec.variators.bit_flip_mutation]
        ga.replacer = ec.replacers.generational_replacement
        ga.terminator = ec.terminators.generation_termination

        problem = GOL(dimensions=DIMENSION * DIMENSION)

        final_pop = ga.evolve(
            generator=problem.generator,
            evaluator=problem.evaluator,
            bounder=problem.bounder,
            maximize=problem.maximize,
            pop_size=100,
            max_generations=100,
            num_elites=1,
            num_selected=100,
            crossover_rate=1,
            num_crossover_points=1,
            mutation_rate=0.05
        )

        elite = max(final_pop)
        matrix = np.array(elite.candidate).reshape((DIMENSION, DIMENSION)).astype(np.uint8)
        final_state, iterations = ejecutar_gol(matrix)

        resultado = {
            'matrix': matrix,
            'fitness': elite.fitness,
            'alive_cells': final_state.sum(),
            'iterations': iterations
        }
        resultados.append(resultado)

    # Guardar en disco
    np.save("ultima_GA.npy", resultados)
    print("\nResultados guardados en 'ultima_GA.npy'")



# ===================== Main =====================

if __name__ == "__main__":
    #hyperparameter_tuning()
    #estadístico_GA()
    ejecutar_varias_veces_gol()