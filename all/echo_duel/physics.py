import pygame
import math
from config import *

class PhysicsSystem:
    def __init__(self):
        self.gravity = 0.5
        self.jump_force = -12
        self.friction = 0.9
        self.terminal_velocity = 15
        
    def apply_gravity(self, player, terrain):
        """Apply gravity and handle ground collision"""
        # Apply gravity
        player.velocity_y += self.gravity
        
        # Limit terminal velocity
        player.velocity_y = min(player.velocity_y, self.terminal_velocity)
        
        # Check ground collision
        player.on_ground = False
        if player.position[1] + player.size >= HEIGHT - 10:  # Ground level
            player.position[1] = HEIGHT - player.size - 10
            player.velocity_y = 0
            player.on_ground = True
            
        # Check terrain block collisions
        for obstacle in terrain.obstacles:
            obs_x, obs_y = obstacle['position']
            obs_size = obstacle['size']
            
            # Check if player is above obstacle and falling
            if (player.position[0] + player.size > obs_x and
                player.position[0] < obs_x + obs_size and
                player.position[1] + player.size <= obs_y and
                player.velocity_y > 0):
                
                player.position[1] = obs_y - player.size
                player.velocity_y = 0
                player.on_ground = True
                break
    
    def apply_movement(self, player, direction):
        """Apply movement with friction and collision handling"""
        # Apply horizontal movement with friction
        player.velocity_x = direction[0] * 5
        player.velocity_x *= self.friction
        
        # Update position
        player.position[0] += player.velocity_x
        player.position[1] += player.velocity_y
        
        # Boundary checking
        player.position[0] = max(0, min(WIDTH - player.size, player.position[0]))
        player.position[1] = max(0, min(HEIGHT - player.size, player.position[1]))
    
    def handle_jump(self, player):
        """Handle jumping mechanics"""
        if player.on_ground:
            player.velocity_y = self.jump_force
            player.on_ground = False
            return True
        return False
    
    def check_collision(self, obj1_pos, obj1_size, obj2_pos, obj2_size):
        """Check collision between two objects"""
        return (obj1_pos[0] < obj2_pos[0] + obj2_size and
                obj1_pos[0] + obj1_size > obj2_pos[0] and
                obj1_pos[1] < obj2_pos[1] + obj2_size and
                obj1_pos[1] + obj1_size > obj2_pos[1])
    
    def resolve_collision(self, player1, player2):
        """Resolve collision between two players"""
        if self.check_collision(player1.position, player1.size, 
                              player2.position, player2.size):
            # Simple collision response - push players apart
            dx = player2.position[0] - player1.position[0]
            dy = player2.position[1] - player1.position[1]
            
            # Normalize direction
            distance = max(0.1, math.sqrt(dx*dx + dy*dy))
            dx /= distance
            dy /= distance
            
            # Push players apart
            overlap = (player1.size + player2.size) - distance
            player1.position[0] -= dx * overlap * 0.5
            player1.position[1] -= dy * overlap * 0.5
            player2.position[0] += dx * overlap * 0.5
            player2.position[1] += dy * overlap * 0.5
            
            return True
        return False
