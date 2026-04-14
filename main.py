"""
Entry point for the Game of Life simulation.

Initializes the game logic and launches the graphical interface.
The grid size can be adjusted via the SIZE constant.
"""
import logic
import interface


SIZE = 100

if __name__ == "__main__":
    game_of_life = logic.GameOfLife(SIZE)
    app = interface.Application(game_of_life)
    app.title("Game of Life")
    app.mainloop()
