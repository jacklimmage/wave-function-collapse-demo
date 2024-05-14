import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from matplotlib.widgets import TextBox, Button

# ANSI escape codes for colours
class Colours:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GREY = '\033[90m'
    BLACK = '\033[30m'

class TerrainList:
    def __init__(self) -> None:
        self.availTerrains = ['M', 'm', 'g', 's', 'w', 'W']

    def semi_collapse(self, terrain):
        allTerrains = ['M', 'm', 'g', 's', 'w', 'W']
        match terrain:
            case 'M': 
                for char in allTerrains:
                    if char not in ['M', 'm'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
            case 'm':
                for char in allTerrains:
                    if char not in ['M', 'm', 'g'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
            case 'g':
                for char in allTerrains:
                    if char not in ['m', 'g', 's'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
            case 's':
                for char in allTerrains:
                    if char not in ['g', 's', 'w'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
            case 'w':
                for char in allTerrains:
                    if char not in ['s', 'w', 'W'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
            case 'W':
                for char in allTerrains:
                    if char not in ['w', 'W'] and char in self.availTerrains:
                        self.availTerrains.remove(char)
    
    def collapse(self, terrain):
        self.availTerrains = [terrain]

class Grid:
    def __init__(self) -> None:
        self.numRows = 0
        self.numCols = 0
        self.numMaps = 0

        self.superpositionGrid = []
        self.mapGrid = []
        self.entropyGrid = []
        self.entropyDict = {}

    def get_entropy_dict(self):
        self.entropyDict = {}
        for j, row in enumerate(self.entropyGrid):
            for i, value in enumerate(row):
                if value not in self.entropyDict:
                    self.entropyDict[value] = []
                self.entropyDict[value].append([i, j])
        return self.entropyDict

    def display_map(self):
        for j, row in enumerate(self.mapGrid):
            toPrint = ""
            for i, cell in enumerate(row):
                match cell:
                    case 0:
                        toPrint += Colours.BLACK 
                    case 1:
                        toPrint += Colours.BLUE
                    case 2:
                        toPrint += Colours.CYAN
                    case 3:
                        toPrint += Colours.YELLOW
                    case 4:
                        toPrint += Colours.GREEN
                    case 5:
                        toPrint += Colours.GREY
                    case 6:
                        toPrint += Colours.WHITE
                toPrint += "\u2588\u2588" + Colours.RESET
            print(toPrint)

    def update_cell(self):
        self.entropyGrid = []
        self.entropyDict = {}
        self.get_entropy_grid()
        self.get_entropy_dict()
        coords = self.get_lowest_entropy()

        x = coords[0]
        y = coords[1]
        colourDict = {
            'W': 1,
            'w': 2,
            's': 3,
            'g': 4,
            'm': 5,
            'M': 6,
        }
        availTerrains = self.superpositionGrid[y][x].availTerrains
        terrain = random.choice(availTerrains)
        self.superpositionGrid[y][x].collapse(terrain)
        self.mapGrid[y][x] = colourDict[terrain]
        minX = max(0, x - 1)
        maxX = min(len(self.mapGrid[0]) - 1, x + 1)
        minY = max(0, y - 1)
        maxY = min(len(self.mapGrid) - 1, y + 1)
        for j in range(minY, maxY + 1):
            for i in range(minX, maxX + 1):
                if j == y and i == x:
                    continue
                self.superpositionGrid[j][i].semi_collapse(terrain)

    def get_entropy_grid(self):
        self.entropyGrid = [[len(cell.availTerrains) for cell in row] for row in self.superpositionGrid]

    def get_lowest_entropy(self):
        for entropy in range(2, 7):
            if entropy in self.entropyDict:
                coords = random.choice(self.entropyDict[entropy])
                break
        return coords

    def handle_input(self):
        # Get num rows and cols
        while True:
            rowsInput = input("Enter number of rows (enter '1' for 1D with time axis): ")
            try:
                numRows = int(rowsInput)
                if numRows > 0:
                    self.numRows = numRows
                    break
                else: 
                    print("Please enter a positive integer")
            except ValueError:
                print("Please enter an integer")
        while True:
            colInput = input("Enter number of columns: ")
            try:
                numCols = int(colInput)
                if numCols > 0:
                    self.numCols = numCols
                    break
                else: 
                    print("Please enter a positive integer")
            except ValueError:
                print("Please enter an integer")
        # Get num maps
        while True:
            mapsInput = input("Enter number of maps: ")
            try:
                numMaps = int(mapsInput)
                if numMaps > 0:
                    self.numMaps = numMaps
                    break
                else: 
                    print("Please enter a positive integer")
            except ValueError:
                print("Please enter an integer")

    def initialise_superposition_grid(self):
        self.superpositionGrid = []
        for j in range(self.numRows):
            row = []
            for i in range(self.numCols):
                row.append(TerrainList())
            self.superpositionGrid.append(row)

    def initialise_map(self):
        self.mapGrid = []
        for j in range(self.numRows):
            row = []
            for i in range(self.numCols):
                row.append(0)
            self.mapGrid.append(row)

    def wave_function_collapsed(self):
        ret = True
        for row in self.mapGrid:
            for cell in row:
                if cell == 0:
                    ret = False
        return ret

def main():
    grid = Grid()
    handle_input(grid)

    for i in range(grid.numMaps):
        grid.initialise_superposition_grid()
        grid.initialise_map()

        cmap = colors.ListedColormap(['k', 'b', 'c', 'y', 'g', '0.5', '1'])
        bounds = [0, 1, 2, 3, 4, 5, 6, 7]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig, ax = plt.subplots()
        ax.axis('off')
        img = plt.imshow(grid.mapGrid, animated=True, cmap=cmap, norm=norm)
        
        def animate(i):
            if not grid.wave_function_collapsed():
                grid.update_cell()
                updatedMap = grid.mapGrid
                img.set_array(updatedMap)
            return img,
        
        ani = animation.FuncAnimation(fig, animate, frames=24, interval=100, blit=True)
        plt.show()

def handle_input(grid):

    def update_rows(text):
        grid.numRows = int(text)

    def update_cols(text):
        grid.numCols = int(text)

    def update_maps(text):
        grid.numMaps = int(text)

    ax_numrows = plt.axes([0.9, 0.7, 0.1, 0.03])  # [left, bottom, width, height]
    textbox_numrows = TextBox(ax_numrows, 'Num Rows', initial='10')
    update_rows(10)
    textbox_numrows.on_submit(update_rows)

    ax_numcols = plt.axes([0.85, 0.65, 0.1, 0.03])  # [left, bottom, width, height]
    textbox_numcols = TextBox(ax_numcols, 'Num Cols', initial='10')
    update_cols(10)
    textbox_numcols.on_submit(update_cols)

    ax_custom = plt.axes([0.85, 0.6, 0.1, 0.03])  # [left, bottom, width, height]
    textbox_custom = TextBox(ax_custom, 'Num Maps', initial='1')
    update_maps(1)
    textbox_custom.on_submit(update_maps)

    # Function to start the animation when the button is clicked
    class buttonHandler:
        def __init__(self) -> None:
            self.buttonPressed = False

    button = buttonHandler()
    def start_animation(event):
        button.buttonPressed = True
        plt.close()

    # Add a button to start the animation
    button_ax = plt.axes([0.85, 0.1, 0.1, 0.05])  # [left, bottom, width, height]
    start_button = Button(button_ax, 'Start')
    start_button.on_clicked(start_animation)

    plt.show()
    while not button.buttonPressed:
        pass

if __name__ == "__main__":
    main()