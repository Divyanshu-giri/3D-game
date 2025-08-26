import random
from config import *

class BiomeGenerator:
    def __init__(self):
        self.biome_types = BIOME_TYPES

    def generate_biome(self, biome_name):
        if biome_name in self.biome_types:
            return self.biome_types[biome_name]
        else:
            # Default to volcanic crater if biome not found
            return self.biome_types['volcanic_crater']

    def create_terrain(self, biome):
        # Create terrain based on biome type
        terrain = {
            'type': biome['boss_type'],
            'ground_color': biome['ground_color'],
            'obstacle_color': biome['obstacle_color'],
            'resources': self.generate_resources(biome['resource_spawns']),
            'obstacles': self.generate_obstacles()
        }
        return terrain

    def generate_resources(self, resource_types):
        resources = []
        for _ in range(10):  # Generate 10 resources
            resource_type = random.choice(resource_types)
            position = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
            resources.append({
                'type': resource_type,
                'position': position,
                'value': RESOURCE_TYPES[resource_type]['value'],
                'color': RESOURCE_TYPES[resource_type]['color']
            })
        return resources

    def generate_obstacles(self):
        obstacles = []
        for _ in range(5):  # Generate 5 obstacles
            position = [random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)]
            size = random.randint(30, 80)
            obstacles.append({
                'position': position,
                'size': size,
                'color': (100, 100, 100)
            })
        return obstacles
