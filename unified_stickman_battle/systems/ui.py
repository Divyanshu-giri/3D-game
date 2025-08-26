import pygame
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class UIManager:
    def __init__(self):
        self.health_bars = {}
        self.score_text = None
        self.inventory_text = None
        
    def create_health_bar(self, player_id, position):
        """Create a health bar for a player"""
        self.health_bars[player_id] = {
            'position': position,
            'max_health': PLAYER_HEALTH,
            'current_health': PLAYER_HEALTH
        }
        
    def update_health_bar(self, player_id, health):
        """Update health bar for a player"""
        if player_id in self.health_bars:
            self.health_bars[player_id]['current_health'] = health
            
    def draw_health_bars(self, screen):
        """Draw all health bars on the screen"""
        for player_id, bar in self.health_bars.items():
            health_ratio = bar['current_health'] / bar['max_health']
            bar_width = 200
            bar_height = 20
            pygame.draw.rect(screen, (255, 0, 0), 
                             (bar['position'][0], bar['position'][1], bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                             (bar['position'][0], bar['position'][1], bar_width * health_ratio, bar_height))
            
    def create_score_display(self, position):
        """Create score display"""
        self.score_text = {
            'position': position,
            'score': {'player1': 0, 'player2': 0}
        }
        
    def update_score(self, player_id):
        """Update score for a player"""
        if player_id in self.score_text['score']:
            self.score_text['score'][player_id] += 1
            
    def draw_score(self, screen):
        """Draw score display on the screen"""
        score_text = f"{self.score_text['score']['player1']} - {self.score_text['score']['player2']}"
        font = pygame.font.Font(None, FONT_SIZES['normal'])
        text_surface = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, self.score_text['position'])
        
    def create_inventory_display(self, position):
        """Create inventory display"""
        self.inventory_text = {
            'position': position,
            'items': {}
        }
        
    def update_inventory(self, item, quantity):
        """Update inventory display"""
        if item in self.inventory_text['items']:
            self.inventory_text['items'][item] += quantity
        else:
            self.inventory_text['items'][item] = quantity
            
    def draw_inventory(self, screen):
        """Draw inventory display on the screen"""
        font = pygame.font.Font(None, FONT_SIZES['small'])
        y_offset = 0
        for item, quantity in self.inventory_text['items'].items():
            item_text = f"{item}: {quantity}"
            text_surface = font.render(item_text, True, (255, 255, 255))
            screen.blit(text_surface, (self.inventory_text['position'][0], 
                                        self.inventory_text['position'][1] + y_offset))
            y_offset += 20
            
    def clear(self):
        """Clear UI elements"""
        self.health_bars.clear()
        self.score_text = None
        self.inventory_text = None
