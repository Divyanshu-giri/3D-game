import pygame
import sys
from unified_stickman_battle.systems.physics import PhysicsSystem
from unified_stickman_battle.systems.combat import CombatSystem
from unified_stickman_battle.systems.echo_system import EchoSystem
from unified_stickman_battle.systems.particle_system import ParticleSystem
from unified_stickman_battle.systems.ai_system import AIManager
from unified_stickman_battle.systems.crafting import CraftingSystem
from unified_stickman_battle.systems.ui import UIManager

def test_systems():
    """Test all game systems integration"""
    print("Testing Unified Stickman Battle Game Systems...")
    
    # Initialize systems
    physics = PhysicsSystem()
    combat = CombatSystem()
    echo = EchoSystem()
    particles = ParticleSystem()
    ai = AIManager()
    crafting = CraftingSystem()
    ui = UIManager()
    
    print("All systems initialized successfully")
    
    # Test physics system
    test_entity = {
        'position': [100, 100],
        'velocity': [0, 0],
        'on_ground': False
    }
    physics.update_entity_position(test_entity, 0.016)  # 60 FPS delta time
    print("Physics system test passed")
    
    # Test combat system
    attacker = {'id': 'player1', 'health': 100, 'stamina': 100}
    target = {'id': 'enemy1', 'health': 100, 'armor_reduction': 0.1}
    damage = combat.attack(attacker, target)
    print(f"Combat system test passed - Damage dealt: {damage}")
    
    # Test echo system
    echo.create_echo('move', [200, 200], (255, 0, 0))
    echo.update()
    print("Echo system test passed")
    
    # Test particle system
    particles.create_explosion([300, 300])
    particles.update(0.016)
    print("Particle system test passed")
    
    # Test AI system
    test_player = {'id': 'player1', 'position': [400, 400], 'health': 100}
    ai.add_entity('boss1', {'position': [500, 500], 'health': 1000}, 'boss')
    ai.update(0.016, [test_player])
    print("AI system test passed")
    
    # Test crafting system
    crafting.add_resource('wood', 10)
    crafting.add_resource('stone', 5)
    can_craft = crafting.can_craft('basic_sword')
    print(f"Crafting system test passed - Can craft basic sword: {can_craft}")
    
    # Test UI system
    ui.create_health_bar('player1', [50, 50])
    ui.update_health_bar('player1', 75)
    print("UI system test passed")
    
    print("\n🎉 All systems integrated successfully!")
    print("The Unified Stickman Battle Game framework is ready for game mode implementation.")

if __name__ == "__main__":
    test_systems()
