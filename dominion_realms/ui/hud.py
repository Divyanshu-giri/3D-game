import pygame
from config import *

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        
    def draw(self, screen, player1_health, player2_health, timer, phase):
        # Draw player 1 health
        health_text = self.font.render(f"P1 Health: {player1_health}", True, UI_COLORS['health_bar'])
        screen.blit(health_text, (20, 20))
        
        # Draw player 2 health
        health_text = self.font.render(f"P2 Health: {player2_health}", True, UI_COLORS['health_bar'])
        screen.blit(health_text, (WIDTH - 150, 20))
        
        # Draw timer
        timer_text = self.font.render(f"Time: {int(timer)}s", True, UI_COLORS['resource_text'])
        screen.blit(timer_text, (WIDTH // 2 - 50, 20))
        
        # Draw phase
        phase_text = self.font.render(f"Phase: {phase}", True, UI_COLORS['resource_text'])
        screen.blit(phase_text, (WIDTH // 2 - 50, 50))
