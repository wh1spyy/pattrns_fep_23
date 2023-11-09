import pygame
import random

# Pygame Initialization
pygame.init()

# Set Screen Dimensions
screen_width = 1200
screen_height = 700

# Define Colors
purple = (128, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Load and Resize Images
snake_head_img = pygame.image.load("alegabara.png")
snake_head_img = pygame.transform.scale(snake_head_img, (40, 40))
food_img = pygame.image.load("pivo.png")
food_img = pygame.transform.scale(food_img, (30, 30))
poison_img = pygame.image.load("capusta.png")
poison_img = pygame.transform.scale(poison_img, (20, 20))
background_img = pygame.image.load("fight.jpg")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
game_over_background_img = pygame.image.load("kalaska.png")
game_over_background_img = pygame.transform.scale(game_over_background_img, (screen_width, screen_height))

# Create Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set Font Style
font_style = pygame.font.SysFont(None, 50)

# Set Snake Speed and Target FPS
snake_block = 5
snake_speed = 1
target_fps = 40

# Collision Detection Function
def is_collision(x1, y1, x2, y2, width, height, item_type):
    if item_type == "food":
        return pygame.Rect(x1, y1, snake_block, snake_block).colliderect(pygame.Rect(x2, y2, width, height))
    elif item_type == "poison":
        return pygame.Rect(x1, y1, snake_block, snake_block).colliderect(pygame.Rect(x2, y2, width, height))

# Draw Snake Function
def snake(snake_block, snake_list):
    for x in snake_list:
        screen.blit(snake_head_img, (x[0], x[1]))

# Main Game Loop
def gameLoop():
    game_over = False
    game_close = False
    game_over_background = False  # Додайте цю змінну

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

    poison_list = []
    for _ in range(8):
        poisonx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
        poisony = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
        poison_list.append([poisonx, poisony])

    score = 0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close == True:
            if game_over_background:
                screen.blit(game_over_background_img, (0, 0))
            else:
                screen.blit(background_img, (0, 0))
            
            message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
            screen.blit(message, [screen_width / 12, screen_height / 3])

            score_message = font_style.render("Score: " + str(score), True, black)
            screen.blit(score_message, [screen_width / 10, screen_height / 2])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        head = []
        head.append(x1)
        head.append(y1)
        snake_List.append(head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == head:
                game_close = True

        screen.blit(background_img, (0, 0))
        screen.blit(food_img, (foodx, foody))

        for poison in poison_list:
            screen.blit(poison_img, (poison[0], poison[1]))

        snake(snake_block, snake_List)

        score_message = font_style.render("Score: " + str(score), True, black)
        screen.blit(score_message, [0, 0])

        fps = int(clock.get_fps())

        fps_message = font_style.render("FPS: " + str(fps), True, black)
        screen.blit(fps_message, [0, 50])

        pygame.display.update()

        if is_collision(x1, y1, foodx, foody, 40, 40, "food"):
            foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            score += 10

        for i in range(len(poison_list)):
            poisonx = poison_list[i][0]
            poisony = poison_list[i][1]

            direction = random.choice(['left', 'right', 'up', 'down'])

            if direction == 'left':
                poisonx -= snake_block
            elif direction == 'right':
                poisonx += snake_block
            elif direction == 'up':
                poisony -= snake_block
            elif direction == 'down':
                poisony += snake_block

            poisonx = max(0, min(poisonx, screen_width - snake_block))
            poisony = max(0, min(poisony, screen_height - snake_block))

            poison_list[i] = [poisonx, poisony]

        for poison in poison_list:
            if is_collision(x1, y1, poison[0], poison[1], 25, 25, "poison"):
                game_close = True

        clock.tick(target_fps)

    pygame.quit()
    quit()

game_over_background = False
gameLoop()
