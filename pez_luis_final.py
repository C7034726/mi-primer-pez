import pygame, math, random

pygame.init()
W, H = 1000, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pez de Luis - Ya eres programador")
clock = pygame.time.Clock()

N = 22
elems = [{"x": W//2, "y": 0} for _ in range(N)]
pointer = {"x": W//2, "y": H//2}
frm = random.random()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            pointer["x"], pointer["y"] = event.pos

    frm += 0.08
    elems[0]["x"] = pointer["x"]
    elems[0]["y"] = pointer["y"]

    for i in range(1, N):
        prev = elems[i-1]
        cur = elems[i]
        dx = prev["x"] - cur["x"]
        dy = prev["y"] - cur["y"]
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        cur["x"] += math.cos(angle) * (dist - 18) * 0.3
        cur["y"] += math.sin(angle) * (dist - 18) * 0.3

    screen.fill((232, 221, 209))

    for i in range(1, N):
        cur = elems[i]
        prev = elems[i-1]
        angle = math.atan2(prev["y"]-cur["y"], prev["x"]-cur["x"])
        if i == 1:
            pygame.draw.polygon(screen, (17,17,17), [
                (cur["x"] + 20*math.cos(angle), cur["y"] + 20*math.sin(angle)),
                (cur["x"] + 10*math.cos(angle+2), cur["y"] + 10*math.sin(angle+2)),
                (cur["x"] + 10*math.cos(angle-2), cur["y"] + 10*math.sin(angle-2)),
            ])
        elif i in (8, 14):
            for j in range(5):
                fx = cur["x"] + math.cos(angle + math.radians(j*15-30)) * (30+j*5)
                fy = cur["y"] + math.sin(angle + math.radians(j*15-30)) * (30+j*5)
                pygame.draw.line(screen, (34,34,34), (cur["x"], cur["y"]), (fx, fy), 2)
        else:
            pygame.draw.circle(screen, (34,34,34), (int(cur["x"]), int(cur["y"])), int(max(2, 10 - i*0.3)))
        pygame.draw.line(screen, (50,50,50), (cur["x"], cur["y"]), (prev["x"], prev["y"]), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
