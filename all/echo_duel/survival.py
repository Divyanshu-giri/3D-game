import pygame
import random
from config import *

class EnergyShard:
    def __init__(self):
        self.position = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
        self.size = 15
        self.color = (255, 215, 0)  # Gold color
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10000  # 10 seconds

    def update(self):
        # Check if shard should expire
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.active = False
        return self.active

    def draw(self, screen):
        if self.active:
            # Draw shard with pulsing effect
            pulse = (pygame.time.get_ticks() // 200) % 2
            size_mod = 2 if pulse else 0
            pygame.draw.circle(screen, self.color, 
                              (self.position[0], self.position[1]), 
                              self.size + size_mod)

    def check_collision(self, player_pos, player_size):
        # Simple collision detection
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        shard_rect = pygame.Rect(self.position[0] - self.size, self.position[1] - self.size, 
                                self.size * 2, self.size * 2)
        return player_rect.colliderect(shard_rect)

class Survival:
    def __init__(self):
        self.energy_shards = 0
        self.shards = []
        self.shard_spawn_timer = 0
        self.shard_spawn_interval = 5000  # 5 seconds between shard spawns

    def update(self):
        # Spawn new shards
        current_time = pygame.time.get_ticks()
        if current_time - self.shard_spawn_timer > self.shard_spawn_interval:
            self.shards.append(EnergyShard())
            self.shard_spawn_timer = current_time
        
        # Update existing shards
        self.shards = [shard for shard in self.shards if shard.update()]

    def check_player_collisions(self, player):
        collected = 0
        remaining_shards = []
        
        for shard in self.shards:
            if shard.active and shard.check_collision(player.position, player.size):
                self.energy_shards += 1
                collected += 1
            else:
                remaining_shards.append(shard)
        
        self.shards = remaining_shards
        return collected

    def draw(self, screen):
        for shard in self.shards:
            shard.draw(screen)

    def use_shard(self):
        if self.energy_shards > 0:
            self.energy_shards -= 1
            return True
        return False
