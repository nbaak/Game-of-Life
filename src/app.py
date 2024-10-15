#!/usr/bin/env python3

import pygame
import datetime
import numpy as np
from typing import Tuple

from colors import Colors

# Constants
CELL_SIZE = 20
GRID_WIDTH = 1800 // CELL_SIZE
GRID_HEIGHT = 900 // CELL_SIZE
FPS = 10


def take_screenshot(surface:pygame.Surface):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Screenshot saved as {filename}")
    
    
def get_neighbours(grid:np.ndarray, x:int, y:int) -> int:
    """Returns the number of alive neighbours of a cell."""
    total = np.sum(grid[max(0, x - 1):min(x + 2, GRID_WIDTH),
                        max(0, y - 1):min(y + 2, GRID_HEIGHT)])
    return total - grid[x, y]


def update_grid(grid:np.ndarray) -> np.ndarray:
    """Updates the grid based on Conway's Game of Life rules."""
    new_grid = np.copy(grid)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            alive_neighbours = get_neighbours(grid, x, y)
            if grid[x, y] == 1 and (alive_neighbours < 2 or alive_neighbours > 3):
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and alive_neighbours == 3:
                new_grid[x, y] = 1
    return new_grid


def draw_grid(screen:pygame.Surface, grid:np.ndarray) -> None:
    """Draws the grid on the screen with thin lines."""
    screen.fill(Colors.BACKGROUND)
    
    # Draw cells
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x, y] == 1:
                pygame.draw.rect(screen, Colors.ALIVE, rect)

    # Draw thin grid lines
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, Colors.LINE, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
    for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, Colors.LINE, (0, y), (GRID_WIDTH * CELL_SIZE, y))


def handle_mouse_click(grid:np.ndarray, pos:Tuple[int, int]) -> None:
    """Toggles the state of the clicked cell."""
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    grid[x, y] = 1 - grid[x, y]  # Toggle cell state


def handle_mouse_hold(grid:np.ndarray) -> None:
    """Handles continuous drawing when the mouse button is held."""
    if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
        handle_mouse_click(grid, pygame.mouse.get_pos())
        
        
def main():
    pygame.init()
    
    pygame.display.set_caption("Pygame of Life")
    pygame.init()
    surface = screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    surface.fill(Colors.BACKGROUND)    
    clock = pygame.time.Clock()

    # Create the grid
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

    running = True
    paused = True

    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q: running = False
                    case pygame.K_SPACE: take_screenshot(surface)
                    case pygame.K_p: paused = not paused  # toggle pause
                    
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     handle_mouse_click(grid, pygame.mouse.get_pos())
                
        handle_mouse_hold(grid)
                    
        # App
        if not paused:
            grid = update_grid(grid)

        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
