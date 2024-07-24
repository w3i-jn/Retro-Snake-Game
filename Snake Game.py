import pygame
import sys
import time
import random
from pygame import mixer

# Difficulty settings
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Initialize Pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Eater')
text_font = pygame.font.SysFont("Helvetica", 30)

# Function to draw text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Main starting screen loop
def show_start_screen():
    run = True
    while run:
        screen.fill((0, 0, 0))
        draw_text("Snake Game", text_font, (255, 255, 255), 270, 100)
        draw_text("Control:", text_font, (255, 255, 255), 270, 200)
        draw_text("Use Arrow Key To Move", text_font, (255, 255, 255), 270, 250)
        draw_text("Press any key to start", text_font, (255, 255, 255), 270, 400)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Background music
def load_sounds():
    mixer.music.load("bgm.mp3")
    global consume_sound, game_over_sound
    consume_sound = mixer.Sound("consume_sound.mp3")
    game_over_sound = mixer.Sound("game_over.mp3")
    mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Game Over function with restart and quit options
def game_over():
    mixer.music.stop()
    game_over_sound.play()
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    draw_text("Press R to Restart or Q to Quit", text_font, white, 180, frame_size_y / 1.5)
    pygame.display.flip()
    
    # Waiting for user to press R or Q
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Score display function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Main game function
def main_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    mixer.music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
            consume_sound.play()
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over()
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)

# Main
if __name__ == "__main__":
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    fps_controller = pygame.time.Clock()
    
    show_start_screen()
    load_sounds()
    main_game()
