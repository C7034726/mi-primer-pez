import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pez de Luis - NIVEL 2 - ¡A COMER!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Pez
x = 100
y = 300
speed = 3
direction = 1
wiggle = 0
score = 0

# Comida
food_x = random.randint(100, 700)
food_y = random.randint(100, 500)
food_size = 15

# Boca abierta?
mouth_open = False
mouth_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouth_open = True
                mouth_timer = 10  # frames que dura abierta

    # Movimiento
    x += speed * direction
    y = 300 + math.sin(wiggle) * 80
    wiggle += 0.08
    
    if x > WIDTH - 80 or x < 20:
        direction *= -1

    # Comer
    dist = math.hypot((x+160 - food_x), (y - food_y))
    if dist < 40 and mouth_open:
        score += 1
        food_x = random.randint(100, 700)
        food_y = random.randint(100, 500)
        print(f"¡ÑAM! Puntos: {score}")

    if mouth_timer > 0:
        mouth_timer -= 1
    else:
        mouth_open = False

    # DIBUJO
    screen.fill((15, 30, 80))

    # Comida (camarón rojo)
    pygame.draw.circle(screen, (255, 80, 80), (food_x, food_y), food_size)

    # Pez esqueleto
    for i in range(8):
        offset = math.sin(wiggle + i*0.6) * 12
        pygame.draw.circle(screen, (255, 255, 255), (int(x + i*22), int(y + offset)), 9)
    
    # Cabeza
    head_x = int(x + 8*22)
    head_y = int(y + math.sin(wiggle + 8*0.6)*12)
    if mouth_open:
        # boca abierta grande
        pygame.draw.circle(screen, (255,255,255), (head_x, head_y), 22, 3)
        pygame.draw.circle(screen, (0,0,0), (head_x, head_y), 8)
    else:
        pygame.draw.circle(screen, (255,255,255), (head_x, head_y), 18)
        pygame.draw.circle(screen, (0,0,0), (head_x, head_y), 6)

    # Cola
    tail_x = int(x)
    tail_y = int(y + math.sin(wiggle)*12)
    pygame.draw.polygon(screen, (200,200,255), [(tail_x, tail_y), (tail_x-25, tail_y-18), (tail_x-25, tail_y+18)])

    # Marcador
    texto = font.render(f"Puntos: {score}  [ESPACIO para comer]", True, (255,255,255))
    screen.blit(texto, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
