
# 🧬 Conway's Game of Life – Python Project (L3 BI)

This project implements the **Game of Life**, a cellular automaton devised by **John Horton Conway** in 1970.  
It simulates the evolution of a population of cells on a 2D grid based on simple deterministic rules.

---

## 📋 Project Overview

The simulation is based on a square grid where each cell can be:
- **Alive (1)**
- **Dead (0)**

At each generation, the state of each cell depends on its 8 neighbors:

- **Birth**: A dead cell with exactly 3 live neighbors becomes alive  
- **Survival**: A live cell with 2 or 3 neighbors survives  
- **Death**: All other cells die or remain dead  

<div align="center">			
<img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif"/>
</div>

---

## ✨ Features

This implementation goes beyond a basic Game of Life:

### 🖥️ Interactive Graphical Interface
- Built with **Tkinter**
- Real-time rendering of the grid
- Click & drag to draw cells or patterns

### 🎮 Simulation Controls
- ▶️ Play / Stop simulation  
- ⏭️ Step-by-step execution  
- 🔄 Reset grid  
- 🎲 Random initialization  

### ⚙️ Parameters
- Adjustable simulation speed (**FPS slider**)  
- Grid display toggle  
- Edge behavior:
  - **Wrap ON** → toroidal grid  
  - **Wrap OFF** → fixed boundaries  

### 🧩 Pattern System
- Predefined patterns (via `PATTERNS`)
- Selectable from a dropdown menu
- Click to place directly on the grid

### 📈 Population Graph
- Real-time population tracking using **Matplotlib**
- Displays evolution of living cells over generations

---

## 🛠️ Project Structure
.
├── main.py # Entry point of the program
├── logic.py # Simulation logic (GameOfLife class)
├── interface.py # Graphical interface (Tkinter + Matplotlib)
├── pattern.py # Predefined patterns

### 🔬 `logic.py`
Handles all simulation mechanics:
- Grid initialization
- Random population
- Neighbor computation:
  - With boundaries
  - With wrapping (toroidal topology)
- State updates (Conway rules)
- Pattern placement

### 🎨 `interface.py`
Manages the graphical interface:
- Canvas rendering (optimized with pre-created rectangles)
- User interactions (mouse input)
- Simulation loop using `.after()`
- Control panel (buttons, sliders, toggles)
- Live population graph

### 🚀 `main.py`
- Initializes the simulation
- Launches the interface

---

## 🚀 Installation and Usage

### ✅ Prerequisites
- Python 3.x  
- Standard libraries:
  - `tkinter`
  - `random`
- External library:
  - `matplotlib`

Install matplotlib if needed:
```bash
pip install matplotlib
