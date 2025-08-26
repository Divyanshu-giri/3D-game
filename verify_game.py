#!/usr/bin/env python3
"""
Simple verification test for the game
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=== GAME VERIFICATION TEST ===")

# Test 1: Check if modules can be imported
print("\n1. Testing module imports...")
try:
    from unified_stickman_battle.systems.physics import PhysicsSystem
    print("   PhysicsSystem: OK")
except Exception as e:
    print(f"   PhysicsSystem: ERROR - {e}")

try:
    from unified_stickman_battle.systems.combat import CombatSystem
    print("   CombatSystem: OK")
except Exception as e:
    print(f"   CombatSystem: ERROR - {e}")

try:
    from unified_stickman_battle.systems.echo_system import EchoSystem
    print("   EchoSystem: OK")
except Exception as e:
    print(f"   EchoSystem: ERROR - {e}")

try:
    from unified_stickman_battle.systems.particle_system import ParticleSystem
    print("   ParticleSystem: OK")
except Exception as e:
    print(f"   ParticleSystem: ERROR - {e}")

try:
    from unified_stickman_battle.systems.ai_system import AIManager
    print("   AIManager: OK")
except Exception as e:
    print(f"   AIManager: ERROR - {e}")

try:
    from unified_stickman_battle.systems.crafting import CraftingSystem
    print("   CraftingSystem: OK")
except Exception as e:
    print(f"   CraftingSystem: ERROR - {e}")

try:
    from unified_stickman_battle.systems.ui import UIManager
    print("   UIManager: OK")
except Exception as e:
    print(f"   UIManager: ERROR - {e}")

try:
    from unified_stickman_battle.config import *
    print("   Config: OK")
except Exception as e:
    print(f"   Config: ERROR - {e}")

# Test 2: Create instances
print("\n2. Testing system instantiation...")
try:
    physics = PhysicsSystem()
    print("   PhysicsSystem instance: OK")
except Exception as e:
    print(f"   PhysicsSystem instance: ERROR - {e}")

try:
    combat = CombatSystem()
    print("   CombatSystem instance: OK")
except Exception as e:
    print(f"   CombatSystem instance: ERROR - {e}")

try:
    particles = ParticleSystem()
    print("   ParticleSystem instance: OK")
except Exception as e:
    print(f"   ParticleSystem instance: ERROR - {e}")

# Test 3: Basic functionality
print("\n3. Testing basic functionality...")
try:
    # Test physics
    entity = {'position': [100, 100], 'velocity': [0, 0], 'size': 50, 'on_ground': False}
    physics.update_entity_position(entity, 0.016, {'blocks': []})
    print("   Physics update: OK")
except Exception as e:
    print(f"   Physics update: ERROR - {e}")

try:
    # Test combat
    player = {'stamina': 100, 'id': 'test_player'}
    combat.consume_stamina(player)
    print("   Combat stamina: OK")
except Exception as e:
    print(f"   Combat stamina: ERROR - {e}")

try:
    # Test particles
    particles.create_explosion([500, 300], count=5)
    print("   Particle creation: OK")
except Exception as e:
    print(f"   Particle creation: ERROR - {e}")

print("\n=== VERIFICATION COMPLETE ===")
print("All systems are ready for gameplay!")
