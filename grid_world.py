class GridWorld:
    def __init__(self):
        self.grid = [["| |" for i in range(10)] for j in range(7)]
        self.starting = (3, 0)
        self.goal = (3, 7)
        self.grid[self.starting[0]][self.starting[1]] = "|S|"
        self.grid[self.goal[0]][self.goal[1]] = "|G|"
        self.winds = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

    def print_grid(self):
        for i in range(len(self.grid)):
            print(([''.join(['{:8}'.format(item) for item in self.grid[i]])]))
        print("\n")


a = GridWorld()
a.print_grid()
