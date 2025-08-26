import random
from config import *

class BossSpawnSystem:
    def __init__(self):
        self.boss_types = list(BOSS_TYPES.keys())

    def spawn_boss(self, biome):
        boss_type = random.choice(self.boss_types)
        boss_attributes = BOSS_TYPES[boss_type]
        boss = Boss(boss_type, boss_attributes['health'], boss_attributes['damage'], boss_attributes['speed'], boss_attributes['abilities'])
        print(f"Spawned {boss_type} in {biome}")
        return boss

class Boss:
    def __init__(self, name, health, damage, speed, abilities):
        self.name = name
        self.health = health
        self.damage = damage
        self.speed = speed
        self.abilities = abilities
        self.position = [random.randint(100, 700), random.randint(100, 500)]  # Random spawn position
        self.color = (255, 0, 0)  # Red color for boss

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, 80, 80))  # Draw boss as a colored square
