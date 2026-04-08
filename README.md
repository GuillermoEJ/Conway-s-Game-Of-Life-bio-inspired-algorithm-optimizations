# Game of Life - Optimization with Evolutionary Algorithms

Conway's Game of Life optimization project using genetic algorithms (GA) and ant colony optimization (ACO) to find optimal initial configurations that maximize evolution duration and maintain stable or cyclic states.

<img width="400" height="280" alt="Figure_2" src="https://github.com/user-attachments/assets/bc15d5cb-eabd-43f6-9a72-23b1ad887f17" />

>Visualization of high fitness solution for stable pattern

## Description

This project implements and compares two bio-inspired optimization algorithms:

- **Genetic Algorithm (GA)**: Population-based search using selection, crossover, and mutation operators to evolve better solutions over generations.

- **Ant Colony Optimization (ACO)**: Metaheuristic inspired by ant foraging behavior, using pheromone trails to guide the search toward promising regions of the solution space.

Both algorithms are designed to find initial Game of Life configurations that exhibit interesting evolutionary behavior.

## Requirements

- Python >= 3.7
- NumPy >= 1.21.0
- Matplotlib >= 3.4.0
- SciPy >= 1.7.0
- inspyred >= 1.0.1
- NetworkX >= 2.6

## Installation

```bash
pip install -r requirements.txt
```

Or with setup.py:

```bash
pip install -e .
```

## Usage

### Interactive Game of Life

```bash
python src/gameoflife.py
```

Allows manual or random grid initialization and real-time visualization.

### Run Genetic Algorithm

```bash
python src/GA.py
```

Optimizes initial configurations using genetic algorithm with configurable parameters.

### Run Ant Colony Optimization

```bash
python src/ACO.py
```

Optimizes initial configurations using ant colony optimization.

### Results Analysis

```bash
python analysis/analisis.py
```

Performs statistical analysis and visualization of optimization results.

### Statistical Tests

```bash
python tests/tests.py
```

Runs Friedman and Shaffer tests comparing algorithm performance.

## Configuration

Edit parameters directly in each module:

- **src/GA.py**: Population size, generations, mutation rate, selection method
- **src/ACO.py**: Number of ants, pheromone parameters (alpha, beta, rho), evaluation budget
- **src/gameoflife.py**: Board size, iterations

## Results

### Generated Artifacts

The optimization runs generate the following files in the `results/` directory:

| File | Description |
|------|-------------|
| `fitness_A.npy` | Fitness history - Genetic Algorithm run A |
| `fitness_B.npy` | Fitness history - Genetic Algorithm run B |
| `fitness_C.npy` | Fitness history - Genetic Algorithm run C |
| `fitness_M.npy` | Fitness history - Ant Colony Optimization |
| `mejores_individuos_A.npy` | Best individuals - GA run A |
| `mejores_individuos_B.npy` | Best individuals - GA run B |
| `mejores_individuos_C.npy` | Best individuals - GA run C |
| `mejores_individuos_M.npy` | Best individuals - ACO |
| `elites_GA.npy` | Elite solutions found by GA |
| `elites_ACO.npy` | Elite solutions found by ACO |
| `aco_31.npy` | ACO final configuration (31×31 grid) |
| `random_31.npy` | Random baseline configuration (31×31 grid) |
| `ultima_GA.npy` | Latest GA configuration |

### Statistical Analysis

The project includes comprehensive statistical tests to compare algorithm performance:

- **Friedman Test**: Non-parametric test for comparing multiple algorithms across multiple datasets
- **Shaffer Post-hoc Test**: Identifies significant pairwise differences between algorithms
- **Normality Tests**: Validates assumptions for parametric tests
- **Homogeneity of Variance**: Checks equality of variances between groups

Run statistical analysis with:
```bash
python tests/tests.py
```

### Key Findings

- **Convergence Speed**: GA shows faster initial convergence, ACO provides more stability
- **Solution Quality**: Both algorithms significantly outperform random initialization
- **Scalability**: ACO demonstrates better performance on larger grid sizes
- **Stability**: ACO finds more consistent elite solutions across runs

### Visualization Examples

Generated visualizations include:
- Fitness curves over generations
- Population distribution heatmaps
- Best solution configurations on Game of Life grid
- Statistical comparison charts 

## Contributing

Contributions are welcome! Please ensure:

- Code follows PEP 8 style guidelines
- Add docstrings to new functions
- Test your changes before submitting
- Use meaningful commit messages

## License

MIT
