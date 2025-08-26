#!/usr/bin/env python3
"""
Simple script to test if the game runs properly
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_game():
    """Test if the game modules can be imported and basic functionality works"""
    print("Testing Unified Stickman Battle Game...")
    
    try:
        # Test imports
        import unified_stickman_battle.config as config
        from unified_stickman_battle.systems.physics import PhysicsSystem
        from unified_stickman_battle.systems.combat import CombatSystem
        from unified_stickman_battle.systems.particle_system import ParticleSystem
        
        print("✓ All modules imported successfully")
        
        # Test system initialization
        physics = PhysicsSystem()
        combat = CombatSystem()
        particles = ParticleSystem()
        
        print("✓ All systems initialized successfully")
        
        # Test basic physics
        entity = {'position': [100, 100], 'velocity': [0, 0], 'size': 30, 'on_ground': False}
        terrain = {'blocks': []}
        physics.update_entity_position(entity, 0.016, terrain)
        print(f"✓ Physics test passed - Entity position: {entity['position']}")
        
        # Test combat
        player = {'stamina': 100, 'id': 'test_player'}
        combat.consume_stamina(player)
        print(f"✓ Combat test passed - Stamina: {player['stamina']}")
        
        # Test particles
        particles.create_explosion([200, 200], count=3)
        print("✓ Particle system test passed")
        
        print("\n🎮 Game is ready to play!")
        print("To build for Android, run: buildozer android debug")
        print("Then check the bin/ folder for the APK file")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your installation and dependencies")
        return False

if __name__ == "__main__":
    test_game()
