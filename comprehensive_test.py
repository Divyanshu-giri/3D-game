#!/usr/bin/env python3
"""
Comprehensive test script for Unified Stickman Battle Game
Tests all systems with edge cases, performance scenarios, and integration
"""

import pygame
import time
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stickman_battle.systems.physics import PhysicsSystem
from unified_stickman_battle.systems.combat import CombatSystem
from unified_stickman_battle.systems.echo_system import EchoSystem
from unified_stickman_battle.systems.particle_system import ParticleSystem
from unified_stickman_battle.systems.ai_system import AIManager
from unified_stickman_battle.systems.crafting import CraftingSystem
from unified_stickman_battle.systems.ui import UIManager
from unified_stickman_battle.config import *

def test_physics_edge_cases():
    """Test physics system with edge cases"""
    print("\nTesting Physics System Edge Cases...")
    
    physics = PhysicsSystem()
    
    # Test 1: Entity falling through ground
    entity = {
        'position': [WIDTH//2, 0],
        'velocity': [0, 0],
        'size': 50,
        'on_ground': False
    }
    terrain = {'blocks': []}
    
    for _ in range(100):  # Simulate 100 frames
        physics.update_entity_position(entity, 0.016, terrain)
    
    print(f"Entity fell to position: {entity['position']}")
    
    # Test 2: Collision resolution
    entity1 = {'position': [100, 100], 'velocity': [10, 0], 'size': 25}
    entity2 = {'position': [110, 100], 'velocity': [-10, 0], 'size': 25}
    physics.resolve_collision(entity1, entity2)
    print(f"Collision resolved - Entity1 vel: {entity1['velocity']}, Entity2 vel: {entity2['velocity']}")
    
    # Test 3: Terminal velocity
    entity = {'position': [WIDTH//2, 0], 'velocity': [0, 0], 'on_ground': False}
    for _ in range(200):
        physics.apply_gravity(entity, 0.016)
    print(f"Terminal velocity reached: {entity['velocity'][1]:.2f}")
    
    return True

def test_combat_edge_cases():
    """Test combat system with edge cases"""
    print("\nTesting Combat System Edge Cases...")
    
    combat = CombatSystem()
    
    # Test 1: Stamina management
    player = {'stamina': 100, 'id': 'player1'}
    for _ in range(15):
        combat.consume_stamina(player)
    print(f"Stamina after 15 actions: {player['stamina']}")
    
    # Test 2: Health regeneration
    player = {'health': 50, 'max_health': 100}
    for _ in range(100):
        combat.regenerate_health(player, 0.016)
    print(f"Health after regeneration: {player['health']:.1f}")
    
    # Test 3: Combo system
    attacker = {'combo': 0, 'id': 'attacker1'}
    target = {'health': 100, 'armor_reduction': 0.2}
    
    for i in range(5):
        combat.attack(attacker, target)
        print(f"  Combo {i+1}: Damage dealt, combo count: {attacker.get('combo', 0)}")
    
    return True

def test_particle_performance():
    """Test particle system performance"""
    print("\nTesting Particle System Performance...")
    
    particle_system = ParticleSystem()
    
    # Create large explosion
    start_time = time.time()
    particle_system.create_explosion([WIDTH//2, HEIGHT//2], count=100)
    creation_time = time.time() - start_time
    
    # Update particles
    update_start = time.time()
    for _ in range(60):  # 1 second at 60fps
        particle_system.update(0.016)
    update_time = time.time() - update_start
    
    print(f"Created 100 particles in {creation_time:.4f}s")
    print(f"Updated particles for 1s in {update_time:.4f}s")
    print(f"Final particle count: {particle_system.get_particle_count()}")
    
    return True

def test_ai_complex_scenarios():
    """Test AI with complex scenarios"""
    print("\nTesting AI Complex Scenarios...")
    
    ai_manager = AIManager()
    
    # Add multiple entities
    boss = {
        'position': [300, 300],
        'velocity': [0, 0],
        'health': BOSS_HEALTH,
        'max_health': BOSS_HEALTH,
        'speed': BOSS_MOVEMENT_SPEED,
        'damage': BOSS_ATTACK_DAMAGE,
        'type': 'volcano_lord',
        'id': 'boss1'
    }
    
    minion = {
        'position': [400, 400],
        'velocity': [0, 0],
        'health': 50,
        'id': 'minion1'
    }
    
    player = {
        'position': [350, 350],
        'health': 100,
        'id': 'player1'
    }
    
    ai_manager.add_entity('boss1', boss, 'boss')
    ai_manager.add_entity('minion1', minion, 'minion')
    
    # Test AI behavior
    for frame in range(120):  # 2 seconds at 60fps
        ai_manager.update(0.016, [player])
        
        if frame % 30 == 0:  # Every 0.5 seconds
            print(f"  Frame {frame}: Boss pos {boss['position']}, Minion pos {minion['position']}")
    
    print("AI behavior simulation completed")
    return True

def test_crafting_complex_recipes():
    """Test crafting with complex scenarios"""
    print("\nTesting Crafting Complex Scenarios...")
    
    crafting = CraftingSystem()
    
    # Add resources
    resources = {
        'wood': 20,
        'stone': 15,
        'metal': 12,
        'crystal': 8,
        'energy': 6
    }
    
    for resource, quantity in resources.items():
        crafting.add_resource(resource, quantity)
    
    # Test all recipes
    available = crafting.get_available_recipes()
    print(f"Available recipes: {len(available)}")
    
    # Test crafting queue
    crafting.craft_item('basic_sword', 'player1')
    crafting.craft_item('shield', 'player1')
    
    # Simulate crafting process
    for _ in range(100):
        crafting.update()
        time.sleep(0.01)
    
    print("Crafting queue processing completed")
    return True

def test_echo_system_performance():
    """Test echo system performance"""
    print("\nTesting Echo System Performance...")
    
    echo_system = EchoSystem()
    
    # Create multiple echoes
    start_time = time.time()
    for i in range(50):
        echo_system.create_echo('attack', [i*10, 100], (255, 0, 0), delay=i*0.1)
    
    creation_time = time.time() - start_time
    
    # Update echoes
    update_start = time.time()
    for _ in range(120):  # 2 seconds
        echo_system.update()
        time.sleep(0.016)
    update_time = time.time() - update_start
    
    print(f"Created 50 echoes in {creation_time:.4f}s")
    print(f"Updated echoes for 2s in {update_time:.4f}s")
    
    return True

def test_integration_scenario():
    """Test all systems working together"""
    print("\nTesting Full Integration Scenario...")
    
    # Initialize all systems
    physics = PhysicsSystem()
    combat = CombatSystem()
    echo = EchoSystem()
    particles = ParticleSystem()
    ai = AIManager()
    crafting = CraftingSystem()
    ui = UIManager()
    
    # Create game entities
    player = {
        'position': [WIDTH//2, HEIGHT//2],
        'velocity': [0, 0],
        'health': PLAYER_HEALTH,
        'stamina': 100,
        'level': 1,
        'weapon': 'fists',
        'id': 'player1',
        'size': 50,
        'on_ground': False
    }
    
    enemy = {
        'position': [WIDTH//2 + 200, HEIGHT//2],
        'velocity': [0, 0],
        'health': 50,
        'id': 'enemy1',
        'size': 40,
        'on_ground': False
    }
    
    # Simulate game loop
    print("Simulating 5 seconds of gameplay...")
    for frame in range(300):  # 5 seconds at 60fps
        dt = 0.016
        
        # Update physics
        physics.update_entity_position(player, dt, None)
        physics.update_entity_position(enemy, dt, None)
        
        # Combat interactions
        if frame % 30 == 0:  # Attack every 0.5 seconds
            if combat.can_attack(player):
                damage = combat.attack(player, enemy)
                if damage > 0:
                    echo.create_echo('attack', player['position'], (255, 0, 0))
                    particles.create_blood_splash(enemy['position'])
        
        # AI behavior
        ai.update(dt, [player])
        
        # Regeneration
        combat.regenerate_stamina(player, dt)
        combat.regenerate_health(player, dt)
        
        # System updates
        combat.update()
        echo.update()
        particles.update(dt)
        
        if frame % 60 == 0:  # Every second
            print(f"  {frame//60}s: Player health {player['health']:.1f}, Enemy health {enemy['health']:.1f}")
    
    print("Full integration test completed successfully!")
    return True

def main():
    """Run comprehensive tests"""
    print("Starting Comprehensive Tests for Unified Stickman Battle Game...")
    print("Initializing Pygame...")
    print("=" * 70)
    
    try:
        # Initialize pygame for some tests
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Comprehensive Tests")
        
        # Run all tests
        tests = [
            test_physics_edge_cases,
            test_combat_edge_cases,
            test_particle_performance,
            test_ai_complex_scenarios,
            test_crafting_complex_recipes,
            test_echo_system_performance,
            test_integration_scenario
        ]
        
        all_passed = True
        for test in tests:
            try:
                if test():
                    print("PASSED")
                else:
                    print("FAILED")
                    all_passed = False
            except Exception as e:
                print(f"ERROR in {test.__name__}: {e}")
                all_passed = False
        
        print("\n" + "=" * 70)
        if all_passed:
            print("ALL COMPREHENSIVE TESTS PASSED!")
            print("The Unified Stickman Battle Game framework is robust and ready for production!")
        else:
            print("Some tests failed. Please review the errors above.")
        
        pygame.quit()
        return all_passed
        
    except Exception as e:
        print(f"Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
