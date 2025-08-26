#!/usr/bin/env python3
"""
Mobile entry point for Unified Stickman Battle Game
This is a simplified version for Android deployment
"""

import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
    from unified_stickman_battle.config import *
    from unified_stickman_battle.systems.physics import PhysicsSystem
    from unified_stickman_battle.systems.combat import CombatSystem
    from unified_stickman_battle.systems.particle_system import ParticleSystem
    
    print("Game modules imported successfully")
    
except ImportError as e:
    print(f"Import error: {e}")
    # Try to install missing dependencies
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame installed successfully")
    except:
        print("Failed to install pygame")
    sys.exit(1)

def mobile_main():
    """Simplified mobile version of the game"""
    pygame.init()
    
    # Set up display for mobile
    info = pygame.display.Info()
    screen_width = min(1024, info.current_w)
    screen_height = min(768, info.current_h)
    
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Stickman Battle")
    
    # Initialize game systems
    physics = PhysicsSystem()
    combat = CombatSystem()
    particles = ParticleSystem()
    
    # Game state
    running = True
    clock = pygame.time.Clock()
    
    # Simple player representation
    player = {
        'position': [screen_width // 2, screen_height // 2],
        'velocity': [0, 0],
        'size': 30,
        'health': 100,
        'stamina': 100,
        'color': (255, 0, 0)
    }
    
    # Simple terrain
    terrain = {
        'blocks': [{'x': 0, 'y': screen_height - 50, 'size': screen_width, 'color': (100, 100, 100)}]
    }
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Simple controls for mobile (touch controls would be added later)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player['position'][0] -= 5
        if keys[pygame.K_RIGHT]:
            player['position'][0] += 5
        if keys[pygame.K_UP]:
            player['position'][1] -= 5
        if keys[pygame.K_DOWN]:
            player['position'][1] += 5
        
        # Apply physics
        physics.update_entity_position(player, 0.016, terrain)
        
        # Draw everything
        screen.fill((0, 0, 0))
        
        # Draw terrain
        for block in terrain['blocks']:
            pygame.draw.rect(screen, block['color'], 
                           (block['x'], block['y'], block['size'], 50))
        
        # Draw player
        pygame.draw.circle(screen, player['color'], 
                         (int(player['position'][0]), int(player['position'][1])), 
                         player['size'])
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player['health']}", True, (255, 255, 255))
        screen.blit(health_text, (20, 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    print("Starting Stickman Battle Mobile...")
    mobile_main()
