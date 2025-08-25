import pygame
from config import *

class ResourceSystem:
    def __init__(self):
        self.resources = []

    def spawn_resources(self, biome):
        self.resources = biome['resources']
        return self.resources

    def check_collection(self, player_position, crafting_system):
        collected = []
        for resource in self.resources[:]:
            distance = ((resource['position'][0] - player_position[0])**2 + 
                       (resource['position'][1] - player_position[1])**2)**0.5
            if distance < 50:  # Collection radius
                crafting_system.add_resource(resource['type'], resource['value'])
                collected.append(resource)
                self.resources.remove(resource)
        return collected

    def draw_resources(self, screen):
        for resource in self.resources:
            pygame.draw.circle(screen, resource['color'], resource['position'], 15)
