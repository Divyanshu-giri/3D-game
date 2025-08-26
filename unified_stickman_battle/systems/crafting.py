import pygame
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class CraftingSystem:
    def __init__(self):
        self.recipes = CRAFTING_RECIPES.copy()
        self.player_inventory = {}
        self.crafting_queue = []
        self.crafting_timers = {}
        self.available_recipes = set()
        
    def add_resource(self, resource_type, quantity=1):
        """Add resources to player inventory"""
        if resource_type not in self.player_inventory:
            self.player_inventory[resource_type] = 0
        self.player_inventory[resource_type] += quantity
        
        # Update available recipes
        self._update_available_recipes()
        
    def remove_resource(self, resource_type, quantity=1):
        """Remove resources from player inventory"""
        if resource_type in self.player_inventory:
            self.player_inventory[resource_type] = max(0, self.player_inventory[resource_type] - quantity)
            self._update_available_recipes()
            
    def get_resource_count(self, resource_type):
        """Get quantity of a specific resource"""
        return self.player_inventory.get(resource_type, 0)
    
    def get_all_resources(self):
        """Get all resources in inventory"""
        return self.player_inventory.copy()
    
    def can_craft(self, recipe_name):
        """Check if player can craft an item"""
        if recipe_name not in self.recipes:
            return False
            
        recipe = self.recipes[recipe_name]
        for resource, required in recipe.items():
            if self.get_resource_count(resource) < required:
                return False
        return True
        
    def craft_item(self, recipe_name, player_id):
        """Start crafting an item"""
        if not self.can_craft(recipe_name):
            return False
            
        # Deduct resources
        recipe = self.recipes[recipe_name]
        for resource, required in recipe.items():
            self.remove_resource(resource, required)
            
        # Add to crafting queue
        craft_data = {
            'recipe': recipe_name,
            'player_id': player_id,
            'start_time': pygame.time.get_ticks(),
            'duration': CRAFTING_TIME * 1000,  # Convert to milliseconds
            'completed': False
        }
        
        self.crafting_queue.append(craft_data)
        self.crafting_timers[recipe_name] = craft_data
        return True
        
    def get_crafting_progress(self, recipe_name):
        """Get crafting progress for an item"""
        if recipe_name not in self.crafting_timers:
            return 0.0
            
        craft_data = self.crafting_timers[recipe_name]
        if craft_data['completed']:
            return 1.0
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - craft_data['start_time']
        progress = min(1.0, elapsed / craft_data['duration'])
        return progress
        
    def update(self):
        """Update crafting system"""
        current_time = pygame.time.get_ticks()
        completed_items = []
        
        for craft_data in self.crafting_queue:
            if not craft_data['completed']:
                elapsed = current_time - craft_data['start_time']
                if elapsed >= craft_data['duration']:
                    craft_data['completed'] = True
                    completed_items.append(craft_data)
                    
        # Process completed items
        for completed in completed_items:
            self._complete_crafting(completed)
            self.crafting_queue.remove(completed)
            if completed['recipe'] in self.crafting_timers:
                del self.crafting_timers[completed['recipe']]
                
    def _complete_crafting(self, craft_data):
        """Complete crafting process and give item to player"""
        recipe_name = craft_data['recipe']
        player_id = craft_data['player_id']
        
        # TODO: Implement item granting to player
        print(f"Player {player_id} crafted {recipe_name}!")
        
        # Different effects based on crafted item
        if recipe_name == 'health_potion':
            # Grant health potion effect
            pass
        elif recipe_name == 'stamina_boost':
            # Grant stamina boost effect
            pass
        elif recipe_name == 'basic_sword':
            # Equip basic sword
            pass
        elif recipe_name == 'shield':
            # Equip shield
            pass
        elif recipe_name == 'armor':
            # Equip armor
            pass
            
    def _update_available_recipes(self):
        """Update list of available recipes based on current resources"""
        self.available_recipes.clear()
        
        for recipe_name, recipe in self.recipes.items():
            if self.can_craft(recipe_name):
                self.available_recipes.add(recipe_name)
                
    def get_available_recipes(self):
        """Get set of available recipes"""
        return self.available_recipes.copy()
        
    def get_recipe_requirements(self, recipe_name):
        """Get requirements for a specific recipe"""
        if recipe_name in self.recipes:
            return self.recipes[recipe_name].copy()
        return {}
        
    def get_recipe_info(self, recipe_name):
        """Get detailed info about a recipe"""
        if recipe_name not in self.recipes:
            return None
            
        recipe = self.recipes[recipe_name]
        info = {
            'name': recipe_name,
            'requirements': recipe,
            'can_craft': self.can_craft(recipe_name),
            'missing_resources': {}
        }
        
        # Calculate missing resources
        for resource, required in recipe.items():
            current = self.get_resource_count(resource)
            if current < required:
                info['missing_resources'][resource] = required - current
                
        return info
        
    def get_all_recipes_info(self):
        """Get info for all recipes"""
        recipes_info = {}
        for recipe_name in self.recipes:
            recipes_info[recipe_name] = self.get_recipe_info(recipe_name)
        return recipes_info
        
    def draw_crafting_menu(self, screen, position):
        """Draw crafting menu UI"""
        font = pygame.font.Font(None, FONT_SIZES['normal'])
        small_font = pygame.font.Font(None, FONT_SIZES['small'])
        
        # Draw background
        menu_width = 300
        menu_height = 400
        pygame.draw.rect(screen, UI_COLORS['crafting_bg'], 
                        (position[0], position[1], menu_width, menu_height))
        pygame.draw.rect(screen, (100, 100, 100), 
                        (position[0], position[1], menu_width, menu_height), 2)
                        
        # Draw title
        title = font.render("Crafting Menu", True, (255, 255, 255))
        screen.blit(title, (position[0] + 10, position[1] + 10))
        
        # Draw available recipes
        y_offset = 50
        for recipe_name in sorted(self.available_recipes):
            recipe_info = self.get_recipe_info(recipe_name)
            
            # Recipe name
            name_text = small_font.render(recipe_name, True, (255, 255, 255))
            screen.blit(name_text, (position[0] + 20, position[1] + y_offset))
            
            # Requirements
            req_y = y_offset + 20
            for resource, quantity in recipe_info['requirements'].items():
                req_text = small_font.render(f"  {resource}: {quantity}", True, 
                                           (200, 200, 200))
                screen.blit(req_text, (position[0] + 30, position[1] + req_y))
                req_y += 15
                
            y_offset = req_y + 10
            
        # Draw current resources
        resources_y = position[1] + menu_height - 120
        res_title = small_font.render("Your Resources:", True, (255, 255, 255))
        screen.blit(res_title, (position[0] + 10, resources_y))
        
        res_y = resources_y + 20
        for resource, quantity in self.player_inventory.items():
            if quantity > 0:
                res_text = small_font.render(f"{resource}: {quantity}", True, 
                                           (200, 200, 200))
                screen.blit(res_text, (position[0] + 20, res_y))
                res_y += 15
                
    def clear(self):
        """Clear crafting system state"""
        self.player_inventory.clear()
        self.crafting_queue.clear()
        self.crafting_timers.clear()
        self.available_recipes.clear()
