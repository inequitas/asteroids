import pygame
from constants import *
from logger import log_state
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    log_state()
    screen.fill("black")
    player.update(dt)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    dt = clock.tick(60) / 1000
    

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    


if __name__ == "__main__":
    main()