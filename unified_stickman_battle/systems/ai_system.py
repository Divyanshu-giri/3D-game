import pygame
import random
import math
import time
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class AIManager:
    def __init__(self):
        self.entities = {}
        self.bosses = {}
        self.minions = {}
        self.behavior_timers = {}
        self.target_positions = {}
        
    def add_entity(self, entity_id, entity_data, entity_type='enemy'):
        """Add an AI-controlled entity"""
        entity_data['ai_state'] = 'idle'
        entity_data['ai_timer'] = 0
        entity_data['target_id'] = None
        
        if entity_type == 'boss':
            self.bosses[entity_id] = entity_data
        elif entity_type == 'minion':
            self.minions[entity_id] = entity_data
        else:
            self.entities[entity_id] = entity_data
            
    def remove_entity(self, entity_id):
        """Remove an AI-controlled entity"""
        if entity_id in self.entities:
            del self.entities[entity_id]
        if entity_id in self.bosses:
            del self.bosses[entity_id]
        if entity_id in self.minions:
            del self.minions[entity_id]
            
    def update_boss_behavior(self, boss_id, players, dt):
        """Update boss AI behavior"""
        if boss_id not in self.bosses:
            return
            
        boss = self.bosses[boss_id]
        boss['ai_timer'] += dt
        
        # Find closest player
        closest_player = None
        min_distance = float('inf')
        
        for player in players:
            dx = player['position'][0] - boss['position'][0]
            dy = player['position'][1] - boss['position'][1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < min_distance:
                min_distance = distance
                closest_player = player
                boss['target_id'] = player.get('id', None)
        
        if not closest_player:
            return
            
        # Boss behavior states
        if boss['ai_state'] == 'idle':
            if min_distance < 400:  # Aggro range
                boss['ai_state'] = 'chase'
                boss['ai_timer'] = 0
                
        elif boss['ai_state'] == 'chase':
            # Move towards player
            dx = closest_player['position'][0] - boss['position'][0]
            dy = closest_player['position'][1] - boss['position'][1]
            distance = max(0.1, math.sqrt(dx*dx + dy*dy))
            
            if distance > 50:  # Stop at attack range
                speed = boss.get('speed', BOSS_MOVEMENT_SPEED) * dt
                boss['velocity'][0] = (dx / distance) * speed
                boss['velocity'][1] = (dy / distance) * speed
            else:
                boss['velocity'][0] = 0
                boss['velocity'][1] = 0
                
            # Check for ability usage
            if boss['ai_timer'] >= BOSS_ABILITY_COOLDOWN:
                self._use_boss_ability(boss_id, closest_player)
                boss['ai_timer'] = 0
                
            # Switch to attack if close enough
            if min_distance < 100:
                boss['ai_state'] = 'attack'
                boss['ai_timer'] = 0
                
        elif boss['ai_state'] == 'attack':
            # Attack player
            if boss['ai_timer'] >= BOSS_ATTACK_COOLDOWN:
                self._perform_boss_attack(boss_id, closest_player)
                boss['ai_timer'] = 0
                
            # Switch back to chase if player moves away
            if min_distance > 150:
                boss['ai_state'] = 'chase'
                boss['ai_timer'] = 0
                
        elif boss['ai_state'] == 'flee':
            # Flee from player when low health
            if boss['health'] > boss.get('max_health', BOSS_HEALTH) * 0.3:
                boss['ai_state'] = 'chase'
            else:
                dx = boss['position'][0] - closest_player['position'][0]
                dy = boss['position'][1] - closest_player['position'][1]
                distance = max(0.1, math.sqrt(dx*dx + dy*dy))
                
                speed = boss.get('speed', BOSS_MOVEMENT_SPEED) * dt * 1.2
                boss['velocity'][0] = (dx / distance) * speed
                boss['velocity'][1] = (dy / distance) * speed
                
    def _use_boss_ability(self, boss_id, target):
        """Use boss special ability"""
        boss = self.bosses[boss_id]
        boss_type = boss.get('type', 'volcano_lord')
        
        if boss_type in BOSS_TYPES:
            abilities = BOSS_TYPES[boss_type]['abilities']
            if abilities:
                ability = random.choice(abilities)
                print(f"Boss {boss_id} uses {ability}!")
                
                # TODO: Implement specific ability effects
                return ability
        return None
        
    def _perform_boss_attack(self, boss_id, target):
        """Perform boss basic attack"""
        boss = self.bosses[boss_id]
        
        # Check if target is in range
        dx = target['position'][0] - boss['position'][0]
        dy = target['position'][1] - boss['position'][1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance <= 100:  # Attack range
            damage = boss.get('damage', BOSS_ATTACK_DAMAGE)
            target['health'] -= damage
            print(f"Boss {boss_id} attacks for {damage} damage!")
            
    def update_minion_behavior(self, minion_id, players, dt):
        """Update minion AI behavior"""
        if minion_id not in self.minions:
            return
            
        minion = self.minions[minion_id]
        minion['ai_timer'] += dt
        
        # Find closest player
        closest_player = None
        min_distance = float('inf')
        
        for player in players:
            dx = player['position'][0] - minion['position'][0]
            dy = player['position'][1] - minion['position'][1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < min_distance:
                min_distance = distance
                closest_player = player
                minion['target_id'] = player.get('id', None)
        
        if not closest_player:
            return
            
        # Simple minion behavior: chase and attack
        if min_distance > 80:  # Chase
            dx = closest_player['position'][0] - minion['position'][0]
            dy = closest_player['position'][1] - minion['position'][1]
            distance = max(0.1, math.sqrt(dx*dx + dy*dy))
            
            speed = 200 * dt  # Minion speed
            minion['velocity'][0] = (dx / distance) * speed
            minion['velocity'][1] = (dy / distance) * speed
        else:  # Attack
            minion['velocity'][0] = 0
            minion['velocity'][1] = 0
            
            if minion['ai_timer'] >= 1.0:  # Attack every second
                damage = 5  # Minion damage
                closest_player['health'] -= damage
                minion['ai_timer'] = 0
                print(f"Minion {minion_id} attacks for {damage} damage!")
                
    def update_enemy_behavior(self, entity_id, players, dt):
        """Update generic enemy behavior"""
        if entity_id not in self.entities:
            return
            
        entity = self.entities[entity_id]
        entity['ai_timer'] += dt
        
        # Simple wandering behavior for generic enemies
        if entity['ai_state'] == 'idle':
            if entity['ai_timer'] >= 2.0:  # Change direction every 2 seconds
                entity['velocity'][0] = random.uniform(-1, 1) * 100 * dt
                entity['velocity'][1] = random.uniform(-1, 1) * 100 * dt
                entity['ai_timer'] = 0
                
        # Check for players nearby
        for player in players:
            dx = player['position'][0] - entity['position'][0]
            dy = player['position'][1] - entity['position'][1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 200:  # Aggro range
                entity['ai_state'] = 'chase'
                entity['target_id'] = player.get('id', None)
                break
                
        if entity['ai_state'] == 'chase' and entity['target_id']:
            # Find the target player
            target = None
            for player in players:
                if player.get('id') == entity['target_id']:
                    target = player
                    break
                    
            if target:
                dx = target['position'][0] - entity['position'][0]
                dy = target['position'][1] - entity['position'][1]
                distance = max(0.1, math.sqrt(dx*dx + dy*dy))
                
                if distance > 50:  # Chase
                    speed = 150 * dt
                    entity['velocity'][0] = (dx / distance) * speed
                    entity['velocity'][1] = (dy / distance) * speed
                else:  # Attack
                    entity['velocity'][0] = 0
                    entity['velocity'][1] = 0
                    
                    if entity['ai_timer'] >= 1.5:  # Attack cooldown
                        damage = 8
                        target['health'] -= damage
                        entity['ai_timer'] = 0
                        print(f"Enemy {entity_id} attacks for {damage} damage!")
            else:
                entity['ai_state'] = 'idle'
                entity['target_id'] = None
                
    def update(self, dt, players):
        """Update all AI entities"""
        # Update bosses
        for boss_id in list(self.bosses.keys()):
            self.update_boss_behavior(boss_id, players, dt)
            
        # Update minions
        for minion_id in list(self.minions.keys()):
            self.update_minion_behavior(minion_id, players, dt)
            
        # Update generic enemies
        for entity_id in list(self.entities.keys()):
            self.update_enemy_behavior(entity_id, players, dt)
            
    def get_entity_count(self):
        """Get total number of AI entities"""
        return len(self.entities) + len(self.bosses) + len(self.minions)
        
    def clear(self):
        """Clear all AI entities"""
        self.entities.clear()
        self.bosses.clear()
        self.minions.clear()
        self.behavior_timers.clear()
        self.target_positions.clear()
