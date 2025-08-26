import pygame
import random
import math
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class Particle:
    def __init__(self, position, velocity, size, color, lifetime, particle_type='default'):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.particle_type = particle_type
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
    def update(self, dt):
        """Update particle position and state"""
        # Update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        
        # Apply gravity for certain particle types
        if self.particle_type in ['dust', 'smoke', 'blood']:
            self.velocity[1] += GRAVITY * 0.5 * dt
            
        # Apply drag
        self.velocity[0] *= 0.95
        self.velocity[1] *= 0.95
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Update lifetime
        self.lifetime -= dt * 1000  # Convert to milliseconds
        
        return self.lifetime > 0
        
    def draw(self, screen):
        """Draw the particle"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        if self.particle_type == 'spark':
            # Spark particles (lines)
            end_x = self.position[0] + math.cos(math.radians(self.rotation)) * self.size
            end_y = self.position[1] + math.sin(math.radians(self.rotation)) * self.size
            pygame.draw.line(screen,
                           (*self.color, alpha),
                           (self.position[0], self.position[1]),
                           (end_x, end_y),
                           2)
                           
        elif self.particle_type == 'circle':
            # Circle particles
            pygame.draw.circle(screen,
                             (*self.color, alpha),
                             (int(self.position[0]), int(self.position[1])),
                             self.size)
                             
        elif self.particle_type == 'square':
            # Square particles (rotated)
            points = []
            for i in range(4):
                angle = math.radians(self.rotation + i * 90)
                x = self.position[0] + math.cos(angle) * self.size
                y = self.position[1] + math.sin(angle) * self.size
                points.append((x, y))
            pygame.draw.polygon(screen,
                              (*self.color, alpha),
                              points)
                              
        else:
            # Default particle (circle)
            pygame.draw.circle(screen,
                             (*self.color, alpha),
                             (int(self.position[0]), int(self.position[1])),
                             self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 1000
        self.emitters = {}
        
    def create_particle(self, position, velocity=None, size=None, color=None, 
                       lifetime=None, particle_type='default'):
        """Create a new particle"""
        if len(self.particles) >= self.max_particles:
            return None
            
        if velocity is None:
            velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        if size is None:
            size = random.randint(2, 6)
        if color is None:
            color = (255, 255, 255)
        if lifetime is None:
            lifetime = random.randint(500, 2000)
            
        particle = Particle(position, velocity, size, color, lifetime, particle_type)
        self.particles.append(particle)
        return particle
        
    def create_explosion(self, position, count=20, color=(255, 200, 100), size_range=(3, 8)):
        """Create an explosion effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            velocity = [
                math.cos(angle) * speed,
                math.sin(angle) * speed
            ]
            self.create_particle(position, velocity, 
                               random.randint(*size_range), 
                               color,
                               random.randint(800, 1500),
                               'spark')
                               
    def create_blood_splash(self, position, count=15):
        """Create blood splash effect"""
        for _ in range(count):
            angle = random.uniform(math.pi/2, math.pi*3/2)  # Upward arc
            speed = random.uniform(3, 7)
            velocity = [
                math.cos(angle) * speed,
                math.sin(angle) * speed
            ]
            self.create_particle(position, velocity,
                               random.randint(3, 6),
                               (200, 0, 0),
                               random.randint(1000, 2000),
                               'circle')
                               
    def create_dust_cloud(self, position, count=10):
        """Create dust cloud effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            velocity = [
                math.cos(angle) * speed,
                math.sin(angle) * speed
            ]
            self.create_particle(position, velocity,
                               random.randint(4, 8),
                               (150, 150, 150),
                               random.randint(1500, 2500),
                               'dust')
                               
    def create_magic_effect(self, position, color=(100, 100, 255), count=12):
        """Create magic/spell effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            velocity = [
                math.cos(angle) * speed,
                math.sin(angle) * speed
            ]
            self.create_particle(position, velocity,
                               random.randint(4, 7),
                               color,
                               random.randint(1200, 2000),
                               'square')
                               
    def create_healing_effect(self, position, count=8):
        """Create healing effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 2)
            velocity = [
                math.cos(angle) * speed,
                math.sin(angle) * speed
            ]
            # Green particles moving upward
            velocity[1] -= random.uniform(1, 3)
            self.create_particle(position, velocity,
                               random.randint(3, 6),
                               (0, 255, 100),
                               random.randint(1000, 1800),
                               'circle')
                               
    def add_emitter(self, emitter_id, position, rate=10, particle_config=None):
        """Add a continuous particle emitter"""
        if particle_config is None:
            particle_config = {
                'velocity': [0, -1],
                'size': 3,
                'color': (255, 255, 255),
                'lifetime': 1000,
                'type': 'default'
            }
            
        self.emitters[emitter_id] = {
            'position': position,
            'rate': rate,
            'config': particle_config,
            'timer': 0
        }
        
    def remove_emitter(self, emitter_id):
        """Remove a particle emitter"""
        if emitter_id in self.emitters:
            del self.emitters[emitter_id]
            
    def update(self, dt):
        """Update all particles and emitters"""
        # Update existing particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Update emitters
        current_time = pygame.time.get_ticks()
        for emitter_id, emitter in list(self.emitters.items()):
            emitter['timer'] += dt * 1000
            if emitter['timer'] >= 1000 / emitter['rate']:
                emitter['timer'] = 0
                self.create_particle(
                    emitter['position'].copy(),
                    emitter['config']['velocity'],
                    emitter['config']['size'],
                    emitter['config']['color'],
                    emitter['config']['lifetime'],
                    emitter['config']['type']
                )
                
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
            
    def clear(self):
        """Clear all particles"""
        self.particles.clear()
        self.emitters.clear()
        
    def get_particle_count(self):
        """Get current particle count"""
        return len(self.particles)
