
"""
Interface module for the Game of Life simulation.
 
This module contains the Application class which handles the graphical
display of the grid using tkinter.
"""
import tkinter as tk


class Application(tk.Tk):
    """
    A tkinter-based graphical interface for the Game of Life simulation.
 
    This class manages the canvas rendering of the grid, updating it at
    each step of the simulation.
 
    Attributes:
        game (GameOfLife): The game logic instance managing the grid state.
        cell_size (int): The size in pixels of each cell on the canvas.
        canv (tk.Canvas): The canvas widget used to draw the grid.
    """

    def __init__(self, game, cell_size=10):
        """
        Initializes the application window and starts the simulation loop.
 
        Args:
            game (GameOfLife): An instance of the GameOfLife logic class.
            cell_size (int): The size in pixels of each cell. Defaults to 10.
        """
        tk.Tk.__init__(self)
        self.game = game
        self.cell_size = cell_size
        self.create_widget()
        self.draw_matrix()
        self.bind("<Escape>", self.stop)
        self.next_step()

    def create_widget(self):
        """
        Creates and packs the canvas widget sized to fit the entire grid.
        """
        self.canv = tk.Canvas(
            self, bg="white",
            height=self.game.size * self.cell_size,
            width=self.game.size * self.cell_size
            )
        self.canv.pack()

    def draw_matrix(self):
        """
        Redraws the entire grid on the canvas based on the current matrix state.
 
        Live cells (1) are drawn in black, dead cells (0) in white.
        """
        self.canv.delete("all")
        for i in range(self.game.size):
            for j in range(self.game.size):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = (i+1) * self.cell_size, (j+1) * self.cell_size
                if self.game.matrix[i][j] == 1:
                    self.canv.create_rectangle(x1, y1, x2, y2, fill="black", outline="lightgrey")
                else:
                    self.canv.create_rectangle(x1, y1, x2, y2, fill="white", outline="lightgrey")

    def stop(self, _event=None):
        """
        Quits the application.
 
        Args:
            event: The tkinter event triggered by pressing Escape. Defaults to None.
        """
        self.quit()

    def next_step(self):
        """
        Advances the simulation by one step and schedules the next update.
 
        Calls the game's step method, redraws the grid, then schedules
        itself to run again after 500 milliseconds.
        """
        self.game.step()
        self.draw_matrix()
        self.after(500, self.next_step)
