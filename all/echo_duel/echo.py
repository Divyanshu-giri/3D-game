import pygame
import time
from config import *

class Echo:
    def __init__(self, action_type, position, player_color, delay=3.0):
        self.action_type = action_type  # 'move', 'attack'
        self.original_position = position
        self.position = list(position)
        self.color = player_color
        self.alpha = 255  # For fading effect
        self.delay = delay  # Seconds before echo appears
        self.spawn_time = time.time() + self.delay
        self.active = False
        self.lifetime = 2.0  # How long echo stays visible
        self.size = 30

    def update(self):
        current_time = time.time()
        
        # Check if it's time to activate the echo
        if not self.active and current_time >= self.spawn_time:
            self.active = True
            self.spawn_time = current_time
        
        # If active, handle fading and lifetime
        if self.active:
            elapsed = current_time - self.spawn_time
            if elapsed >= self.lifetime:
                return False  # Echo should be removed
            
            # Fade out effect
            self.alpha = max(0, 255 * (1 - elapsed / self.lifetime))
            
            # For move echoes, they could move in the original direction
            if self.action_type == 'move':
                pass  # Could implement movement replay here
            
        return True  # Echo is still active

    def draw(self, screen):
        if self.active:
            # Create a surface with alpha for the fading effect
            echo_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            echo_color = (*self.color, self.alpha)  # Add alpha to color
            
            if self.action_type == 'move':
                pygame.draw.rect(echo_surface, echo_color, (0, 0, self.size, self.size))
            elif self.action_type == 'attack':
                # Draw a different shape for attacks
                pygame.draw.circle(echo_surface, echo_color, (self.size//2, self.size//2), self.size//2)
            
            screen.blit(echo_surface, self.position)

    def get_action_type(self):
        return self.action_type

    def get_position(self):
        return self.position
