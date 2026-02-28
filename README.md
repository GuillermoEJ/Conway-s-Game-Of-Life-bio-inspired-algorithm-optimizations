# Game of Life - Optimization with Evolutionary Algorithms

Conway's Game of Life optimization project using genetic algorithms (GA) and ant colony optimization (ACO) to find optimal initial configurations that maximize evolution duration and maintain stable or cyclic states.

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

The project generates and saves:

- Optimal initial configurations as .npy files
- Fitness evolution history
- Best individuals per execution
- Comparative statistical analysis with visualization

## Contributing

Contributions are welcome! Please ensure:

- Code follows PEP 8 style guidelines
- Add docstrings to new functions
- Test your changes before submitting
- Use meaningful commit messages

## License

MIT
