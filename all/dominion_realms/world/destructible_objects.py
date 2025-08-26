import pygame
import random
from config import *

class DestructibleSystem:
    def __init__(self):
        self.objects = []
        
    def spawn_objects(self, biome):
        # Create some destructible objects based on biome
        self.objects = []
        for _ in range(8):  # 8 destructible objects
            obj = {
                'position': [random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)],
                'size': random.randint(30, 60),
                'health': random.randint(20, 50),
                'type': random.choice(['rock', 'crystal', 'barrel']),
                'color': random.choice(biome['obstacle_color'])
            }
            self.objects.append(obj)
        return self.objects
        
    def draw_objects(self, screen):
        for obj in self.objects:
            if obj['health'] > 0:
                pygame.draw.rect(screen, obj['color'], 
                               (*obj['position'], obj['size'], obj['size']))
                
    def check_damage(self, position, damage_radius, damage_amount):
        # Check if any objects are within damage radius and apply damage
        for obj in self.objects:
            if obj['health'] > 0:
                dx = obj['position'][0] - position[0]
                dy = obj['position'][1] - position[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < damage_radius:
                    obj['health'] -= damage_amount
                    if obj['health'] <= 0:
                        print(f"Destroyed {obj['type']} object!")
