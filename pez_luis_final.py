import pygame, math, random
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pez de Luis - NIVEL 6 - DIOS DEL OCEANO")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big = pygame.font.SysFont(None, 70, bold=True)

# Jugador
x, y = 400, 300
speed_base = 5
speed = speed_base
score = 0
size = 12
freeze_cooldown = 0

# Enemigo IA
ex, ey = 100, 100
espeed = 2.2
enemy_frozen = 0
enemy_size = 14

# Comida y poderes
food_x, food_y = random.randint(50,850), random.randint(50,550)
power_x, power_y = random.randint(50,850), random.randint(50,550)
power_type = random.choice(['speed','grow','freeze'])
power_timer = 0

wiggle = 0
winner = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and freeze_cooldown <= 0:
            enemy_frozen = 180 # 3 seg a 60fps
            freeze_cooldown = 300 # 5 seg cooldown
            print("¡CONGELADO!")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: y -= speed
    if keys[pygame.K_DOWN]: y += speed
    if keys[pygame.K_LEFT]: x -= speed
    if keys[pygame.K_RIGHT]: x += speed

    x = max(0, min(WIDTH-60, x))
    y = max(0, min(HEIGHT-20, y))
    wiggle += 0.15
    if freeze_cooldown > 0: freeze_cooldown -= 1
    if power_timer > 0: power_timer -= 1
    else: speed = speed_base

    # Enemigo IA persigue
    if enemy_frozen > 0:
        enemy_frozen -= 1
    else:
        if ex < x: ex += espeed
        else: ex -= espeed
        if ey < y: ey += espeed
        else: ey -= espeed

    # Comer comida
    if math.hypot(x+20-food_x, y-food_y) < 25+size:
        score += 1
        size += 0.6
        food_x, food_y = random.randint(50,850), random.randint(50,550)
        espeed += 0.08

    # Poder
    if math.hypot(x+20-power_x, y-power_y) < 30:
        if power_type == 'speed':
            speed = 9
            power_timer = 180
        elif power_type == 'grow':
            size += 8
        elif power_type == 'freeze':
            enemy_frozen = 240
        power_x, power_y = random.randint(50,850), random.randint(50,550)
        power_type = random.choice(['speed','grow','freeze'])

    # Te atrapa enemigo
    if math.hypot(x-ex, y-ey) < 35+size and enemy_frozen==0:
        score = max(0, score-2)
        size = max(10, size-2)
        x, y = 400, 300
        print("¡TE ATRAPO!")

    if score >= 20:
        winner = True

    # DIBUJO
    screen.fill((5, 20, 60))
    
    # Comida roja
    pygame.draw.circle(screen, (255,60,60), (food_x, food_y), 13)
    # Poder
    color = (60,180,255) if power_type=='speed' else (255,230,60) if power_type=='grow' else (150,220,255)
    pygame.draw.circle(screen, color, (power_x, power_y), 16)
    pygame.draw.circle(screen, (255,255,255), (power_x, power_y), 6)

    # Enemigo
    if enemy_frozen>0:
        col = (100,200,255)
    else:
        col = (255,120,40)
    for i in range(4):
        off = math.sin(wiggle+i+2)*6
        pygame.draw.circle(screen, col, (int(ex+i*10), int(ey+off)), int(enemy_size))
    
    # Tu pez
    for i in range(6):
        off = math.sin(wiggle+i)*9
        pygame.draw.circle(screen, (255,255,255), (int(x+i*12), int(y+off)), int(size))

    hud = font.render(f"Puntos: {score}/20 | Tamaño: {int(size)} | ESPACIO: Congelar { 'LISTO' if freeze_cooldown<=0 else f'{freeze_cooldown//60}s' } | Poder: {power_type}", True, (255,255,255))
    screen.blit(hud, (10,10))

    if winner:
        screen.fill((0,0,0))
        t = big.render("¡ERES DIOS DEL OCEANO!", True, (255,255,0))
        t2 = font.render(f"Puntaje Final: {score} - Tamaño Dios: {int(size)}", True, (255,255,255))
        screen.blit(t, (WIDTH//2-t.get_width()//2, 250))
        screen.blit(t2, (WIDTH//2-t2.get_width()//2, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
