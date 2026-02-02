import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import numpy as np
import pygame

pygame.init()

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
PURPLE1 = (90, 30, 160)
PURPLE2 = (170, 90, 255)

def render(game, block_size=20):
    surface = pygame.Surface((game.w, game.h))
    surface.fill(BLACK)

    for pt in game.snake:
        pygame.draw.rect(surface, PURPLE1, pygame.Rect(pt.x, pt.y, block_size, block_size))
        pygame.draw.rect(surface, PURPLE2, pygame.Rect(pt.x + 4, pt.y + 4, block_size - 8, block_size - 8))

    pygame.draw.rect(surface, ORANGE, pygame.Rect(game.food.x, game.food.y, block_size, block_size))

    frame = pygame.surfarray.array3d(surface)
    return np.transpose(frame, (1, 0, 2))