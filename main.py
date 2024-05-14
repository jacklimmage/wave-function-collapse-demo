import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from matplotlib.widgets import TextBox, Button
import sys

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
        self.numRows = 10
        self.numCols = 20
        self.numMaps = 1

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

        cmap = colors.ListedColormap(['#000000', # black
                                      '#1E90FF', # blue
                                      '#00C5CD', # cyan
                                      '#FFE37E', # yellow
                                      '#639E51', # green
                                      '#808080', # grey
                                      '#FFFFFF']) # white
        bounds = [0, 1, 2, 3, 4, 5, 6, 7]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        plt.rcParams['toolbar'] = 'toolbar2'

        fig, ax = plt.subplots()
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        
        ax.axis('off')
        img = plt.imshow(grid.mapGrid, animated=True, cmap=cmap, norm=norm)
        
        def animate(i):
            if not grid.wave_function_collapsed():
                grid.update_cell()
                updatedMap = grid.mapGrid
                img.set_array(updatedMap)
            return img,
        
        interval = 10000 / (grid.numRows * grid.numCols) #ms
        print(interval)
        ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)
        plt.show()

    plt.close()

def handle_input(grid):

    def update_rows(text):
        try:
            numRows = int(text)
            if numRows > 0:
                grid.numRows = numRows
                buttonObj.rowsValid = True
                buttonObj.tryButtonToggle(startButton, True)
            else: 
                buttonObj.tryButtonToggle(startButton, False)
                buttonObj.rowsValid = False
        except ValueError:
            buttonObj.tryButtonToggle(startButton, False)
            buttonObj.rowsValid = False

    def update_cols(text):
        try:
            numCols = int(text)
            if numCols > 0:
                grid.numCols = numCols
                buttonObj.colsValid = True
                buttonObj.tryButtonToggle(startButton, True)
            else: 
                buttonObj.tryButtonToggle(startButton, False)
                buttonObj.rowsValid = False
        except ValueError:
            buttonObj.tryButtonToggle(startButton, False)
            buttonObj.colsValid = False

    def update_maps(text):
        try:
            numMaps = int(text)
            if numMaps > 0:
                grid.numMaps = numMaps
                buttonObj.mapsValid = True
                buttonObj.tryButtonToggle(startButton, True)
            else: 
                buttonObj.tryButtonToggle(startButton, False)
                buttonObj.mapsValid = False
        except ValueError:
            buttonObj.tryButtonToggle(startButton, False)
            buttonObj.mapsValid = False

    plt.rcParams['toolbar'] = 'None'
    fig = plt.figure("Enter Parameters", (3,2)) # (width, height)

    axNumRows = plt.axes([0.5, 0.75, 0.2, 0.1])  # [left, bottom, width, height]
    textboxNumRows = TextBox(axNumRows, 'Num Rows: ', initial='10')
    textboxNumRows.on_submit(update_rows)

    axNumCols = plt.axes([0.5, 0.6, 0.2, 0.1])  # [left, bottom, width, height]
    textboxNumCols = TextBox(axNumCols, 'Num Cols: ', initial='20')
    textboxNumCols.on_submit(update_cols)

    axNumMaps = plt.axes([0.5, 0.45, 0.2, 0.1])  # [left, bottom, width, height]
    textboxNumMaps = TextBox(axNumMaps, 'Num Maps: ', initial='1')
    textboxNumMaps.on_submit(update_maps)

    # Function to start the animation when the button is clicked
    class buttonHandler:
        def __init__(self, startButton) -> None:
            self.buttonPressed = False
            self.rowsValid = True
            self.colsValid = True
            self.mapsValid = True
            self.tryButtonToggle(startButton, True)
        
        def tryButtonToggle(self, startButton, to):
            if not to:
                self.canBePressed = False
                startButton.hovercolor = 'r'
            else:
                if self.rowsValid and self.colsValid and self.mapsValid:
                    self.canBePressed = True
                    startButton.hovercolor = 'g'

    # Add a button to start the animation
    axButton = plt.axes([0.5, 0.3, 0.2, 0.1])  # [left, bottom, width, height]
    startButton = Button(axButton, 'Start')

    buttonObj = buttonHandler(startButton)
    def start_animation(event):
        if buttonObj.canBePressed:
            buttonObj.buttonPressed = True
            plt.close()

    startButton.on_clicked(start_animation)

    plt.show()
    while not buttonObj.buttonPressed:
        if not plt.fignum_exists(1):  # Check if the figure window is closed
            sys.exit()

if __name__ == "__main__":
    main()