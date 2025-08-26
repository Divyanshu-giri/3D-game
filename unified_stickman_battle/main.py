import sys
import pygame
from systems.physics import PhysicsSystem
from systems.combat import CombatSystem
# from systems.crafting import CraftingSystem  # Will be implemented later
# from systems.echo_system import EchoSystem    # Will be implemented later  
# from systems.particle_system import ParticleSystem  # Will be implemented later
# from systems.ai_system import AIManager       # Will be implemented later

def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Unified Stickman Battle")
    clock = pygame.time.Clock()
    
    # Initialize game systems
    physics_system = PhysicsSystem()
    combat_system = CombatSystem()
    # crafting_system = CraftingSystem()
    # echo_system = EchoSystem()
    # particle_system = ParticleSystem()
    # ai_manager = AIManager()

    # Game loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update systems
        physics_system.update()
        combat_system.update()
        # crafting_system.update()
        # echo_system.update()
        # particle_system.update()
        # ai_manager.update()

        # Clear screen
        screen.fill((0, 0, 0))
        
        # Render game elements here
        # TODO: Add rendering logic
        
        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
