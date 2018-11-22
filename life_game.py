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
            living_neighbours = int((grid[i, (j-1)%n] +
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
    glider = np.array([[255,255,255],
                       [255,255,255],
                       [255,255,255]])
    grid[i:i+3, j:j+3] = glider

def add_cube(i, j, grid):
    qube = np.array([[255, 255],
                     [255, 255]])
    grid[i:i + 2, j:j + 2] = qube

def add_gosper_glider_gun(i,j,grid):
    qube = np.array([[255,255],
                    [255,255]])
    grid[i:i+2, j:j+2] = qube
    i = i + 2 - 4
    j = j + 2 + 8   # przesunięcie do następnego elementu pierwsza wartość oznacza miejsce zajęte przez figurę druga odległość

    crucible = np.array([[0,  0,   255, 255, 0,   0,   0,  0],
                        [0,   255, 0,   0,   0,   255, 0,  0],
                        [255, 0,   0,   0,   0,   0,   255, 0],
                        [255, 0,   0,   0,   255, 0,   255, 255],
                        [255, 0,   0,   0,   0,   0,   255,  0],
                        [0,   255, 0,   0,   0,   255, 0,  0],
                        [0,   0,   255, 255, 0,   0,   0,  0]
                        ])
    grid[i:i + 7, j:j + 8] = crucible

    i = i + 8 - 10
    j = j + 7 + 3

    gun = np.array([[0,   0,   0,   0, 255],
                    [0,   0,   255, 0, 255],
                    [255, 255, 0,   0, 0],
                    [255, 255, 0,   0, 0],
                    [255, 255, 0,   0, 0],
                    [0,   0,   255, 0, 255],
                    [0,   0,   0,   0, 255],
                    ]
                   )
    grid[i:i+7, j:j+5] = gun

    i = i + 7 - 5
    j = j + 5 + 9

    grid[i:i+2, j:j+2] = qube

def load_pattern_from_file():
    file = open("pattern.txt", 'r')
    elements = file.read().split(' ')
    array = []
    for element in elements:
        array.append(int(element))
    file.close()
    return array;

def main():
    parser = argparse.ArgumentParser(description="Uruchamianie gry w życie Conwaya.")
    # argumenty
    parser.add_argument('--grid-size', dest='n', required=False)    # wielkość siatki
    parser.add_argument('--mov-file', dest='mov_file', required=False)  # nazwa pliku .mov
    parser.add_argument('--interval', dest='interval', required=False)  # przerwa między animacjiami w milisekundach
    parser.add_argument('--glider', action='store_true', required=False)    # rozpoczynanie ze strukturą szybowca
    parser.add_argument('--glider_gun', action='store_true', required=False) # dodanie glider gun'a ale nie działa :/
    parser.add_argument('--qube', action='store_true', required=False) # dodanie twórcę szybowców
    parser.add_argument('--pattern_file', action='store_true', required=False) # wczytanie konfiguracji z pliku
    args = parser.parse_args()

    n = 20

    if args.n and int(args.n) > 100:
        n = int(args.n)

    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    grid = np.array([])


    if args.glider:
        grid = np.zeros(n*n).reshape(n,n)
        add_glider(1,1,grid)

    elif args.glider_gun:
        grid = np.zeros(n*n).reshape(n,n)
        add_gosper_glider_gun(10,5,grid)

    elif args.qube:
        grid = np.zeros(n * n).reshape(n, n)
        add_cube(1,1,grid)

    elif args.pattern_file:

        params = np.array(load_pattern_from_file())
        n = int(params[0])
        grid = np.zeros(n * n)
        params = params[1:]
        grid = grid.flatten()
        grid[0:len(params)] = params
        grid = grid.reshape(n,n)

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
