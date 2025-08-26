import pygame
import math
import random
from config import *

class Pseudo3DEffects:
    def __init__(self):
        self.shadows = []
        self.particles = []
        self.light_sources = []
        
    def create_shadow(self, position, size, intensity=100):
        """Create a pseudo-3D shadow effect"""
        shadow = {
            'position': position,
            'size': size,
            'intensity': intensity,
            'lifetime': 1000  # milliseconds
        }
        self.shadows.append(shadow)
        
    def create_particle_effect(self, position, effect_type, color=(255, 255, 255)):
        """Create various particle effects for realism"""
        particles = []
        
        if effect_type == "move":
            # Dust particles for movement
            for _ in range(5):
                particles.append({
                    'position': list(position),
                    'velocity': [random.uniform(-2, 2), random.uniform(-2, 2)],
                    'size': random.randint(2, 5),
                    'color': color,
                    'lifetime': random.randint(300, 800)
                })
                
        elif effect_type == "attack":
            # Impact particles for attacks
            for _ in range(10):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 5)
                particles.append({
                    'position': list(position),
                    'velocity': [math.cos(angle) * speed, math.sin(angle) * speed],
                    'size': random.randint(3, 6),
                    'color': (255, 100, 50),  # Orange-red for impact
                    'lifetime': random.randint(200, 500)
                })
                
        self.particles.extend(particles)
        
    def update_effects(self):
        """Update all visual effects"""
        # Update shadows
        self.shadows = [s for s in self.shadows if s['lifetime'] > 0]
        for shadow in self.shadows:
            shadow['lifetime'] -= 16  # Assuming 60 FPS
            
        # Update particles
        self.particles = [p for p in self.particles if p['lifetime'] > 0]
        for particle in self.particles:
            particle['position'][0] += particle['velocity'][0]
            particle['position'][1] += particle['velocity'][1]
            particle['lifetime'] -= 16
            
    def draw_shadows(self, screen):
        """Draw shadow effects"""
        for shadow in self.shadows:
            alpha = min(100, shadow['intensity'] * (shadow['lifetime'] / 1000))
            shadow_surface = pygame.Surface((shadow['size'], shadow['size']), pygame.SRCALPHA)
            shadow_color = (0, 0, 0, alpha)
            pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, shadow['size'], shadow['size']))
            screen.blit(shadow_surface, shadow['position'])
            
    def draw_particles(self, screen):
        """Draw particle effects"""
        for particle in self.particles:
            alpha = min(255, 255 * (particle['lifetime'] / 500))
            particle_color = (*particle['color'], alpha)
            pygame.draw.circle(screen, particle_color, 
                              (int(particle['position'][0]), int(particle['position'][1])), 
                              particle['size'])
            
    def create_light_flare(self, position, intensity=200):
        """Create a light flare effect for energy shards"""
        self.light_sources.append({
            'position': position,
            'intensity': intensity,
            'radius': 50,
            'lifetime': 1000
        })
        
    def draw_light_effects(self, screen):
        """Draw light source effects"""
        for light in self.light_sources:
            # Draw radial gradient for light effect
            for radius in range(light['radius'], 0, -5):
                alpha = min(100, light['intensity'] * (radius / light['radius']) * (light['lifetime'] / 1000))
                light_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                light_color = (255, 255, 200, alpha)
                pygame.draw.circle(light_surface, light_color, (radius, radius), radius)
                screen.blit(light_surface, (light['position'][0] - radius, light['position'][1] - radius))
