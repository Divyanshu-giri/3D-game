import random
from config import *

class BossAbilities:
    def __init__(self):
        self.ability_cooldowns = {ability: 0 for ability in ABILITY_EFFECTS.keys()}

    def activate_abilities(self, boss, terrain, terrain_deform):
        current_time = pygame.time.get_ticks() / 1000.0
        
        for ability in boss.abilities:
            if current_time - self.ability_cooldowns[ability] >= ABILITY_EFFECTS[ability]['cooldown']:
                if random.random() < 0.1:  # 10% chance to use ability each frame
                    self.use_ability(ability, boss, terrain, terrain_deform)
                    self.ability_cooldowns[ability] = current_time

    def use_ability(self, ability_name, boss, terrain, terrain_deform):
        effect = ABILITY_EFFECTS[ability_name]
        
        if ability_name == 'lava_pool':
            # Create a lava pool at boss position
            terrain_deform.create_lava_pool(boss.position, effect['duration'])
            print(f"Boss used Lava Pool at {boss.position}")
            
        elif ability_name == 'meteor_shower':
            # Create multiple meteor impacts
            for _ in range(3):
                pos = [boss.position[0] + random.randint(-200, 200), 
                       boss.position[1] + random.randint(-200, 200)]
                terrain_deform.create_crater(pos, effect['duration'])
                print(f"Boss used Meteor Shower at {pos}")
                
        elif ability_name == 'earthquake':
            # Create earthquake effect across terrain
            terrain_deform.apply_earthquake(effect['duration'])
            print("Boss used Earthquake")
            
        elif ability_name == 'crystal_spikes':
            # Create crystal spikes around boss
            for angle in range(0, 360, 45):
                pos = [boss.position[0] + 100 * math.cos(math.radians(angle)),
                       boss.position[1] + 100 * math.sin(math.radians(angle))]
                terrain_deform.create_crystal_spike(pos, effect['duration'])
                print(f"Boss used Crystal Spikes at {pos}")
                
        elif ability_name == 'energy_beam':
            # Create energy beam in direction of players
            print("Boss used Energy Beam")
            
        elif ability_name == 'teleport':
            # Teleport boss to random position
            boss.position = [random.randint(100, 700), random.randint(100, 500)]
            print(f"Boss teleported to {boss.position}")
            
        elif ability_name == 'wind_gust':
            # Create wind gust effect
            terrain_deform.apply_wind_gust(effect['duration'])
            print("Boss used Wind Gust")
            
        elif ability_name == 'lightning_strike':
            # Create lightning strike at random position
            pos = [random.randint(100, 700), random.randint(100, 500)]
            terrain_deform.create_lightning_strike(pos, effect['duration'])
            print(f"Boss used Lightning Strike at {pos}")
            
        elif ability_name == 'aerial_assault':
            # Boss jumps and lands with impact
            print("Boss used Aerial Assault")
