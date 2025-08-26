import pygame
import math
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class PhysicsSystem:
    def __init__(self):
        self.gravity = GRAVITY
        self.friction = FRICTION
        self.terminal_velocity = TERMINAL_VELOCITY
        self.collision_damping = COLLISION_DAMPING
        
    def apply_gravity(self, entity, dt):
        """Apply gravity to an entity"""
        if not entity.get('on_ground', False):
            entity['velocity'][1] += self.gravity * dt
            if entity['velocity'][1] > self.terminal_velocity:
                entity['velocity'][1] = self.terminal_velocity
    
    def apply_movement(self, entity, direction, speed, dt):
        """Apply movement to an entity"""
        entity['velocity'][0] = direction[0] * speed * dt
        entity['velocity'][1] = direction[1] * speed * dt
    
    def apply_friction(self, entity, dt):
        """Apply friction to slow down movement"""
        entity['velocity'][0] *= self.friction
        entity['velocity'][1] *= self.friction
    
    def handle_jump(self, entity, jump_force):
        """Handle jumping mechanics"""
        if entity.get('on_ground', False):
            entity['velocity'][1] = jump_force
            entity['on_ground'] = False
            return True
        return False
    
    def check_collision(self, position, terrain, entity_size=50):
        """Check if entity collides with terrain"""
        # Simple ground collision
        if position[1] >= HEIGHT - 50 - entity_size:
            return True
        
        # Check terrain blocks collision (simplified)
        for block in terrain.get('blocks', []):
            block_rect = pygame.Rect(block['x'], block['y'], block['size'], block['size'])
            entity_rect = pygame.Rect(position[0], position[1], entity_size, entity_size)
            if block_rect.colliderect(entity_rect):
                return True
        
        return False
    
    def resolve_collision(self, entity1, entity2):
        """Resolve collision between two entities"""
        if not entity1 or not entity2:
            return
        
        # Calculate distance between entities
        dx = entity2['position'][0] - entity1['position'][0]
        dy = entity2['position'][1] - entity1['position'][1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return
            
        # Minimum distance to avoid collision (sum of radii)
        min_distance = (entity1.get('size', 25) + entity2.get('size', 25)) / 2
        
        if distance < min_distance:
            # Calculate overlap
            overlap = min_distance - distance
            
            # Normalize direction
            nx = dx / distance
            ny = dy / distance
            
            # Move entities apart
            entity1['position'][0] -= nx * overlap * 0.5
            entity1['position'][1] -= ny * overlap * 0.5
            entity2['position'][0] += nx * overlap * 0.5
            entity2['position'][1] += ny * overlap * 0.5
            
            # Apply damping to velocities
            entity1['velocity'][0] *= self.collision_damping
            entity1['velocity'][1] *= self.collision_damping
            entity2['velocity'][0] *= self.collision_damping
            entity2['velocity'][1] *= self.collision_damping
    
    def update_entity_position(self, entity, dt, terrain=None):
        """Update entity position with collision checking"""
        if not entity:
            return
            
        # Apply gravity
        self.apply_gravity(entity, dt)
        
        # Update position
        entity['position'][0] += entity['velocity'][0] * dt
        entity['position'][1] += entity['velocity'][1] * dt
        
        # Check for ground collision
        if terrain and self.check_collision(entity['position'], terrain, entity.get('size', 50)):
            entity['position'][1] = HEIGHT - 50 - entity.get('size', 50)
            entity['velocity'][1] = 0
            entity['on_ground'] = True
        else:
            entity['on_ground'] = False
        
        # Apply friction
        self.apply_friction(entity, dt)
    
    def check_attack_range(self, attacker, target, attack_range):
        """Check if target is within attack range"""
        dx = target['position'][0] - attacker['position'][0]
        dy = target['position'][1] - attacker['position'][1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance <= attack_range
    
    def get_direction_to_target(self, source, target):
        """Get normalized direction vector to target"""
        dx = target['position'][0] - source['position'][0]
        dy = target['position'][1] - source['position'][1]
        distance = max(0.1, math.sqrt(dx*dx + dy*dy))
        return (dx/distance, dy/distance)
