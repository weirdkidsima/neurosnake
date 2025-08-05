import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 600  # Размер окна
GRID_SIZE = 20            # Размер клетки
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10                  # Скорость обновления кадров

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Направления (векторы движения)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Начальная позиция
        self.direction = RIGHT                                  # Начальное направление
        self.length = 1                                        # Начальная длина
        self.score = 0                                          # Счёт

    def get_head_position(self):
        return self.positions[0]  # Голова змейки

    def move(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        # Новая позиция головы: текущая + направление (векторное сложение)
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        new_position = (new_x, new_y)

        if new_position in self.positions[1:]:
            return False  # Конец игры

        self.positions.insert(0, new_position)  # Добавляем новую голову
        if len(self.positions) > self.length:
            self.positions.pop()  # Удаляем хвост, если не съели еду
        return True  # Игра продолжается

    def grow(self):
        self.length += 1
        self.score += 1

    def change_direction(self, new_dir):
        # Запрещаем резкие развороты
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            color = GREEN if i == 0 else (0, 200, 0)  # Голова ярче
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    food = Food()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if not snake.move():
            print(f"Игра окончена! Счёт: {snake.score}")
            time.sleep(2)
            running = False

        # Проверка, съела ли змейка еду
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # Проверяем, чтобы еда не появилась внутри змейки
            while food.position in snake.positions:
                food.randomize_position()

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()