import pygame, math, random
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pez de Luis - NIVEL 5 - MULTIJUGADOR")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big = pygame.font.SysFont(None, 70, bold=True)

# Jugador 1 - Luis (Blanco)
p1_x, p1_y, p1_score, p1_size = 200, 300, 0, 9
# Jugador 2 - Amigo (Naranja)
p2_x, p2_y, p2_score, p2_size = 600, 300, 0, 9

food_x = random.randint(100, 800)
food_y = random.randint(100, 500)
wiggle = 0
winner = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if winner and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            p1_score = p2_score = 0
            p1_size = p2_size = 9
            p1_x, p1_y = 200, 300
            p2_x, p2_y = 600, 300
            winner = None

    if not winner:
        keys = pygame.key.get_pressed()
        # P1 Flechas
        if keys[pygame.K_UP]: p1_y -= 5
        if keys[pygame.K_DOWN]: p1_y += 5
        if keys[pygame.K_LEFT]: p1_x -= 5
        if keys[pygame.K_RIGHT]: p1_x += 5
        # P2 WASD
        if keys[pygame.K_w]: p2_y -= 5
        if keys[pygame.K_s]: p2_y += 5
        if keys[pygame.K_a]: p2_x -= 5
        if keys[pygame.K_d]: p2_x += 5

        p1_x = max(0, min(WIDTH-60, p1_x))
        p1_y = max(0, min(HEIGHT-20, p1_y))
        p2_x = max(0, min(WIDTH-60, p2_x))
        p2_y = max(0, min(HEIGHT-20, p2_y))

        wiggle += 0.15

        # Comer P1
        if math.hypot(p1_x+30-food_x, p1_y-food_y) < 30+p1_size:
            p1_score+=1; p1_size+=1
            food_x = random.randint(100,800); food_y = random.randint(100,500)
        # Comer P2
        if math.hypot(p2_x+30-food_x, p2_y-food_y) < 30+p2_size:
            p2_score+=1; p2_size+=1
            food_x = random.randint(100,800); food_y = random.randint(100,500)

        if p1_score >= 10: winner = "LUIS (BLANCO)"
        if p2_score >= 10: winner = "AMIGO (NARANJA)"

    # DIBUJO
    screen.fill((10, 40, 90))
    pygame.draw.circle(screen, (255,80,80), (food_x, food_y), 14)

    # Pez 1 Blanco
    for i in range(5):
        off = math.sin(wiggle+i)*8
        pygame.draw.circle(screen, (255,255,255), (int(p1_x+i*12), int(p1_y+off)), int(p1_size))
    # Pez 2 Naranja
    for i in range(5):
        off = math.sin(wiggle+i+1)*8
        pygame.draw.circle(screen, (255,180,50), (int(p2_x+i*12), int(p2_y+off)), int(p2_size))

    # HUD
    t = font.render(f"LUIS [Flechas]: {p1_score} | AMIGO [WASD]: {p2_score} | Primero a 10 gana!", True, (255,255,255))
    screen.blit(t, (10,10))

    if winner:
        screen.fill((0,0,0))
        txt = big.render(f"¡GANA {winner}!", True, (255,255,0))
        txt2 = font.render("Presiona R para revancha", True, (255,255,255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
        screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
