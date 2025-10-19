import random

# Hexomino shapes: each is a list of (x, y) offsets
SHAPES = [
    # Straight
    {
        'shape': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
        'color': (0, 255, 255)  # Cyan
    },
    # L
    {
        'shape': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4)],
        'color': (255, 165, 0)  # Orange
    },
    # Bent
    {
        'shape': [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
        'color': (0, 0, 255)  # Blue
    },
    # T
    {
        'shape': [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3)],
        'color': (128, 0, 128)  # Purple
    },
    # S
    {
        'shape': [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
        'color': (0, 255, 0)  # Green
    },
    # Z
    {
        'shape': [(0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (3, -1)],
        'color': (255, 0, 0)  # Red
    },
    # Plus-like
    {
        'shape': [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)],
        'color': (255, 255, 0)  # Yellow
    }
]

def get_random_piece():
    return random.choice(SHAPES).copy()

# Function to rotate a shape 90 degrees clockwise
def rotate_shape(shape):
    return [(-y, x) for x, y in shape]