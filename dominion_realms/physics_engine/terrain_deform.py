import pygame
import random
from config import *

class TerrainDeformation:
    def __init__(self):
        self.deformations = []  # List of active terrain deformations
        self.earthquake_active = False
        self.earthquake_timer = 0

    def create_crater(self, position, duration):
        crater = {
            'type': 'crater',
            'position': position,
            'radius': 50,
            'duration': duration,
            'start_time': pygame.time.get_ticks() / 1000.0
        }
        self.deformations.append(crater)

    def create_lava_pool(self, position, duration):
        lava_pool = {
            'type': 'lava_pool',
            'position': position,
            'radius': 80,
            'duration': duration,
            'start_time': pygame.time.get_ticks() / 1000.0
        }
        self.deformations.append(lava_pool)

    def create_crystal_spike(self, position, duration):
        crystal_spike = {
            'type': 'crystal_spike',
            'position': position,
            'radius': 30,
            'duration': duration,
            'start_time': pygame.time.get_ticks() / 1000.0
        }
        self.deformations.append(crystal_spike)

    def create_lightning_strike(self, position, duration):
        lightning_strike = {
            'type': 'lightning_strike',
            'position': position,
            'radius': 40,
            'duration': duration,
            'start_time': pygame.time.get_ticks() / 1000.0
        }
        self.deformations.append(lightning_strike)

    def apply_earthquake(self, duration):
        self.earthquake_active = True
        self.earthquake_timer = duration

    def apply_wind_gust(self, duration):
        wind_gust = {
            'type': 'wind_gust',
            'duration': duration,
            'start_time': pygame.time.get_ticks() / 1000.0
        }
        self.deformations.append(wind_gust)

    def update(self, dt):
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Update earthquake
        if self.earthquake_active:
            self.earthquake_timer -= dt
            if self.earthquake_timer <= 0:
                self.earthquake_active = False

        # Update other deformations
        self.deformations = [d for d in self.deformations 
                           if current_time - d['start_time'] < d['duration']]

    def draw_terrain(self, screen, terrain):
        # Draw base terrain
        screen.fill((50, 50, 50))  # Dark gray background
        
        # Draw deformations
        for deformation in self.deformations:
            if deformation['type'] == 'crater':
                pygame.draw.circle(screen, (100, 100, 100), 
                                  deformation['position'], deformation['radius'])
            elif deformation['type'] == 'lava_pool':
                pygame.draw.circle(screen, (255, 69, 0), 
                                  deformation['position'], deformation['radius'])
            elif deformation['type'] == 'crystal_spike':
                pygame.draw.circle(screen, (0, 191, 255), 
                                  deformation['position'], deformation['radius'])
            elif deformation['type'] == 'lightning_strike':
                pygame.draw.circle(screen, (255, 255, 0), 
                                  deformation['position'], deformation['radius'])
