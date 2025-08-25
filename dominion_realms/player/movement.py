import pygame
from config import *

class PlayerMovement:
    def __init__(self, start_position):
        self.position = start_position
        self.velocity = [0, 0]
        self.on_ground = True
        self.health = PLAYER_HEALTH

    def jump(self):
        if self.on_ground:
            self.velocity[1] = PLAYER_JUMP_FORCE
            self.on_ground = False

    def update(self, direction, dt, terrain, collision_system):
        # Apply gravity
        self.velocity[1] += GRAVITY * dt
        if self.velocity[1] > TERMINAL_VELOCITY:
            self.velocity[1] = TERMINAL_VELOCITY
        
        # Move player
        self.position[0] += direction[0] * PLAYER_SPEED * dt
        self.position[1] += self.velocity[1] * dt
        
        # Check for collisions
        if collision_system.check_collision(self.position):
            self.on_ground = True
            self.velocity[1] = 0  # Reset vertical velocity on ground contact

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (*self.position, 50, 50))  # Draw player as a green square
