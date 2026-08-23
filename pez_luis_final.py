import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pez de Luis - NIVEL 4 - JUEGO FINAL")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont(None, 60, bold=True)
font = pygame.font.SysFont(None, 36)

# --- SONIDO ÑAM simple ---
pygame.mixer.init()
def sonido_nam():
    # beep casero
    try:
        pygame.mixer.Sound(pygame.mixer.Sound.buffer_size)
    except:
        pass
    print("\a") # beep del sistema

# Variables
x, y = 400, 300
speed = 5
wiggle = 0
score = 0
size = 9  # tamaño inicial del pez
vidas = 3
game_over = False

food_x = random.randint(50, 750)
food_y = random.randint(50, 550)
shark_x = -100
shark_y = 300
shark_speed = 2.5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # REINICIAR
                x, y = 400, 300
                score = 0
                size = 9
                vidas = 3
                game_over = False
                shark_x = -100

    if not game_over:
        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: y -= speed
        if keys[pygame.K_DOWN]: y += speed
        if keys[pygame.K_LEFT]: x -= speed
        if keys[pygame.K_RIGHT]: x += speed

        x = max(20, min(WIDTH-80, x))
        y = max(20, min(HEIGHT-20, y))
        wiggle += 0.15

        # Tiburon te sigue
        if shark_x < x:
            shark_x += shark_speed
        else:
            shark_x -= shark_speed * 0.5
        if shark_y < y:
            shark_y += shark_speed * 0.3
        else:
            shark_y -= shark_speed * 0.3

        # Comer
        dist = math.hypot((x+40 - food_x), (y - food_y))
        if dist < 35 + size:
            score += 1
            size += 0.8  # ¡CRECE!
            shark_speed += 0.15  # se pone más difícil
            food_x = random.randint(50, 750)
            food_y = random.randint(50, 550)
            sonido_nam()
            print(f"¡ÑAM! Puntos: {score} - Tamaño: {size:.1f}")

        # Choque tiburon
        dist_shark = math.hypot((x - shark_x), (y - shark_y))
        if dist_shark < 45 + size:
            vidas -= 1
            x, y = 400, 300
            shark_x = -200
            shark_y = random.randint(50, 550)
            print(f"¡OUCH! Te quedan {vidas} vidas")
            if vidas <= 0:
                game_over = True

    # DIBUJO
    screen.fill((10, 30, 70))

    if not game_over:
        # Comida
        pygame.draw.circle(screen, (255, 80, 80), (food_x, food_y), 12)
        pygame.draw.circle(screen, (255, 220, 220), (food_x, food_y), 5)

        # Tiburon
        pygame.draw.ellipse(screen, (100,100,110), (int(shark_x-35), int(shark_y-18), 70, 36))
        pygame.draw.polygon(screen, (80,80,90), [(shark_x-35, shark_y), (shark_x-55, shark_y-22), (shark_x-55, shark_y+22)])
        pygame.draw.polygon(screen, (90,90,100), [(shark_x+5, shark_y-18), (shark_x+15, shark_y-30), (shark_x+10, shark_y-18)])

        # Tu pez - AHORA CRECE con size
        for i in range(7):
            offset = math.sin(wiggle + i*0.5) * 10
            pygame.draw.circle(screen, (255,255,255), (int(x + i*18), int(y + offset)), int(size))

        head_x = int(x + 7*18)
        head_y = int(y + math.sin(wiggle + 7*0.5)*10)
        pygame.draw.circle(screen, (255,255,255), (head_x, head_y), int(size+7))
        pygame.draw.circle(screen, (0,0,0), (head_x+5, head_y), 4)

        # Cola
        pygame.draw.polygon(screen, (180,220,255), [(int(x), int(y)), (int(x-22), int(y-15)), (int(x-22), int(y+15))])

        # HUD
        txt = font.render(f"Puntos: {score} | Tamaño: {int(size)} | Vidas: {vidas} | Flechas para moverte", True, (255,255,255))
        screen.blit(txt, (10, 10))
    else:
        # PANTALLA GAME OVER
        screen.fill((20, 10, 40))
        t1 = font_big.render("GAME OVER", True, (255, 80, 80))
        t2 = font_big.render(f"PUNTOS: {score}", True, (255,255,255))
        t3 = font.render(f"¡Increíble, LUIS! Hiciste crecer tu pez a tamaño {int(size)}", True, (180, 220, 255))
        t4 = font.render("Presiona R para jugar de nuevo - Presiona X para cerrar", True, (255,255,255))
        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 150))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 230))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 310))
        screen.blit(t4, (WIDTH//2 - t4.get_width()//2, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
