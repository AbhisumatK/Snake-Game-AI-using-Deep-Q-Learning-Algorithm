import numpy as np

def render(game, block_size=20):
    h, w = game.h, game.w
    frame = np.zeros((h, w, 3), dtype=np.uint8)

    # Draw snake (purple)
    for pt in game.snake:
        frame[
            pt.y:pt.y + block_size,
            pt.x:pt.x + block_size
        ] = (160, 60, 220)

    # Draw food (orange)
    fx, fy = game.food.x, game.food.y
    frame[
        fy:fy + block_size,
        fx:fx + block_size
    ] = (255, 165, 0)

    return frame
