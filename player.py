#import all the things
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

#make the player
class Player(CircleShape):
    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots_group = shots_group
        self.shoot_cooldown = 0
    
    #drawing triangle is hard    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    #redefine the draw parameter
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    #making sure I can rotate
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    #all the keypresses for the player
    def update(self, dt):
        keys = pygame.key.get_pressed()
        #press A
        if keys[pygame.K_a]:
            self.rotate(-dt)
        #Press D
        if keys[pygame.K_d]:
            self.rotate(dt)
        #Press W
        if keys[pygame.K_w]:
            self.move(dt)
        #Press S
        if keys[pygame.K_s]:
            self.move(-dt)
        #press SPACEBAR
        if keys[pygame.K_SPACE]:
            self.shoot()
        #decrease shot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    #actually moving
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    #making sure I can rotate
    def shoot(self):
        #check if on cooldown, if so then no shooty
        if self.shoot_cooldown > 0:
            return
        #shooty
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shots_group.add(shot)
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        
