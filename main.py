#import all the things
import pygame
import sys
from constants import *
from logger import log_state,log_event
from player import Player
from asteroid import Asteroid
from AsteroidField import AsteroidField
from shot import Shot

#initialize pygame
pygame.init()

#set the screen and clock parameters
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

#making the groups
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()


#assigning groups to classes
Player.containers = (updatable, drawable)
Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable)
Shot.containers = (updatable, drawable)

#create player instance
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
field = AsteroidField()

#start loop
done = False
while not done:
    
    #make sure I can quit out again
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #logging!
    log_state()
    
    #make screen go black
    screen.fill("black")
    
    #updating everything in updatable
    updatable.update(dt)

    for asteroid in asteroids:
        if player.collides_with(asteroid):
            log_event("player_hit")
            print("Game over!")
            sys.exit()
        

    # drawing everything in drawable
    for item in drawable:
        item.draw(screen)
    
    #update the screen
    pygame.display.flip()
    
    #set FPS
    clock.tick(60)
    
    #change FPS to frames per miliseconds
    dt = clock.tick(60) / 1000
    
#start main
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    


if __name__ == "__main__":
    main()