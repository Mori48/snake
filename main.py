import pygame
from sys import exit
import random

pygame.init()

fps = 5
screen = pygame.display.set_mode((900, 1000))

pygame.display.set_caption('Smart snake')
clock = pygame.time.Clock()
font = pygame.font.Font("font/slkscr.ttf", 30)

# Размер поля
FIELD_X = 0
FIELD_Y = 100
FIELD_WIDTH = 900
FIELD_HEIGHT = 900

CELL_SIZE = 50  # Размер клетки
GRID_WIDTH = FIELD_WIDTH // CELL_SIZE  # Количество клеток по X
GRID_HEIGHT = FIELD_HEIGHT // CELL_SIZE  # Количество клеток по Y (минус отступ сверху)

score = 0

snake_surf = pygame.Surface((CELL_SIZE // 1.5, CELL_SIZE // 1.5))
snake_surf.fill('cornflowerblue')

# Задаем начальную точку
snake_x_pos = GRID_WIDTH // 2 * CELL_SIZE + CELL_SIZE / 2
snake_y_pos = GRID_HEIGHT // 2 * CELL_SIZE + FIELD_Y + CELL_SIZE / 2

snake_speed = CELL_SIZE
snake_move_x = 0
snake_move_y = -snake_speed  # Начальное движение вверх

# Список хранящий тело змеи (голова на одну клетку выше тела)
snake_body = [
    (snake_x_pos, snake_y_pos),  # Голова
    (snake_x_pos, snake_y_pos + CELL_SIZE),  # Второй сегмент
    (snake_x_pos, snake_y_pos + 2 * CELL_SIZE)  # Третий сегмент
]

apple_x_pos = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE + CELL_SIZE / 2
apple_y_pos = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE + FIELD_Y + CELL_SIZE / 2

apple_surf = pygame.Surface((CELL_SIZE // 2, CELL_SIZE // 2))
apple_surf.fill('Red')
apple_rect = apple_surf.get_rect(center=(apple_x_pos, apple_y_pos))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake_move_y = -snake_speed
                snake_move_x = 0
            if event.key == pygame.K_s:
                snake_move_y = snake_speed
                snake_move_x = 0
            if event.key == pygame.K_d:
                snake_move_y = 0
                snake_move_x = snake_speed
            if event.key == pygame.K_a:
                snake_move_y = 0
                snake_move_x = -snake_speed

    screen.fill('Black')
    # Отрисовка цветного поля
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = 'chartreuse4' if (row + col) % 2 == 0 else 'chartreuse3'
            pygame.draw.rect(screen, color, (col * CELL_SIZE, FIELD_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, 'white', (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), 5)

    snake_y_pos += snake_move_y
    snake_x_pos += snake_move_x

    snake_body.insert(0, (snake_x_pos, snake_y_pos))

    snake_rect_head = snake_surf.get_rect(center=(snake_x_pos, snake_y_pos))

    if snake_rect_head.colliderect(apple_rect):
        score += 1
        if score % 2 == 0:
            fps += 0.2
        print(score)
        apple_x_pos = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE + CELL_SIZE / 2
        apple_y_pos = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE + FIELD_Y + CELL_SIZE / 2
        apple_rect = apple_surf.get_rect(center=(apple_x_pos, apple_y_pos))
    else:
        snake_body.pop()

    if (
        snake_rect_head.left < FIELD_X or
        snake_rect_head.right > FIELD_X + FIELD_WIDTH or
        snake_rect_head.top < FIELD_Y or
        snake_rect_head.bottom > FIELD_Y + FIELD_HEIGHT
    ):
        pygame.quit()
        exit()

    # Проверка столкновений с телом (исключая голову)
    for segment in snake_body[1:]:
        if snake_rect_head.colliderect(pygame.Rect(segment[0] - CELL_SIZE // 2, segment[1] - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE)):
            pygame.quit()
            exit()

    text_surf = font.render('Score: ' + str(score), False, 'White')
    screen.blit(apple_surf, apple_rect)

    for segment in snake_body:
        screen.blit(snake_surf, snake_surf.get_rect(center=segment))

    screen.blit(text_surf, (FIELD_WIDTH - 200, 60))

    pygame.display.update()
    clock.tick(fps)