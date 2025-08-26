import pygame
import sys
import asyncio
from config import *

# Web-specific imports
try:
    import pygbag
    IS_WEB = True
except ImportError:
    IS_WEB = False

async def main():
    pygame.init()
    
    if IS_WEB:
        # Web-specific setup
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
    pygame.display.set_caption("Dominion Realms - Web Edition")
    
    # Import game modules (web-safe)
    from player.movement import PlayerMovement
    from player.combat import PlayerCombat
    from player.crafting import CraftingSystem
    from physics_engine.collision import CollisionSystem
    from world.biome_generator import BiomeGenerator
    from world.resource_nodes import ResourceSystem
    from ui.hud import HUD
    
    # Initialize systems
    collision_system = CollisionSystem()
    biome_generator = BiomeGenerator()
    resource_system = ResourceSystem()
    hud = HUD()
    
    # Generate world
    biome = biome_generator.generate_biome("volcanic_crater")
    terrain = biome_generator.create_terrain(biome)
    resources = resource_system.spawn_resources(biome)
    
    # Create players
    player1_movement = PlayerMovement((100, 100))
    player1_combat = PlayerCombat()
    player1_crafting = CraftingSystem()
    
    player2_movement = PlayerMovement((700, 500))
    player2_combat = PlayerCombat()
    player2_crafting = CraftingSystem()
    
    clock = pygame.time.Clock()
    running = True
    
    # Web-specific variables
    last_time = pygame.time.get_ticks()
    
    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000.0
        last_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Web-friendly controls
                elif event.key == pygame.K_e:
                    player1_crafting.open_crafting_menu()
                elif event.key == pygame.K_i:
                    pass  # Inventory would go here
        
        # Get keyboard state (web-safe)
        keys = pygame.key.get_pressed()
        
        # Player 1 movement (WASD)
        direction1 = [0, 0]
        if keys[pygame.K_w]: direction1[1] = -1
        if keys[pygame.K_s]: direction1[1] = 1
        if keys[pygame.K_a]: direction1[0] = -1
        if keys[pygame.K_d]: direction1[0] = 1
        if keys[pygame.K_SPACE]: player1_movement.jump()
        
        # Player 2 movement (Arrow keys)
        direction2 = [0, 0]
        if keys[pygame.K_UP]: direction2[1] = -1
        if keys[pygame.K_DOWN]: direction2[1] = 1
        if keys[pygame.K_LEFT]: direction2[0] = -1
        if keys[pygame.K_RIGHT]: direction2[0] = 1
        if keys[pygame.K_RETURN]: player2_movement.jump()
        
        # Apply physics and movement
        player1_movement.update(direction1, dt, terrain, collision_system)
        player2_movement.update(direction2, dt, terrain, collision_system)
        
        # Handle combat
        if keys[pygame.K_q]: player1_combat.attack(player2_movement.position)
        if keys[pygame.K_SLASH]: player2_combat.attack(player1_movement.position)
        
        # Check resource collection
        resource_system.check_collection(player1_movement.position, player1_crafting)
        resource_system.check_collection(player2_movement.position, player2_crafting)
        
        # Update resource system
        resource_system.update_resources(current_time / 1000.0)
        
        # Render
        screen.fill((0, 0, 0))
        
        # Draw terrain and environment
        biome_generator.draw_terrain(screen, terrain)
        resource_system.draw_resources(screen)
        
        # Draw players
        player1_movement.draw(screen)
        player2_movement.draw(screen)
        
        # Draw UI
        hud.draw(screen, player1_movement.health, player2_movement.health, 
                0, 'scavenge')  # Simplified for web
        
        pygame.display.flip()
        
        # Web-specific: yield to browser
        if IS_WEB:
            await asyncio.sleep(0)
        else:
            clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

# Web entry point
if __name__ == "__main__":
    if IS_WEB:
        asyncio.run(main())
    else:
        asyncio.run(main())
