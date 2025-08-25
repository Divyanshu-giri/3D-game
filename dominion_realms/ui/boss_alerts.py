import pygame
from config import *

class BossAlertSystem:
    def __init__(self):
        self.active_alerts = []
        self.font = pygame.font.Font(None, 32)
        
    def trigger_boss_alert(self, boss_name):
        self.active_alerts.append({
            'boss_name': boss_name,
            'duration': 3.0,  # seconds
            'start_time': pygame.time.get_ticks() / 1000.0
        })
        
    def draw(self, screen):
        current_time = pygame.time.get_ticks() / 1000.0
        self.active_alerts = [alert for alert in self.active_alerts 
                            if current_time - alert['start_time'] < alert['duration']]
        
        for alert in self.active_alerts:
            # Calculate fade effect
            elapsed = current_time - alert['start_time']
            alpha = int(255 * (1 - elapsed / alert['duration']))
            
            # Draw boss alert text
            alert_text = self.font.render(f"BOSS SPAWNED: {alert['boss_name']}", True, (255, 0, 0))
            text_surface = pygame.Surface(alert_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((0, 0, 0, alpha))
            text_surface.blit(alert_text, (0, 0))
            screen.blit(text_surface, (WIDTH // 2 - alert_text.get_width() // 2, 100))
