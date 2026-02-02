import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import os
print("Directorio actual:", os.getcwd())


EJECUCION = 1
size = 8  

def initialize_grid_random(size):
    return np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])

def initialize_grid_manual(size):
    grid = np.zeros((size, size), dtype=int)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1)

    def on_click(event):
        if event.inaxes == ax:
            x, y = int(event.ydata + 0.5), int(event.xdata + 0.5)
            grid[x, y] = 1 - grid[x, y]
            img.set_data(grid)
            fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.title("Click to toggle cells. Close window to continue.")
    plt.show()
    return grid

def count_neighbors(grid, x, y):
    size = grid.shape[0]
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = x + i, y + j
            if 0 <= nx < size and 0 <= ny < size:
                neighbors += grid[nx, ny]
    return neighbors

def update(grid):
    size = grid.shape[0]
    new_grid = np.zeros((size, size), dtype=int)
    for x in range(size):
        for y in range(size):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and neighbors in [2, 3]:
                new_grid[x, y] = 1
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1
    return new_grid

def animate(i, grid, img):
    new_grid = update(grid)
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

def mostrarSet():
    info_guardada = []
    set = input("Select: 1(A), 2(ACO), 3(GA), 4(Random): ")
    if set == "1":
        info_guardada = np.load("mejores_individuos_A.npy", allow_pickle=True)
    elif set == "2":
        info_guardada = np.load("mejores_individuos_C.npy", allow_pickle=True)
    elif set == "3":
        info_guardada = np.load("mejores_individuos_B.npy", allow_pickle=True)
    elif set == "4":
        info_guardada = np.load("ultima_GA.npy", allow_pickle=True)
    else:
        print("Invalid selection, defaulting to A")
        info_guardada = np.load("random_31.npy", allow_pickle=True)

    accion = input("1. Mostrar mejor\n2. Mostrar individuo nº_\n")

    if accion == "1":
        # Buscar el individuo con mejor fitness
        best = None
        for ejecucion in info_guardada:
            for individuo in ejecucion:
                if best is None or individuo['fitness'] > best['fitness']:
                    best = individuo

        grid = best['matrix']
        fitness = best['fitness']
        iterations = best['iterations']
        cells_alive = grid.sum()

        print(f"Best Individual - Fitness: {fitness:.4f}, Iterations: {iterations}, Alive Cells: {cells_alive}")

        fig, ax = plt.subplots()
        img = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1)
        ani = animation.FuncAnimation(fig, animate, fargs=(grid, img), frames=100, interval=50, blit=False)
        plt.title("Best Individual")
        plt.show()

    elif accion == "2":
        try:
            ejec = int(input("Execution index (0 to N): "))
            gen = int(input("Generation index (0 to 99): "))
            individuo = info_guardada[ejec][gen]
            grid = individuo['matrix']
            fitness = individuo['fitness']
            iterations = individuo['iterations']
            cells_alive = grid.sum()

            print(f"Individual [{ejec}][{gen}] - Fitness: {fitness:.4f}, Iterations: {iterations}, Alive Cells: {cells_alive}")

            fig, ax = plt.subplots()
            img = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1)
            ani = animation.FuncAnimation(fig, animate, fargs=(grid, img), frames=100, interval=50, blit=False)
            plt.title(f"Individual {ejec}-{gen}")
            plt.show()
        except Exception as e:
            print(f"Error loading individual: {e}")
    else:
        print("Invalid action.")


def main():
    print("Choose initialization method:")
    print("1. Ver individuos Set ")
    print("2. Random")
    print("3. Manual")
    print("0. Quit")
    choice = input("Select: ")

    if choice == "1":
        mostrarSet()
    elif choice == "2":
        grid = initialize_grid_random(size)
        fig, ax = plt.subplots()
        img = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1)
        ani = animation.FuncAnimation(fig, animate, fargs=(grid, img), frames=100, interval=50, blit=False)
        plt.show()
    elif choice == "3":
        grid = initialize_grid_manual(size)
        fig, ax = plt.subplots()
        img = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1)
        ani = animation.FuncAnimation(fig, animate, fargs=(grid, img), frames=100, interval=50, blit=False)
        plt.show()
    elif choice == "0":
        global EJECUCION 
        EJECUCION = 0
    else:
        print("Invalid option")

if __name__ == "__main__":
    while(EJECUCION == 1):
        main()
