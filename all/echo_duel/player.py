import pygame
import time
import random
import math
from config import *
from echo import Echo

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = list(position)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.stamina = 100
        self.health = 100
        self.size = 30
        self.color = (255, 0, 0) if name == "Player 1" else (0, 255, 0)
        self.attack_cooldown = 0  # Cooldown for attacks
        self.health = 100  # Player health
        self.echoes = []
        self.last_move_time = 0
        self.move_echo_cooldown = 0.2  # Seconds between move echoes
        self.particles = []

    def move(self, direction):
        # Update position with boundary checking
        old_position = self.position.copy()
        self.position[0] = max(0, min(WIDTH - self.size, self.position[0] + direction[0]))
        self.position[1] = max(0, min(HEIGHT - self.size, self.position[1] + direction[1]))
        
        # Consume stamina for movement
        self.stamina = max(0, self.stamina - 1)
        
        # Create move echo if cooldown allows
        current_time = time.time()
        if current_time - self.last_move_time > self.move_echo_cooldown:
            self.echoes.append(Echo('move', old_position, self.color))
            self.last_move_time = current_time
            
            # Create movement particles
            self._create_movement_particles()

    def attack(self, target_player=None):
        if self.attack_cooldown <= 0:
            print(f"{self.name} attacks!")
            self.attack_cooldown = 30  # 0.5 seconds cooldown at 60 FPS
            
            # Create attack echo
            self.echoes.append(Echo('attack', self.position.copy(), self.color, delay=1.0))
            
            # Create attack particles
            self._create_attack_particles()
            
            # Deal damage to target player if provided and in range
            if target_player:
                attack_range = 100  # Attack range in pixels
                dx = target_player.position[0] - self.position[0]
                dy = target_player.position[1] - self.position[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < attack_range:
                    damage = 10  # Base damage
                    target_player.health -= damage
                    print(f"{self.name} hit {target_player.name} for {damage} damage!")

    def _create_movement_particles(self):
        """Create dust particles when moving"""
        for _ in range(3):
            self.particles.append({
                'position': [self.position[0] + self.size//2, self.position[1] + self.size],
                'velocity': [random.uniform(-1, 1), random.uniform(-2, -1)],
                'size': random.randint(2, 4),
                'color': (200, 200, 200),
                'lifetime': random.randint(300, 600)
            })

    def _create_attack_particles(self):
        """Create impact particles when attacking"""
        for _ in range(8):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(3, 6)
            self.particles.append({
                'position': [self.position[0] + self.size//2, self.position[1] + self.size//2],
                'velocity': [math.cos(angle) * speed, math.sin(angle) * speed],
                'size': random.randint(3, 6),
                'color': (255, 100, 50),
                'lifetime': random.randint(200, 400)
            })

    def update(self):
        # Recover stamina
        self.stamina = min(100, self.stamina + 0.2)
        
        # Update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Update echoes
        self.echoes = [echo for echo in self.echoes if echo.update()]
        
        # Update particles
        self.particles = [p for p in self.particles if p['lifetime'] > 0]
        for particle in self.particles:
            particle['position'][0] += particle['velocity'][0]
            particle['position'][1] += particle['velocity'][1]
            particle['lifetime'] -= 16

    def draw(self, screen):
        # Draw particles first (behind player)
        for particle in self.particles:
            # Use the base color without alpha for simplicity
            pygame.draw.circle(screen, particle['color'], 
                              (int(particle['position'][0]), int(particle['position'][1])), 
                              particle['size'])
        
        # Draw echoes
        for echo in self.echoes:
            echo.draw(screen)
        
        # Draw player character with 3D-like shading
        # Main body
        pygame.draw.rect(screen, self.color, 
                        (self.position[0], self.position[1], self.size, self.size))
        
        # Highlight (top-left corner)
        highlight_color = tuple(min(255, c + 40) for c in self.color)
        pygame.draw.rect(screen, highlight_color, 
                        (self.position[0], self.position[1], self.size//2, self.size//2))
        
        # Shadow (bottom-right corner)
        shadow_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.rect(screen, shadow_color, 
                        (self.position[0] + self.size//2, self.position[1] + self.size//2, 
                         self.size//2, self.size//2))
        
        # Draw stamina bar with 3D effect
        bar_width = 40
        bar_height = 6
        bar_bg = (self.position[0] - 5, self.position[1] - 12, bar_width, bar_height)
        bar_fg = (self.position[0] - 5, self.position[1] - 12, 
                 bar_width * (self.stamina / 100), bar_height)
        
        # Bar background with border
        pygame.draw.rect(screen, (50, 50, 50), bar_bg)
        pygame.draw.rect(screen, (100, 100, 100), bar_bg, 1)
        
        # Bar foreground with gradient
        if self.stamina > 0:
            stamina_color = (
                int(255 * (1 - self.stamina/100)),
                int(255 * (self.stamina/100)),
                0
            )
            pygame.draw.rect(screen, stamina_color, bar_fg)
            pygame.draw.rect(screen, (200, 200, 200), bar_fg, 1)
