import pygame
from config import *

class InventorySystem:
    def __init__(self):
        self.visible = False
        self.font = pygame.font.Font(None, 20)
        
    def toggle_inventory(self):
        self.visible = not self.visible
        
    def draw(self, screen):
        if self.visible:
            # Draw inventory background
            inventory_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, UI_COLORS['inventory_bg'], inventory_rect)
            pygame.draw.rect(screen, (255, 255, 255), inventory_rect, 2)
            
            # Draw inventory title
            title = self.font.render("INVENTORY", True, (255, 255, 255))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 + 20))
            
            # Draw placeholder items
            items = ["Sword", "Shield", "Potion", "Armor"]
            for i, item in enumerate(items):
                item_text = self.font.render(f"- {item}", True, (200, 200, 200))
                screen.blit(item_text, (WIDTH // 4 + 50, HEIGHT // 4 + 60 + i * 30))
