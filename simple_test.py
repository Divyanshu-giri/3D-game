#!/usr/bin/env python3
"""
Simple test to check if imports work
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from unified_stickman_battle.systems.physics import PhysicsSystem
    print("✓ PhysicsSystem imported successfully")
except Exception as e:
    print(f"✗ PhysicsSystem import failed: {e}")

try:
    from unified_stickman_battle.systems.combat import CombatSystem
    print("✓ CombatSystem imported successfully")
except Exception as e:
    print(f"✗ CombatSystem import failed: {e}")

try:
    from unified_stickman_battle.systems.echo_system import EchoSystem
    print("✓ EchoSystem imported successfully")
except Exception as e:
    print(f"✗ EchoSystem import failed: {e}")

try:
    from unified_stickman_battle.systems.particle_system import ParticleSystem
    print("✓ ParticleSystem imported successfully")
except Exception as e:
    print(f"✗ ParticleSystem import failed: {e}")

try:
    from unified_stickman_battle.systems.ai_system import AIManager
    print("✓ AIManager imported successfully")
except Exception as e:
    print(f"✗ AIManager import failed: {e}")

try:
    from unified_stickman_battle.systems.crafting import CraftingSystem
    print("✓ CraftingSystem imported successfully")
except Exception as e:
    print(f"✗ CraftingSystem import failed: {e}")

try:
    from unified_stickman_battle.systems.ui import UIManager
    print("✓ UIManager imported successfully")
except Exception as e:
    print(f"✗ UIManager import failed: {e}")

try:
    from unified_stickman_battle.config import *
    print("✓ Config imported successfully")
except Exception as e:
    print(f"✗ Config import failed: {e}")

print("Simple import test completed")
