"""Simple Snake game implemented with pygame.

Run with `python run.py`.
"""
import random
import sys

import pygame

# Configuration
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
MOVE_EVENT = pygame.USEREVENT + 1
MOVE_INTERVAL = 150  # milliseconds between moves


def place_food(snake):
    """Return a random cell not occupied by the snake."""
    while True:
        pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if pos not in snake:
            return pos


def draw_rect(screen, color, pos):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PySnake")
    clock = pygame.time.Clock()
    pygame.time.set_timer(MOVE_EVENT, MOVE_INTERVAL)

    font = pygame.font.SysFont(None, 24)

    def reset():
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        return [start], (1, 0), place_food([start]), 0, False

    snake, direction, food, score, game_over = reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    snake, direction, food, score, game_over = reset()
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()

            if event.type == MOVE_EVENT and not game_over:
                head = snake[0]
                dx, dy = direction
                new = (head[0] + dx, head[1] + dy)

                # Check wall collision
                if not (0 <= new[0] < GRID_WIDTH and 0 <= new[1] < GRID_HEIGHT):
                    game_over = True
                # Check self collision
                elif new in snake:
                    game_over = True
                else:
                    snake.insert(0, new)
                    if new == food:
                        score += 1
                        food = place_food(snake)
                    else:
                        snake.pop()

        # Draw
        screen.fill((0, 0, 0))

        # Draw food
        draw_rect(screen, (220, 50, 50), food)

        # Draw snake
        for i, segment in enumerate(snake):
            color = (50, 200, 50) if i == 0 else (20, 150, 20)
            draw_rect(screen, color, segment)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (5, 5))

        if game_over:
            over_surf = font.render("Game Over - R to restart, Q to quit", True, (255, 200, 0))
            rect = over_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(over_surf, rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
