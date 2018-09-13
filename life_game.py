import matplotlib.pyplot as plt
import matplotlib.animation as anime
import numpy as np
import argparse

ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(n):
    return np.random.choice(vals, n*n, p=[0.2, 0.8]).reshape(n,n)


def update(frame_num, img, grid, n):
    new_grid = grid.copy()
    for i in range(n):
        for j in range(n):
            living_neighbours = int((
                                     grid[i, (j-1)%n] +
                                     grid[i, (j + 1)%n] +
                                     grid[(i - 1)%n, j] +
                                     grid[(i + 1)%n, j] +
                                     grid[(i - 1)%n, (j - 1) % n] +
                                     grid[(i - 1) % n, (j + 1) % n] +
                                     grid[(i+1)%n, (j-1)%n] +
                                     grid[(i+1)%n, (j+1)%n]) / 255)

            if grid[i, j] == ON:
                if (living_neighbours < 2) or (living_neighbours > 3):
                    new_grid[i, j] = OFF
            else:
                if living_neighbours == 3:
                    new_grid[i, j] = ON

    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

def add_glider(i, j, grid):
    glider = np.array([[0,0,255], [255,0,255], [0,255,255]])
    grid[i:i+3, j:j+3] = glider


def main():
    parser = argparse.ArgumentParser(description="Uruchamianie gry w życie Conwaya.")
    # argumenty
    parser.add_argument('--grid-size', dest='n', required=False)    # wielkość siatki
    parser.add_argument('--mov-file', dest='mov_file', required=False)  # nazwa pliku .mov
    parser.add_argument('--interval', dest='interval', required=False)  # przerwa między animacjiami w milisekundach
    parser.add_argument('--glider', action='store_true', required=False)    # rozpoczynanie ze strukturą szybowca
    args = parser.parse_args()

    n = 100
    if args.n and int(args.n) > 100:
        n = int(args.n)

    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    grid = np.array([])
    if args.glider:
        grid = np.zeros(n*n).reshape(n,n)
        add_glider(1,1,grid)
    else:
        grid = random_grid(n)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = anime.FuncAnimation(fig, update, fargs=(img, grid, n, ), frames=10, save_count=50, interval=update_interval)

    if args.mov_file:
        ani.save(args.mov_file,fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()
