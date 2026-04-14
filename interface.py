"""
Interface module for the Game of Life simulation.
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pattern import PATTERNS


class Application(tk.Tk):
    """
    Main application window for the Game of Life simulation.

    Builds a full-screen Tkinter interface composed of:
        - A canvas rendering the cell grid on the left.
        - A control panel on the right with simulation controls,
          display settings, pattern placement, and a live population graph.

    Attributes:
        game (GameOfLife): The simulation logic instance.
        cell_size (int): Pixel size of each cell on the canvas.
        running (bool): Whether the simulation loop is active.
        generation (int): Current generation counter.
        history_x (list[int]): Generation indices for the population graph.
        history_y (list[int]): Population values for the population graph.
    """

    def __init__(self, game, cell_size: int = 10):
        """
        Initializes the application window and all UI components.

        Args:
            game (GameOfLife): The simulation logic instance.
            cell_size (int): Pixel size of each cell. Defaults to 10.
        """
        tk.Tk.__init__(self)
        self.game = game
        self.cell_size = cell_size
        self.running = False

        self.patterns = PATTERNS
        self.selected_pattern = tk.StringVar(value="Pixel")
        self.grid_var = tk.BooleanVar(value=False)
        self.wrap_var = tk.BooleanVar(value=True)
        self.generation = 0
        self.history_x = []
        self.history_y = []

        self.attributes('-fullscreen', True)
        self._create_widgets()
        self.update_stats()
        self.draw_matrix()

        self.bind("<Escape>", self.stop)

    def _create_widgets(self):
        """
        Builds and lays out all top-level UI components:
        the canvas, the right-side control panel, and the graph.
        """
        self.canv = tk.Canvas(
            self, bg="white",
            height=self.game.size * self.cell_size,
            width=self.game.size * self.cell_size,
        )
        self.canv.pack(side="left", padx=10, pady=10)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self._create_controls()
        self._create_graph()
        self._create_grid_rectangles()

        self.canv.bind("<Button-1>", self._on_canvas_click)
        self.canv.bind("<B1-Motion>", self._on_canvas_click)

    def _create_controls(self):
        """
        Creates the simulation control panel, including buttons for
        Play/Stop, Step, Reset, Randomize, speed slider, grid toggle,
        wrap toggle, and pattern selector.
        """
        self.button_exit = tk.Button(
            self, text="Exit", command=self.stop,
            bg="red", activebackground="darkred", fg="white",
            bd=0, width=3
        )
        self.button_exit.place(relx=1.0, rely=0.0, anchor="ne")

        tk.Frame(self.right_frame, height=60).pack()

        sim_frame = tk.LabelFrame(self.right_frame, text=" Simulation ", padx=10, pady=10)
        sim_frame.pack(fill="x", padx=10, pady=5)

        self.button_toggle = tk.Button(sim_frame, text="Play", command=self.toggle_simulation)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=2, pady=5)

        tk.Button(sim_frame, text="Step", command=self.manual_step).grid(row=0, column=1, sticky="ew", padx=2)
        tk.Button(sim_frame, text="Reset", command=self.reset).grid(row=1, column=0, sticky="ew", padx=2)
        tk.Button(sim_frame, text="Random", command=self._randomize_and_draw).grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        sim_frame.columnconfigure(0, weight=1)
        sim_frame.columnconfigure(1, weight=1)

        columns_container = tk.Frame(self.right_frame)
        columns_container.pack(fill="x", padx=10, pady=5)

        settings_frame = tk.LabelFrame(columns_container, text="Parameters", padx=10, pady=10)
        settings_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.slider = tk.Scale(settings_frame, from_=1, to=60, label="Speed (FPS)", orient="horizontal")
        self.slider.set(60)
        self.slider.pack(fill="x")
        tk.Checkbutton(settings_frame, text="Grid", variable=self.grid_var, command=self.toggle_grid_display).pack(anchor="w")
        tk.Checkbutton(settings_frame, text="Wrap", variable=self.wrap_var).pack(anchor="w")

        draw_frame = tk.LabelFrame(columns_container, text="Drawing", padx=10, pady=10)
        draw_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.menu_pattern = tk.OptionMenu(draw_frame, self.selected_pattern, *self.patterns.keys())
        self.menu_pattern.pack(fill="x", pady=5)
        tk.Label(draw_frame, text="Click to place").pack()

    def _create_graph(self):
        """
        Creates the matplotlib population graph embedded in the right panel.
        """
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Population over time")
        self.line, = self.ax.plot([], [], color="blue", marker="o", markersize=2)
        self.canvas_plt = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas_plt.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _create_grid_rectangles(self):
        """
        Pre-creates all cell rectangles on the canvas for efficient rendering.
        Stored in self.rectangles[row][col] for direct access during updates.
        """
        self.rectangles = []
        outline = "lightgrey" if self.grid_var.get() else ""
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                rect = self.canv.create_rectangle(
                    x1, y1, x1 + self.cell_size, y1 + self.cell_size,
                    fill="white", outline=outline
                )
                row.append(rect)
            self.rectangles.append(row)

    def toggle_simulation(self):
        """
        Starts or stops the automatic simulation loop.
        Updates the toggle button label accordingly.
        """
        if not self.running:
            self.running = True
            self.button_toggle.config(text="Stop")
            self.next_step()
        else:
            self.running = False
            self.button_toggle.config(text="Play")

    def manual_step(self):
        """
        Advances the simulation by exactly one generation.
        Only effective when the simulation is not running.
        """
        if not self.running:
            self.game.step(self.wrap_var.get())
            self.draw_matrix()
            self.update_stats()

    def reset(self):
        """
        Stops the simulation and resets the grid, generation counter,
        and population history to their initial empty states.
        """
        self.running = False
        self.button_toggle.config(text="Play")
        self.generation = 0
        self.history_x, self.history_y = [], []
        self.game.reset()
        self.draw_matrix()
        self.update_stats()

    def next_step(self):
        """
        Executes one simulation step and schedules the next one
        based on the current speed slider value. Stops if running is False.
        """
        if self.running:
            self.game.step(self.wrap_var.get())
            self.draw_matrix()
            self.update_stats()
            self.after(round(1000 / self.slider.get()), self.next_step)

    def draw_matrix(self):
        """
        Redraws all canvas cells to reflect the current grid state.
        Alive cells are black; dead cells are white.
        """
        for i in range(self.game.size):
            for j in range(self.game.size):
                color = "black" if self.game.matrix[i][j] else "white"
                self.canv.itemconfig(self.rectangles[i][j], fill=color)

    def update_stats(self):
        """
        Records the current population and generation index,
        then refreshes the population graph.
        """
        population = sum(sum(row) for row in self.game.matrix)
        self.history_x.append(self.generation)
        self.history_y.append(population)
        self.generation += 1
        self._refresh_graph()

    def _refresh_graph(self):
        """
        Updates the matplotlib line plot with the latest population history
        and redraws the canvas.
        """
        self.line.set_data(self.history_x, self.history_y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_plt.draw_idle()

    def _randomize_and_draw(self):
        """
        Resets the grid, fills it randomly, and refreshes the display.
        """
        self.reset()
        self.game.random_fill()
        self.draw_matrix()
        self.update_stats()

    def toggle_grid_display(self):
        """
        Toggles the visual grid lines between visible (light grey) and hidden.
        """
        outline = "lightgrey" if self.grid_var.get() else ""
        for row in self.rectangles:
            for rect in row:
                self.canv.itemconfig(rect, outline=outline)

    def _on_canvas_click(self, event):
        """
        Handles mouse click and drag on the canvas to place the selected pattern.

        Args:
            event: Tkinter mouse event containing x and y canvas coordinates.
        """
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.game.size and 0 <= col < self.game.size:
            pattern_coords = self.patterns[self.selected_pattern.get()]
            self.game.place_pattern(pattern_coords, row, col)
            self.draw_matrix()

    def stop(self, _event=None):
        """
        Closes the application window and terminates the simulation.

        Args:
            _event: Optional Tkinter event (used when bound to keyboard shortcut).
        """
        self.destroy()
