import pygame
import sys
from config import *
from player import Player
from survival import Survival
from terrain import Terrain
from physics import PhysicsSystem

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Duel - Minecraft Style 1v1")
    
    # Create players
    player1 = Player("Player 1", (100, 100))
    player2 = Player("Player 2", (700, 500))
    
    # Create survival system
    survival = Survival()
    
    # Create terrain with Minecraft-like theme
    terrain = Terrain()
    terrain.change_biome("minecraft")  # Set to Minecraft theme
    
    # Create physics system
    physics = PhysicsSystem()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Block placement/breaking keys
                elif event.key == pygame.K_e:  # Player 1 place block
                    terrain.place_block(player1.position, "dirt")
                elif event.key == pygame.K_r:  # Player 1 break block
                    terrain.break_block(player1.position)
                elif event.key == pygame.K_PERIOD:  # Player 2 place block
                    terrain.place_block(player2.position, "stone")
                elif event.key == pygame.K_SLASH:  # Player 2 break block
                    terrain.break_block(player2.position)
                # Jump keys
                elif event.key == pygame.K_SPACE:  # Player 1 jump
                    physics.handle_jump(player1)
                elif event.key == pygame.K_RETURN:  # Player 2 jump
                    physics.handle_jump(player2)
        
        # Handle player 1 input (WASD)
        keys = pygame.key.get_pressed()
        direction1 = [0, 0]
        if keys[pygame.K_w]:
            direction1[1] = -1
        if keys[pygame.K_s]:
            direction1[1] = 1
        if keys[pygame.K_a]:
            direction1[0] = -1
        if keys[pygame.K_d]:
            direction1[0] = 1
        
        # Handle player 2 input (Arrow keys)
        direction2 = [0, 0]
        if keys[pygame.K_UP]:
            direction2[1] = -1
        if keys[pygame.K_DOWN]:
            direction2[1] = 1
        if keys[pygame.K_LEFT]:
            direction2[0] = -1
        if keys[pygame.K_RIGHT]:
            direction2[0] = 1
        
        # Apply physics
        physics.apply_movement(player1, direction1)
        physics.apply_movement(player2, direction2)
        physics.apply_gravity(player1, terrain)
        physics.apply_gravity(player2, terrain)
        physics.resolve_collision(player1, player2)
        
        # Handle attacks
        if keys[pygame.K_q]:  # Player 1 attack
            player1.attack(player2)
        if keys[pygame.K_SLASH]:  # Player 2 attack
            player2.attack(player1)
        
        # Update game state
        player1.update()
        player2.update()
        survival.update()
        
        # Check for shard collisions
        survival.check_player_collisions(player1)
        survival.check_player_collisions(player2)
        
        # Render
        terrain.draw(screen)
        
        # Draw survival elements (shards)
        survival.draw(screen)
        
        # Draw players
        player1.draw(screen)
        player2.draw(screen)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        text = font.render("Block Duel - Minecraft Style 1v1", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 20))
        
        # Draw health and block info
        health_text = font.render(f"P1 Health: {player1.health}  P2 Health: {player2.health}", True, (255, 255, 255))
        screen.blit(health_text, (20, HEIGHT - 80))
        
        # Draw controls info
        small_font = pygame.font.Font(None, 20)
        controls1 = small_font.render("P1: WASD move, SPACE attack, E place, R break", True, (200, 200, 200))
        controls2 = small_font.render("P2: Arrows move, ENTER attack, . place, / break", True, (200, 200, 200))
        screen.blit(controls1, (20, HEIGHT - 40))
        screen.blit(controls2, (20, HEIGHT - 20))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
