import pygame
import random
from config import *

class Terrain:
    def __init__(self):
        self.obstacles = []
        self.generate_terrain()
        self.biome = "crystal_cave"  # Default biome
        self.biome_colors = {
            "minecraft": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],  # Example colors for Minecraft biome
            "crystal_cave": [(100, 100, 255), (150, 150, 255), (200, 200, 255)],
            "decaying_temple": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
            "floating_islands": [(144, 238, 144), (152, 251, 152), (173, 255, 47)]
        }
        self.background_color = (30, 30, 50)  # Default dark blue

    def generate_terrain(self):
        # Generate random obstacles
        self.obstacles = []
        for _ in range(15):
            obstacle = {
                'position': [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)],
                'size': random.randint(20, 40),
                'type': random.choice(['rock', 'crystal', 'pillar'])
            }
            self.obstacles.append(obstacle)

    def change_biome(self, biome_name):
        """Change the current biome theme"""
        if biome_name in self.biome_colors:
            self.biome = biome_name
            # Update background color based on biome
            if biome_name == "crystal_cave":
                self.background_color = (30, 30, 50)  # Deep blue
            elif biome_name == "decaying_temple":
                self.background_color = (40, 25, 15)  # Brownish
            elif biome_name == "floating_islands":
                self.background_color = (25, 50, 30)  # Greenish
            elif biome_name == "minecraft":
                self.background_color = (50, 50, 50)  # Gray for Minecraft

    def draw(self, screen):
        # Draw background
        screen.fill(self.background_color)
        
        # Draw obstacles with 3D effects
        for obstacle in self.obstacles:
            x, y = obstacle['position']
            size = obstacle['size']
            
            # Choose color based on obstacle type and biome
            if obstacle['type'] == 'rock':
                base_color = self.biome_colors[self.biome][0]
            elif obstacle['type'] == 'crystal':
                base_color = self.biome_colors[self.biome][1]
            else:  # pillar
                base_color = self.biome_colors[self.biome][2]
            
            # Draw obstacle with 3D shading
            # Main body
            pygame.draw.rect(screen, base_color, (x, y, size, size))
            
            # Highlight (top-left)
            highlight_color = tuple(min(255, c + 30) for c in base_color)
            pygame.draw.rect(screen, highlight_color, (x, y, size//2, size//2))
            
            # Shadow (bottom-right)
            shadow_color = tuple(max(0, c - 30) for c in base_color)
            pygame.draw.rect(screen, shadow_color, 
                           (x + size//2, y + size//2, size//2, size//2))
            
            # Add details based on obstacle type
            if obstacle['type'] == 'crystal':
                # Draw crystal facets
                pygame.draw.polygon(screen, highlight_color, [
                    (x + size//2, y),
                    (x + size, y + size//2),
                    (x + size//2, y + size),
                    (x, y + size//2)
                ], 1)
            
            elif obstacle['type'] == 'pillar':
                # Draw pillar details
                pygame.draw.rect(screen, shadow_color, (x + size//4, y, size//2, size), 1)
                pygame.draw.rect(screen, highlight_color, (x, y + size//4, size, size//2), 1)

    def check_collision(self, position, size):
        """Check if a position collides with any obstacle"""
        for obstacle in self.obstacles:
            obs_x, obs_y = obstacle['position']
            obs_size = obstacle['size']
            
            # Simple rectangle collision
            if (position[0] < obs_x + obs_size and
                position[0] + size > obs_x and
                position[1] < obs_y + obs_size and
                position[1] + size > obs_y):
                return True
        return False

    def get_biome_info(self):
        """Return information about the current biome"""
        return {
            'name': self.biome,
            'colors': self.biome_colors[self.biome],
            'background': self.background_color
        }

    def place_block(self, position, block_type):
        """Place a block at the specified position"""
        block_size = 30
        block = {
            'position': [position[0] - block_size//2, position[1] - block_size//2],
            'size': block_size,
            'type': block_type,
            'color': self._get_block_color(block_type)
        }
        self.obstacles.append(block)
        print(f"Placed {block_type} block at {position}")

    def break_block(self, position):
        """Break a block at the specified position"""
        break_radius = 50
        for i, obstacle in enumerate(self.obstacles[:]):
            obs_x, obs_y = obstacle['position']
            obs_size = obstacle['size']
            
            # Check if player is close enough to break the block
            dx = position[0] - (obs_x + obs_size//2)
            dy = position[1] - (obs_y + obs_size//2)
            distance = (dx**2 + dy**2)**0.5
            
            if distance < break_radius:
                self.obstacles.remove(obstacle)
                print(f"Broke {obstacle['type']} block at {obstacle['position']}")
                return True
        return False

    def _get_block_color(self, block_type):
        """Get color for different block types"""
        colors = {
            'dirt': (139, 69, 19),
            'stone': (128, 128, 128),
            'wood': (160, 82, 45),
            'crystal': (0, 191, 255)
        }
        return colors.get(block_type, (200, 200, 200))
