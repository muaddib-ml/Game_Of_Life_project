# Python Project: Conway's Game of Life (L3 BI) 🧬

This project implements the **Game of Life**, a cellular automaton devised by the mathematician **John Horton Conway** in 1970. It is a model where each state leads mechanically to the next based on pre-established rules.

## 📋 Project Overview
The objective is to simulate a two-dimensional grid where each cell is defined as either "alive" (1) or "dead" (0). At each step, the evolution of a cell is determined by the state of its 8 neighbors:

* **Birth**: A dead cell with exactly three live neighbors becomes alive.
* **Survival**: A live cell with two or three live neighbors remains alive; otherwise, it dies.

## 🛠️ Project Structure
The project is organized into several modules to ensure a clear separation between logic and display:

1.  **`logic.py`**: Contains the `GameOfLife` class.
    * Initializes an N x N matrix.
    * Randomly populates the grid with 0s and 1s.
    * Calculates the number of live neighbors for each cell.
    * Computes the survival/state of each cell for the next generation.
2.  **`interface.py`**: Manages the graphical display using the **Tkinter** library.
    * Real-time rendering of cells (Black for alive, White for dead).
    * Handles the simulation loop using the `.after()` method.
3.  **`main.py`**: The entry point of the program.
    * Initializes the game logic and launches the graphical interface.

## 🚀 Installation and Usage

### Prerequisites
* Python 3.x
* `tkinter` library (usually included in standard Python installations).
* `random` module (standard library, used for grid initialization).

### Running the Simulation
To start the simulation (default size: 50x50), run the following command in your terminal:

```bash
python main.py
```
Press **Escape (Esc)** to close the window and terminate the program.
