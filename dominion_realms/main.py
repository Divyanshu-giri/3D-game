import pygame
import sys
from config import *
from player.movement import PlayerMovement
from player.combat import PlayerCombat
from player.crafting import CraftingSystem
from physics_engine.collision import CollisionSystem
from physics_engine.ragdoll import RagdollSystem
from physics_engine.terrain_deform import TerrainDeformation
from boss.ai import BossAI
from boss.abilities import BossAbilities
from boss.spawn_logic import BossSpawnSystem
from world.biome_generator import BiomeGenerator
from world.resource_nodes import ResourceSystem
from world.destructible_objects import DestructibleSystem
from ui.hud import HUD
from ui.inventory import InventorySystem
from ui.boss_alerts import BossAlertSystem

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dominion Realms - 3D Survival Combat")
    
    # Initialize systems
    collision_system = CollisionSystem()
    ragdoll_system = RagdollSystem()
    terrain_deform = TerrainDeformation()
    biome_generator = BiomeGenerator()
    resource_system = ResourceSystem()
    destructible_system = DestructibleSystem()
    boss_ai = BossAI()
    boss_abilities = BossAbilities()
    boss_spawn = BossSpawnSystem()
    crafting_system = CraftingSystem()
    hud = HUD()
    inventory = InventorySystem()
    boss_alerts = BossAlertSystem()
    
    # Generate world
    biome = biome_generator.generate_biome("volcanic_crater")
    terrain = biome_generator.create_terrain(biome)
    resources = resource_system.spawn_resources(biome)
    destructibles = destructible_system.spawn_objects(biome)
    
    # Create players
    player1_movement = PlayerMovement((100, 100))
    player1_combat = PlayerCombat()
    player1_crafting = CraftingSystem()
    
    player2_movement = PlayerMovement((700, 500))
    player2_combat = PlayerCombat()
    player2_crafting = CraftingSystem()
    
    clock = pygame.time.Clock()
    running = True
    
    # Game state
    game_state = {
        'boss_spawned': False,
        'boss': None,
        'timer': 0,
        'phase': 'scavenge'
    }
    
    while running:
        dt = clock.tick(FPS) / 1000.0
        game_state['timer'] += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Crafting and inventory
                elif event.key == pygame.K_e:
                    crafting_system.open_crafting_menu()
                elif event.key == pygame.K_i:
                    inventory.toggle_inventory()
        
        # Handle player input
        keys = pygame.key.get_pressed()
        
        # Player 1 movement
        direction1 = [0, 0]
        if keys[pygame.K_w]: direction1[1] = -1
        if keys[pygame.K_s]: direction1[1] = 1
        if keys[pygame.K_a]: direction1[0] = -1
        if keys[pygame.K_d]: direction1[0] = 1
        if keys[pygame.K_SPACE]: player1_movement.jump()
        
        # Player 2 movement
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
        
        # Check for boss spawn
        if not game_state['boss_spawned'] and game_state['timer'] > BOSS_SPAWN_TIME:
            game_state['boss'] = boss_spawn.spawn_boss(biome)
            game_state['boss_spawned'] = True
            game_state['phase'] = 'boss_battle'
            boss_alerts.trigger_boss_alert(game_state['boss'].name)
        
        # Update boss if spawned
        if game_state['boss_spawned']:
            boss_ai.update(game_state['boss'], [player1_movement.position, player2_movement.position], dt)
            boss_abilities.activate_abilities(game_state['boss'], terrain, terrain_deform)
        
        # Check resource collection
        resource_system.check_collection(player1_movement.position, player1_crafting)
        resource_system.check_collection(player2_movement.position, player2_crafting)
        
        # Render
        screen.fill((0, 0, 0))
        
        # Draw terrain and environment
        terrain_deform.draw_terrain(screen, terrain)
        resource_system.draw_resources(screen)
        destructible_system.draw_objects(screen)
        
        # Draw players
        player1_movement.draw(screen)
        player2_movement.draw(screen)
        
        # Draw boss if spawned
        if game_state['boss_spawned']:
            boss_ai.draw_boss(screen, game_state['boss'])
        
        # Draw UI
        hud.draw(screen, player1_movement.health, player2_movement.health, 
                game_state['timer'], game_state['phase'])
        inventory.draw(screen)
        boss_alerts.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
