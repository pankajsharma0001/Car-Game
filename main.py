import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Car Game - Pankaj Sharma")

dis_width = 800
dis_height = 600

display = pygame.display.set_mode((dis_width, dis_height))

background = pygame.image.load('resources\\path.jpg')
background = pygame.transform.scale(background, (dis_width, dis_height))
player = pygame.image.load('resources\\player.png')

# Adjusted car size
player_width = 210
player_height = 125

enemy_width = 165
enemy_height = 125
player = pygame.transform.scale(player, (player_width, player_height))

enemy = pygame.image.load('resources\\enemy.png')
enemy = pygame.transform.scale(enemy, (enemy_width, enemy_height))

# Adjusted starting speed and increments
enemy_car_speed = 10
point = 0

clock = pygame.time.Clock()

def show_pause_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("PAUSED", True, 'black')
    text_rect = text.get_rect(center=(dis_width/2, dis_height/2))
    display.blit(text, text_rect)
    pygame.display.update()

def message(x_mess, y_mess, size, mess, color='red'):
    text = pygame.font.SysFont(None, size)
    blend = text.render(mess, True, color)
    display.blit(blend, (x_mess, y_mess))

def score(point):
    text = pygame.font.SysFont(None, 25)
    blend = text.render(f'Score: {point}', True, 'red')
    display.blit(blend, (0, 0))

def button(x_but, y_but, color, text):
    pygame.draw.rect(display, color, [x_but, y_but, 110, 30])
    message(x_but + 10, y_but, 30, text, 'white')  # Adjust text position to center
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x_but < mouse[0] < x_but + 110 and y_but < mouse[1] < y_but + 30:
        pygame.draw.rect(display, "red", [x_but, y_but, 110, 30])
        message(x_but + 10, y_but, 30, text, 'white')
        if click[0] == 1 and text == 'START':
            start_game(enemy_car_speed, point)
        if click[0] == 1 and text == 'QUIT':
            pygame.quit()
            quit()

def over(scr):
    tex = f'Your Score is {scr}'
    display.fill('grey')
    message(dis_width/4, dis_height/3, 50, tex)
    pygame.display.update()
    time.sleep(2)
    intro()

def intro():
    game_over = False
    while not game_over:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(background, [0, 0, dis_width, dis_height])
        button(150, 400, 'green', 'START')
        button(600, 400, 'green', 'QUIT')
        pygame.display.update()

def start_game(enemy_car_speed, point):
    x = dis_width / 2 - player_width / 2  # Center player car
    y = dis_height - player_height - 10  # Set player's car at the bottom
    x_change = 0
    x_enemy = random.randint(100, dis_width - enemy_width)
    y_enemy = -enemy_height  # Start enemy car off the screen

    game_over = False
    paused = False
    while not game_over:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_over = True
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_LEFT or events.key == pygame.K_a:
                    x_change = -7  # Reduce movement speed for smoother control
                elif events.key == pygame.K_RIGHT or events.key == pygame.K_d:
                    x_change = 7
                if events.key == pygame.K_SPACE:
                    paused = not paused

            if events.type == pygame.KEYUP:
                if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT or events.key == pygame.K_a or events.key == pygame.K_d:
                    x_change = 0  # Stop movement when key is released

        if paused:
            show_pause_screen()
            continue

        x += x_change

        # Boundary check
        if x < 0:
            x = 0
        elif x > dis_width - player_width:
            x = dis_width - player_width

        y_enemy += enemy_car_speed

        # Redraw elements
        display.blit(background, [0, 0, dis_width, dis_height])
        display.blit(enemy, [x_enemy, y_enemy])
        display.blit(player, [x, y])
        score(point)

        # Reset enemy car if it goes off-screen
        if y_enemy > dis_height:
            y_enemy = -enemy_height
            x_enemy = random.randint(100, dis_width - enemy_width)
            point += 1
            # Increase speed by a small increment
            if point % 5 == 0:
                enemy_car_speed += 1  # Increase speed slightly after every 5 points

        # Collision detection (improved)
        if y_enemy + player_height > y and y_enemy < y + player_height:  # Check y-overlap
            if x_enemy < x < x_enemy + 35 or x_enemy < x + 50 < x_enemy + 50:  # Check x-overlap
                over(point)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

intro()
