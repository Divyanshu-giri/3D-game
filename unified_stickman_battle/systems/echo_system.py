import pygame
import time
import math
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class Echo:
    def __init__(self, action_type, position, color, delay=0.0, lifetime=2.0):
        self.action_type = action_type
        self.position = position.copy()
        self.color = color
        self.delay = delay
        self.lifetime = lifetime
        self.spawn_time = time.time() + delay
        self.active = False
        self.alpha = 255
        self.size = 30
        
    def update(self):
        current_time = time.time()
        
        # Check if it's time to activate
        if not self.active and current_time >= self.spawn_time:
            self.active = True
            self.spawn_time = current_time
            
        if self.active:
            elapsed = current_time - self.spawn_time
            if elapsed >= self.lifetime:
                return False  # Echo expired
                
            # Fade out effect
            self.alpha = max(0, 255 * (1 - elapsed / self.lifetime))
            
            # Size pulsation for certain echo types
            if self.action_type == 'attack':
                pulse = math.sin(elapsed * 10) * 5
                self.size = 30 + int(pulse)
            elif self.action_type == 'jump':
                self.size = max(20, 30 - elapsed * 10)
                
        return True
        
    def draw(self, screen):
        if not self.active:
            return
            
        # Create surface with alpha
        echo_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw echo based on action type
        if self.action_type == 'move':
            # Movement echo (faint circle)
            pygame.draw.circle(echo_surface, 
                             (*self.color, self.alpha // 2),
                             (self.size, self.size), 
                             self.size // 2)
                             
        elif self.action_type == 'attack':
            # Attack echo (concentric circles)
            for i in range(3):
                radius = self.size // 2 - i * 5
                if radius > 0:
                    alpha = self.alpha // (i + 1)
                    pygame.draw.circle(echo_surface,
                                     (*self.color, alpha),
                                     (self.size, self.size),
                                     radius,
                                     2)
                                     
        elif self.action_type == 'jump':
            # Jump echo (expanding ring)
            ring_width = max(1, int(self.size * 0.1))
            pygame.draw.circle(echo_surface,
                             (*self.color, self.alpha),
                             (self.size, self.size),
                             self.size // 2,
                             ring_width)
                             
        elif self.action_type == 'special':
            # Special attack echo (star pattern)
            points = []
            for i in range(8):
                angle = math.pi * 2 * i / 8
                radius = self.size // 2 if i % 2 == 0 else self.size // 4
                x = self.size + math.cos(angle) * radius
                y = self.size + math.sin(angle) * radius
                points.append((x, y))
            pygame.draw.polygon(echo_surface,
                              (*self.color, self.alpha),
                              points)
        
        # Draw the echo surface
        screen.blit(echo_surface, 
                   (self.position[0] - self.size, self.position[1] - self.size))

class EchoSystem:
    def __init__(self):
        self.echoes = []
        self.max_echoes = 50  # Limit to prevent performance issues
        
    def create_echo(self, action_type, position, color, delay=0.0, lifetime=2.0):
        """Create a new echo effect"""
        if len(self.echoes) >= self.max_echoes:
            # Remove oldest echo if we're at the limit
            self.echoes.pop(0)
            
        echo = Echo(action_type, position, color, delay, lifetime)
        self.echoes.append(echo)
        return echo
        
    def update(self):
        """Update all echoes and remove expired ones"""
        self.echoes = [echo for echo in self.echoes if echo.update()]
        
    def draw(self, screen):
        """Draw all active echoes"""
        for echo in self.echoes:
            echo.draw(screen)
            
    def clear(self):
        """Clear all echoes"""
        self.echoes.clear()
        
    def get_echoes_at_position(self, position, radius=50):
        """Get echoes near a specific position"""
        nearby_echoes = []
        for echo in self.echoes:
            if echo.active:
                dx = echo.position[0] - position[0]
                dy = echo.position[1] - position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius:
                    nearby_echoes.append(echo)
        return nearby_echoes
        
    def create_chain_reaction(self, position, color, count=5, delay_step=0.1):
        """Create a chain reaction of echoes"""
        for i in range(count):
            self.create_echo('special', 
                           [position[0] + (i * 10), position[1]],
                           color,
                           delay_step * i,
                           1.5)
                           
    def create_radial_echoes(self, position, color, count=8, delay=0.0):
        """Create radial pattern of echoes"""
        for i in range(count):
            angle = math.pi * 2 * i / count
            distance = 50
            target_pos = [
                position[0] + math.cos(angle) * distance,
                position[1] + math.sin(angle) * distance
            ]
            self.create_echo('move', target_pos, color, delay)
