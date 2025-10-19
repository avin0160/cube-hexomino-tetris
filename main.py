import pygame
from pieces import get_random_piece, rotate_shape
import random

pygame.init()

# Constants
BLOCK_SIZE = 30
PLAYFIELD_WIDTH = 12
PLAYFIELD_HEIGHT = 24
SCREEN_WIDTH = PLAYFIELD_WIDTH * BLOCK_SIZE + 200  # Extra for UI
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hexomino Tetris")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 24)

# Playfield: 2D list, 0 empty, tuple color if occupied
playfield = [[0 for _ in range(PLAYFIELD_WIDTH)] for _ in range(PLAYFIELD_HEIGHT)]

# Current piece
current_piece = None
piece_x = 0
piece_y = 0

# Game variables
score = 0
level = 1
lines_cleared = 0
game_over = False
fall_time = 0
fall_speed = 500  # ms

# Functions
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_playfield():
    for y in range(PLAYFIELD_HEIGHT):
        for x in range(PLAYFIELD_WIDTH):
            if playfield[y][x]:
                draw_block(x, y, playfield[y][x])

def draw_current_piece():
    if current_piece:
        for dx, dy in current_piece['shape']:
            draw_block(piece_x + dx, piece_y + dy, current_piece['color'])

def draw_ui():
    if game_over:
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (PLAYFIELD_WIDTH * BLOCK_SIZE + 10, 10))
    else:
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (PLAYFIELD_WIDTH * BLOCK_SIZE + 10, 10))
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (PLAYFIELD_WIDTH * BLOCK_SIZE + 10, 40))
        lines_text = font.render(f"Lines: {lines_cleared}", True, WHITE)
        screen.blit(lines_text, (PLAYFIELD_WIDTH * BLOCK_SIZE + 10, 70))

def spawn_piece():
    global current_piece, piece_x, piece_y, game_over
    current_piece = get_random_piece()
    # Find possible x positions
    possible_x = []
    for x in range(PLAYFIELD_WIDTH):
        if not check_collision(current_piece['shape'], x, 0):
            possible_x.append(x)
    if possible_x:
        piece_x = random.choice(possible_x)
        piece_y = 0
    else:
        game_over = True

def check_collision(shape, x, y):
    for dx, dy in shape:
        nx = x + dx
        ny = y + dy
        if nx < 0 or nx >= PLAYFIELD_WIDTH or ny >= PLAYFIELD_HEIGHT or (ny >= 0 and playfield[ny][nx]):
            return True
    return False

def place_piece():
    global score, lines_cleared, level, fall_speed
    for dx, dy in current_piece['shape']:
        x = piece_x + dx
        y = piece_y + dy
        if y >= 0:
            playfield[y][x] = current_piece['color']
    # Clear lines
    lines_to_clear = []
    for y in range(PLAYFIELD_HEIGHT):
        if all(playfield[y]):
            lines_to_clear.append(y)
    lines = len(lines_to_clear)
    for y in reversed(lines_to_clear):
        del playfield[y]
        playfield.insert(0, [0] * PLAYFIELD_WIDTH)
    # Scoring: standard Tetris points
    if lines == 1:
        points = 40
    elif lines == 2:
        points = 100
    elif lines == 3:
        points = 300
    elif lines == 4:
        points = 1200
    else:
        points = lines * 300  # For more lines, though unlikely
    score += points * level
    lines_cleared += lines
    if lines_cleared >= level * 10:
        level += 1
        fall_speed = max(50, fall_speed - 50)
    spawn_piece()

def try_rotate():
    global piece_x, piece_y
    rotated = rotate_shape(current_piece['shape'])
    # Try original position
    if not check_collision(rotated, piece_x, piece_y):
        current_piece['shape'] = rotated
        return
    # Try left
    if not check_collision(rotated, piece_x - 1, piece_y):
        current_piece['shape'] = rotated
        piece_x -= 1
        return
    # Try right
    if not check_collision(rotated, piece_x + 1, piece_y):
        current_piece['shape'] = rotated
        piece_x += 1
        return
    # Try up
    if not check_collision(rotated, piece_x, piece_y - 1):
        current_piece['shape'] = rotated
        piece_y -= 1
        return
    # If none, don't rotate

# Main loop
running = True
last_time = pygame.time.get_ticks()

# Initial spawn
spawn_piece()

while running:
    current_time = pygame.time.get_ticks()
    fall_time += current_time - last_time
    last_time = current_time

    if fall_time >= fall_speed and not game_over:
        fall_time = 0
        if check_collision(current_piece['shape'], piece_x, piece_y + 1):
            place_piece()
        else:
            piece_y += 1

    screen.fill(BLACK)
    draw_playfield()
    draw_current_piece()
    draw_ui()
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not check_collision(current_piece['shape'], piece_x - 1, piece_y):
                    piece_x -= 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not check_collision(current_piece['shape'], piece_x + 1, piece_y):
                    piece_x += 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not check_collision(current_piece['shape'], piece_x, piece_y + 1):
                    piece_y += 1
                    score += 1  # Soft drop point
                else:
                    place_piece()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:  # Rotate
                try_rotate()

pygame.quit()