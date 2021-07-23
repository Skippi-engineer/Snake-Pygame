#
# SIMPLE SNAKE GAME USING PYGAME
#
# Controls - arrow keys
# Requirements: pygame
#

import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# Screen and game size:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_WIDTH = 600
GAME_HEIGHT = 400
GAME_CHANGE = 100

# Colors:
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (154, 197, 2)
BLUE = (46, 90, 195)
LIGHT_BLUE = (56, 120, 195)

# Snake size and speed:
SNAKE_BLOCK = 15
SNAKE_SPEED = 12

# Font and description:
pygame.display.set_caption('Simple Snake Game')
FONT_ARIAL = pygame.font.SysFont("arial", SCREEN_WIDTH // 25)
FONT_COMICSANSMS = pygame.font.SysFont("comicsansms", SCREEN_WIDTH // 23)

# Initialization:
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_WIDTH = (GAME_WIDTH // SNAKE_BLOCK) * SNAKE_BLOCK
GAME_HEIGHT = (GAME_HEIGHT // SNAKE_BLOCK) * SNAKE_BLOCK
GAME_CHANGE = (GAME_CHANGE // SNAKE_BLOCK) * SNAKE_BLOCK
END_Y = GAME_HEIGHT
END_X = GAME_WIDTH + SNAKE_BLOCK
GAME_WIDTH += GAME_CHANGE
GAME_HEIGHT += GAME_CHANGE


# Functions:
def draw_snake(snake_block, snake_list):
    if len(snake_list) % 2:
        even = True
    else:
        even = False

    for x in snake_list:
        if even:
            pygame.draw.rect(display, BLUE, [x[0], x[1], snake_block, snake_block])
            even = False
        else:
            pygame.draw.rect(display, LIGHT_BLUE, [x[0], x[1], snake_block, snake_block])
            even = True
    # pygame.draw.rect(display, BLUE, [snake_list[-1][0], snake_list[-1][1], snake_block, snake_block])


def message(msg, color, font, xy):
    msg = font.render(msg, True, color)
    display.blit(msg, xy)


def your_score(score):
    message("Your Score: " + str(score - 1), BLACK, FONT_COMICSANSMS, [10, 0])


def your_best(best, score):
    if best < score:
        message("Your best Score: " + str(score - 1), BLACK, FONT_COMICSANSMS, [10, 35])
        return score
    else:
        message("Your best Score: " + str(best - 1), BLACK, FONT_COMICSANSMS, [10, 35])
        return best


def game_draw():
    # pygame.draw.rect(display, RED, [start_x, start_y, end_x, end_y])
    # Width up:
    pygame.draw.rect(display, BLACK, [GAME_CHANGE - SNAKE_BLOCK, GAME_CHANGE - SNAKE_BLOCK, END_X, SNAKE_BLOCK])
    # Width down:
    pygame.draw.rect(display, BLACK, [GAME_CHANGE - SNAKE_BLOCK, GAME_HEIGHT, END_X + SNAKE_BLOCK, SNAKE_BLOCK])
    # Height LEFT:
    pygame.draw.rect(display, BLACK, [GAME_CHANGE - SNAKE_BLOCK, GAME_CHANGE, SNAKE_BLOCK, END_Y])
    # Height RIGHT:
    pygame.draw.rect(display, BLACK, [GAME_WIDTH, GAME_CHANGE - SNAKE_BLOCK, SNAKE_BLOCK, END_Y + SNAKE_BLOCK])


def game_over(best_score, length_of_snake):
    over = False
    while not over:
        display.fill(GREEN)
        message("You Lost! Press C-Play Again or Q-Quit", BLACK, FONT_ARIAL, [SCREEN_WIDTH / 8, SCREEN_HEIGHT / 3])
        your_score(length_of_snake)
        your_best(best_score, length_of_snake)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    over = True

                if event.key == pygame.K_c:
                    game_loop(best_score)


def game_loop(best_score):
    game_continue = True

    # The place where the snake start:
    snake_x = (GAME_WIDTH // 2 + GAME_CHANGE) // SNAKE_BLOCK * SNAKE_BLOCK
    snake_y = (GAME_HEIGHT // 2 + GAME_CHANGE) // SNAKE_BLOCK * SNAKE_BLOCK

    # Direction of movement:
    move_x = 0
    move_y = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(GAME_CHANGE, GAME_WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
    food_y = round(random.randrange(GAME_CHANGE, GAME_HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK

    while game_continue:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_continue = False

            # Consequences of pressing key:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and move_x != SNAKE_BLOCK:
                    move_x = -SNAKE_BLOCK
                    move_y = 0
                elif event.key == pygame.K_RIGHT and move_x != -SNAKE_BLOCK:
                    move_x = SNAKE_BLOCK
                    move_y = 0
                elif event.key == pygame.K_UP and move_y != SNAKE_BLOCK:
                    move_x = 0
                    move_y = -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and move_y != -SNAKE_BLOCK:
                    move_x = 0
                    move_y = SNAKE_BLOCK

        if snake_x >= GAME_WIDTH or snake_x < GAME_CHANGE or snake_y >= GAME_HEIGHT or snake_y < GAME_CHANGE:
            game_over(length_of_snake, best_score)
            game_continue = False

        snake_x += move_x
        snake_y += move_y
        display.fill(GREEN)
        game_draw()
        pygame.draw.rect(display, RED, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for i in snake_list[:-1]:
            if i == snake_head:
                game_over(length_of_snake, best_score)
                game_continue = False

        draw_snake(SNAKE_BLOCK, snake_list)
        your_score(length_of_snake)
        best_score = your_best(best_score, length_of_snake)

        pygame.display.update()

        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(GAME_CHANGE, GAME_WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            food_y = round(random.randrange(GAME_CHANGE, GAME_HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


# Main:
game_loop(0)
