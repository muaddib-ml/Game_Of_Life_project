"""
Entry point for the Game of Life simulation.
 
This module initializes the game logic and launches the graphical interface.
The grid size can be adjusted via the SIZE constant.
"""
import logic
import interface


if __name__ == "__main__":
    SIZE = 50
    game_of_life = logic.GameOfLife(SIZE)
    app = interface.Application(game_of_life)
    app.title("Game of Life")
    app.mainloop()
