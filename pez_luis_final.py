import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pez de Luis - NIVEL 3 - TU LO CONTROLAS")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Pez - ahora TU lo controlas
x, y = 400, 300
speed = 5
wiggle = 0
score = 0

# Comida
food_x = random.randint(50, 750)
food_y = random.randint(50, 550)

# Enemigo tiburón
shark_x = 0
shark_y = 300

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # CONTROLES - ¡Esto es lo nuevo!
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed

    # Que no se salga de la pantalla
    x = max(20, min(WIDTH-80, x))
    y = max(20, min(HEIGHT-20, y))

    wiggle += 0.15

    # Tiburón te persigue lento
    shark_x += 1
    if shark_x > WIDTH:
        shark_x = -100
        shark_y = random.randint(50, 550)
    
    # Comer
    dist = math.hypot((x+40 - food_x), (y - food_y))
    if dist < 35:
        score += 1
        food_x = random.randint(50, 750)
        food_y = random.randint(50, 550)
        print(f"¡ÑAM! Puntos: {score}")

    # Choque con tiburón
    dist_shark = math.hypot((x - shark_x), (y - shark_y))
    if dist_shark < 50:
        print(f"¡TE COMIO EL TIBURON! Puntos finales: {score}")
        x, y = 400, 300
        score = max(0, score-1)
        shark_x = -100

    # DIBUJO
    screen.fill((15, 40, 90))

    # Comida
    pygame.draw.circle(screen, (255, 80, 80), (food_x, food_y), 12)
    pygame.draw.circle(screen, (255, 200, 200), (food_x, food_y), 5)

    # Tiburón (gris)
    pygame.draw.ellipse(screen, (100,100,110), (shark_x-30, shark_y-15, 60, 30))
    pygame.draw.polygon(screen, (80,80,90), [(shark_x-30, shark_y), (shark_x-45, shark_y-20), (shark_x-45, shark_y+20)])

    # Tu pez
    for i in range(7):
        offset = math.sin(wiggle + i*0.5) * 10
        color = (255, 255, 255) if i%2==0 else (200, 230, 255)
        pygame.draw.circle(screen, color, (int(x + i*18), int(y + offset)), 9)
    
    head_x = int(x + 7*18)
    head_y = int(y + math.sin(wiggle + 7*0.5)*10)
    pygame.draw.circle(screen, (255,255,255), (head_x, head_y), 16)
    pygame.draw.circle(screen, (0,0,0), (head_x+5, head_y), 4)

    # Cola
    tail_x = int(x)
    tail_y = int(y)
    pygame.draw.polygon(screen, (180,220,255), [(tail_x, tail_y), (tail_x-22, tail_y-15), (tail_x-22, tail_y+15)])

    # Texto
    txt = font.render(f"Puntos: {score}  |  Flechas para moverte  |  ¡Cuidado con el tiburón!", True, (255,255,255))
    screen.blit(txt, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
