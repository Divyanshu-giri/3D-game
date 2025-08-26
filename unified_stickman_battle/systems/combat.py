import pygame
import time
import math
import sys
import os

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class CombatSystem:
    def __init__(self):
        self.attack_cooldowns = {}
        self.special_attack_cooldowns = {}
        self.hit_effects = {}
        self.combo_timers = {}
        
    def attack(self, attacker, target, attack_type='basic'):
        """Handle attack between entities"""
        if not attacker or not target:
            return 0
            
        attacker_id = attacker.get('id', 'unknown')
        
        # Check cooldown
        current_time = time.time()
        if attacker_id in self.attack_cooldowns and current_time < self.attack_cooldowns[attacker_id]:
            return 0
            
        # Set cooldown based on attack type
        cooldown = PLAYER_ATTACK_COOLDOWN
        if attack_type == 'special':
            cooldown = 2.0  # Longer cooldown for special attacks
            if attacker_id in self.special_attack_cooldowns and current_time < self.special_attack_cooldowns[attacker_id]:
                return 0
            self.special_attack_cooldowns[attacker_id] = current_time + cooldown
        
        self.attack_cooldowns[attacker_id] = current_time + cooldown
        
        # Calculate damage based on attacker stats
        base_damage = self.calculate_damage(attacker, attack_type)
        
        # Apply armor reduction
        armor_reduction = target.get('armor_reduction', 0)
        actual_damage = max(1, base_damage * (1 - armor_reduction))
        
        # Apply damage
        target['health'] -= actual_damage
        
        # Add hit effect
        self.hit_effects[target.get('id', 'target')] = {
            'start_time': current_time,
            'duration': 0.2,
            'color': (255, 0, 0)
        }
        
        # Handle combo system
        self._update_combo(attacker)
        
        return actual_damage
    
    def calculate_damage(self, attacker, attack_type):
        """Calculate damage based on attacker stats and weapon"""
        base_damage = PLAYER_ATTACK_DAMAGE
        
        # Apply weapon modifiers
        weapon = attacker.get('weapon', 'fists')
        if weapon == 'sword':
            base_damage *= 1.5
        elif weapon == 'nunchaku':
            base_damage *= 1.2
        elif weapon == 'magic_staff':
            base_damage *= 1.8
            
        # Apply level scaling
        level = attacker.get('level', 1)
        base_damage *= (1 + (level - 1) * 0.1)
        
        # Apply attack type modifier
        if attack_type == 'special':
            base_damage *= 2.0
            
        # Apply combo multiplier
        combo = attacker.get('combo', 0)
        if combo > 0:
            base_damage *= (1 + combo * 0.1)
            
        return int(base_damage)
    
    def _update_combo(self, attacker):
        """Update combo counter for attacker"""
        attacker_id = attacker.get('id', 'unknown')
        current_time = time.time()
        
        if attacker_id not in self.combo_timers:
            self.combo_timers[attacker_id] = {'count': 0, 'last_hit': current_time}
        
        combo_data = self.combo_timers[attacker_id]
        
        # Reset combo if too much time has passed
        if current_time - combo_data['last_hit'] > 3.0:
            combo_data['count'] = 0
            
        # Increment combo
        combo_data['count'] += 1
        combo_data['last_hit'] = current_time
        
        # Cap combo at 10
        combo_data['count'] = min(10, combo_data['count'])
        
        attacker['combo'] = combo_data['count']
        
        # Reset combo timer
        if attacker_id in self.combo_timers:
            self.combo_timers[attacker_id] = combo_data
    
    def can_attack(self, attacker):
        """Check if attacker can perform an attack"""
        attacker_id = attacker.get('id', 'unknown')
        current_time = time.time()
        
        if attacker_id in self.attack_cooldowns and current_time < self.attack_cooldowns[attacker_id]:
            return False
            
        # Check stamina
        if attacker.get('stamina', 100) < STAMINA_DRAIN_RATE:
            return False
            
        return True
    
    def can_special_attack(self, attacker):
        """Check if attacker can perform a special attack"""
        attacker_id = attacker.get('id', 'unknown')
        current_time = time.time()
        
        if attacker_id in self.special_attack_cooldowns and current_time < self.special_attack_cooldowns[attacker_id]:
            return False
            
        # Check if special attack is ready
        if not attacker.get('special_attack_ready', False):
            return False
            
        # Check stamina (special attacks cost more)
        if attacker.get('stamina', 100) < STAMINA_DRAIN_RATE * 2:
            return False
            
        return True
    
    def consume_stamina(self, attacker, amount=None):
        """Consume stamina for an action"""
        if amount is None:
            amount = STAMINA_DRAIN_RATE
            
        current_stamina = attacker.get('stamina', 100)
        attacker['stamina'] = max(0, current_stamina - amount)
    
    def regenerate_stamina(self, attacker, dt):
        """Regenerate stamina over time"""
        current_stamina = attacker.get('stamina', 100)
        regen_amount = STAMINA_REGEN_RATE * dt
        attacker['stamina'] = min(100, current_stamina + regen_amount)
    
    def regenerate_health(self, entity, dt):
        """Regenerate health over time"""
        current_health = entity.get('health', 100)
        max_health = entity.get('max_health', 100)
        regen_amount = HEALTH_REGEN_RATE * dt
        entity['health'] = min(max_health, current_health + regen_amount)
    
    def is_in_attack_range(self, attacker, target, range_multiplier=1.0):
        """Check if target is within attack range"""
        attack_range = 100 * range_multiplier  # Base attack range
        
        # Increase range for certain weapons
        weapon = attacker.get('weapon', 'fists')
        if weapon == 'magic_staff':
            attack_range *= 1.5
            
        dx = target['position'][0] - attacker['position'][0]
        dy = target['position'][1] - attacker['position'][1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        return distance <= attack_range
    
    def update(self):
        """Update combat system state"""
        current_time = time.time()
        
        # Clean up expired cooldowns
        self.attack_cooldowns = {k: v for k, v in self.attack_cooldowns.items() if v > current_time}
        self.special_attack_cooldowns = {k: v for k, v in self.special_attack_cooldowns.items() if v > current_time}
        
        # Update hit effects
        self.hit_effects = {k: v for k, v in self.hit_effects.items() 
                           if current_time - v['start_time'] < v['duration']}
        
        # Update combo timers
        for attacker_id, combo_data in list(self.combo_timers.items()):
            if current_time - combo_data['last_hit'] > 3.0:
                del self.combo_timers[attacker_id]
    
    def get_hit_effect(self, entity_id):
        """Get current hit effect for an entity"""
        return self.hit_effects.get(entity_id, None)
    
    def reset_combo(self, attacker_id):
        """Reset combo for an attacker"""
        if attacker_id in self.combo_timers:
            del self.combo_timers[attacker_id]
