"""
Interface module for the Game of Life simulation.

This module contains the Application class which handles the graphical
display of the grid using tkinter.
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Tk):
    """
    A tkinter-based graphical interface for the Game of Life simulation.

    This class manages the canvas rendering of the grid, updating it at
    each step of the simulation.

    Attributes:
        game (GameOfLife): The game logic instance managing the grid state.
        cell_size (int): The size in pixels of each cell on the canvas.
        canv (tk.Canvas): The canvas widget used to draw the grid.
        running (bool): Whether the simulation is currently running.
        generation (int): The current generation count.
        history_x (list): List of generation indices for the population graph.
        history_y (list): List of population values for the population graph.
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
        self.running = False
        self.generation = 0
        self.history_x = []
        self.history_y = []
        self._create_widgets()
        self.update_stats()
        self.draw_matrix()
        self.bind("<Escape>", self.stop)

    # -------------------------------------------------------------------------
    # Widget creation
    # -------------------------------------------------------------------------

    def _create_widgets(self):
        """
        Creates and lays out all widgets: grid canvas, controls, and graph.
        """
        # Left zone: grid
        self.canv = tk.Canvas(
            self, bg="white",
            height=self.game.size * self.cell_size,
            width=self.game.size * self.cell_size,
        )
        self.canv.pack(side="left", padx=10, pady=10)

        # Right zone: controls and graph
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self._create_controls()
        self._create_graph()
        self._create_grid_rectangles()

    def _create_controls(self):
        """
        Creates and packs the speed slider and control buttons (Play, Stop, Reset).
        """
        self.slider = tk.Scale(
            self.right_frame, from_=1, to=60,
            label="Vitesse (FPS)", orient="horizontal",
        )
        self.slider.set(60)
        self.slider.pack(fill="x")

        self.button_play = tk.Button(
            self.right_frame, text="Jouer", command=self.start_simulation
        )
        self.button_play.pack(fill="x")

        self.button_stop = tk.Button(
            self.right_frame, text="Stop", command=self.freeze
        )
        self.button_stop.pack(fill="x")

        self.button_reset = tk.Button(
            self.right_frame, text="Reset", command=self.reset
        )
        self.button_reset.pack(fill="x")

    def _create_graph(self):
        """
        Creates and embeds the Matplotlib population-over-time graph.
        """
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Population au cours du temps")
        self.line, = self.ax.plot([], [], color="blue", marker="o", markersize=2)

        self.canvas_plt = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas_plt.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _create_grid_rectangles(self):
        """
        Pre-creates all rectangle items on the canvas for the grid cells.

        Storing rectangle IDs avoids recreating them on every redraw,
        which significantly improves rendering performance.
        """
        self.rectangles = []
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = (j + 1) * self.cell_size, (i + 1) * self.cell_size
                rect = self.canv.create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="lightgrey"
                )
                row.append(rect)
            self.rectangles.append(row)

    # -------------------------------------------------------------------------
    # Simulation control
    # -------------------------------------------------------------------------

    def start_simulation(self):
        """
        Starts the simulation loop if it is not already running.
        """
        if not self.running:
            self.running = True
            self.next_step()

    def freeze(self):
        """
        Pauses the simulation without resetting its state.
        """
        self.running = False

    def reset(self):
        """
        Stops the simulation and resets the game, generation counter, and graph.
        """
        self.running = False
        self.generation = 0
        self.history_x = []
        self.history_y = []
        self.game.reset()
        self.draw_matrix()
        self._refresh_graph()

    def next_step(self):
        """
        Advances the simulation by one step and schedules the next update.

        Calls the game's step method, redraws the grid, updates the population
        graph, then schedules itself to run again after the slider delay.
        """
        if self.running:
            self.game.step()
            self.draw_matrix()
            self.update_stats()
            self.after(round(1000/self.slider.get()), self.next_step)

    def stop(self, _event=None):
        """
        Quits the application.

        Args:
            _event: The tkinter event triggered by pressing Escape. Defaults to None.
        """
        self.quit()

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    def draw_matrix(self):
        """
        Redraws the entire grid on the canvas based on the current matrix state.

        Live cells (1) are drawn in black, dead cells (0) in white.
        """
        for i in range(self.game.size):
            for j in range(self.game.size):
                color = "black" if self.game.matrix[i][j] else "white"
                self.canv.itemconfig(self.rectangles[i][j], fill=color)

    def update_stats(self):
        """
        Computes the current population, appends it to the history, and
        refreshes the Matplotlib graph. Increments the generation counter.

        Raises:
            ValueError: If the game matrix contains unexpected values.
        """
        # Use the generation kept in sync with game steps (starts at 0)
        pop = sum(cell for row in self.game.matrix for cell in row)

        self.history_x.append(self.generation)
        self.history_y.append(pop)
        self.generation += 1

        self._refresh_graph()

    def _refresh_graph(self):
        """
        Updates the Matplotlib line data and forces a canvas redraw.
        """
        self.line.set_data(self.history_x, self.history_y)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.canvas_plt.draw()
        self.canvas_plt.flush_events()
