import random
from config import *

class BossAI:
    def __init__(self):
        self.state = 'idle'
        self.state_timer = 0

    def update(self, boss, player_positions, dt):
        self.state_timer += dt
        
        # Find closest player
        closest_player = min(player_positions, key=lambda pos: self.distance(boss.position, pos))
        
        # State machine
        if self.state == 'idle':
            if self.state_timer > 2.0:  # Wait 2 seconds in idle
                self.state = 'chase'
                self.state_timer = 0
                
        elif self.state == 'chase':
            # Move towards closest player
            direction = self.get_direction(boss.position, closest_player)
            boss.position[0] += direction[0] * BOSS_MOVEMENT_SPEED * dt
            boss.position[1] += direction[1] * BOSS_MOVEMENT_SPEED * dt
            
            if self.distance(boss.position, closest_player) < 100:  # Close enough to attack
                self.state = 'attack'
                self.state_timer = 0
                
        elif self.state == 'attack':
            if self.state_timer > BOSS_ATTACK_COOLDOWN:
                # Perform attack
                self.state = 'chase'
                self.state_timer = 0

    def get_direction(self, from_pos, to_pos):
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        distance = max(0.1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        return [dx/distance, dy/distance]

    def distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

    def draw_boss(self, screen, boss):
        pygame.draw.rect(screen, boss.color, (*boss.position, 80, 80))  # Draw boss as a colored square
