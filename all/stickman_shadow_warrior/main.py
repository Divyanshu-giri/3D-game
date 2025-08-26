import pygame
import sys
import random
import math
from config import *

class ShadowWarrior:
    def __init__(self, name, position, color):
        self.name = name
        self.position = list(position)
        self.velocity = [0, 0]
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.color = color
        self.size = 20
        self.attack_cooldown = 0
        self.facing_right = True
        self.is_jumping = False
        self.on_ground = False
        self.attack_animation = 0
        self.hit_animation = 0
        self.level = 1
        self.experience = 0
        self.weapon = "Fists"
        self.armor = "Basic"
        self.special_attack_ready = False
        self.special_attack_cooldown = 0
        
    def move(self, direction):
        self.velocity[0] = direction[0] * 5
        if direction[0] > 0:
            self.facing_right = True
        elif direction[0] < 0:
            self.facing_right = False
            
    def jump(self):
        if self.on_ground and not self.is_jumping:
            self.velocity[1] = -12
            self.is_jumping = True
            self.on_ground = False
            
    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 15
            self.attack_animation = 8
            return True
        return False
        
    def special_attack(self):
        if self.special_attack_ready and self.special_attack_cooldown <= 0:
            self.special_attack_cooldown = 60
            self.special_attack_ready = False
            self.attack_animation = 15
            return True
        return False
        
    def take_damage(self, amount):
        # Armor reduces damage
        damage_reduction = 0
        if self.armor == "Basic":
            damage_reduction = 0.1
        elif self.armor == "Advanced":
            damage_reduction = 0.3
        elif self.armor == "Epic":
            damage_reduction = 0.5
            
        actual_damage = amount * (1 - damage_reduction)
        self.health -= actual_damage
        self.hit_animation = 15
        
        if self.health <= 0:
            self.health = 0
            return True
        return False
        
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 20
        self.health = self.max_health
        self.special_attack_ready = True
        
    def equip_weapon(self, weapon_type):
        self.weapon = weapon_type
        
    def equip_armor(self, armor_type):
        self.armor = armor_type
        
    def get_attack_damage(self):
        base_damage = 10
        if self.weapon == "Sword":
            base_damage = 15
        elif self.weapon == "Nunchaku":
            base_damage = 12
        elif self.weapon == "Magic Staff":
            base_damage = 18
            
        if self.special_attack_cooldown > 50:  # Special attack active
            return base_damage * 2
        return base_damage
        
    def update(self):
        # Apply gravity
        self.velocity[1] += 0.5
        
        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Boundary checking
        self.position[0] = max(0, min(WIDTH - self.size, self.position[0]))
        
        # Ground collision
        if self.position[1] >= HEIGHT - 50 - self.size:
            self.position[1] = HEIGHT - 50 - self.size
            self.velocity[1] = 0
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False
                
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
            if self.special_attack_cooldown == 30:  # Halfway through cooldown
                self.special_attack_ready = True
                
        # Update animations
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
        # Recover stamina
        self.stamina = min(100, self.stamina + 0.5)
            
    def draw(self, screen):
        center_x = self.position[0] + self.size // 2
        center_y = self.position[1] + self.size // 2
        
        # Apply hit animation
        draw_color = self.color
        if self.hit_animation > 0:
            draw_color = (255, 100, 100)
            
        # Draw armor based on type
        if self.armor != "Basic":
            armor_color = (150, 150, 150)
            if self.armor == "Advanced":
                armor_color = (100, 100, 200)
            elif self.armor == "Epic":
                armor_color = (200, 100, 200)
                
            pygame.draw.circle(screen, armor_color, (center_x, center_y - 10), 10)
            pygame.draw.rect(screen, armor_color, (center_x - 8, center_y - 2, 16, 20))
        
        # Head
        pygame.draw.circle(screen, draw_color, (center_x, center_y - 10), 8)
        
        # Body
        pygame.draw.line(screen, draw_color, (center_x, center_y - 2), (center_x, center_y + 15), 3)
        
        # Arms with weapon animation
        if self.attack_animation > 0:
            # Attack animation
            attack_range = 25 + (self.attack_animation * 2)
            arm_x = center_x + math.cos(math.radians(0 if self.facing_right else 180)) * attack_range
            arm_y = center_y + 5 + math.sin(math.radians(0 if self.facing_right else 180)) * attack_range
            pygame.draw.line(screen, draw_color, (center_x, center_y + 5), (arm_x, arm_y), 4)
            
            # Draw weapon
            if self.weapon != "Fists":
                weapon_color = (200, 200, 200)
                if self.weapon == "Sword":
                    pygame.draw.rect(screen, weapon_color, (arm_x - 2, arm_y - 10, 15, 3))
                elif self.weapon == "Nunchaku":
                    pygame.draw.circle(screen, weapon_color, (arm_x, arm_y), 5)
                    pygame.draw.circle(screen, weapon_color, (arm_x + 10, arm_y), 5)
                elif self.weapon == "Magic Staff":
                    pygame.draw.circle(screen, (100, 100, 255), (arm_x, arm_y), 8)
        else:
            # Normal arms
            arm_angle = 45 if self.facing_right else 135
            arm_x = center_x + math.cos(math.radians(arm_angle)) * 15
            arm_y = center_y + 5 + math.sin(math.radians(arm_angle)) * 15
            pygame.draw.line(screen, draw_color, (center_x, center_y + 5), (arm_x, arm_y), 3)
        
        # Legs
        pygame.draw.line(screen, draw_color, (center_x, center_y + 15), (center_x - 8, center_y + 30), 3)
        pygame.draw.line(screen, draw_color, (center_x, center_y + 15), (center_x + 8, center_y + 30), 3)
        
        # Health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0] - 15, self.position[1] - 25, 50, 6))
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - 15, self.position[1] - 25, 50 * (self.health / self.max_health), 6))
        
        # Level indicator
        font = pygame.font.Font(None, 16)
        level_text = font.render(f"Lvl {self.level}", True, (255, 255, 0))
        screen.blit(level_text, (self.position[0] - 10, self.position[1] - 40))

class ShadowRealm:
    def __init__(self):
        self.blocks = []
        self.generate_realm()
        
    def generate_realm(self):
        # Create dark ground
        for x in range(0, WIDTH, 30):
            self.blocks.append({
                'x': x,
                'y': HEIGHT - 50,
                'size': 30,
                'type': 'shadow_stone',
                'color': (50, 50, 70)
            })
            
        # Add shadow realm obstacles
        for _ in range(15):
            block_type = random.choice(['dark_crystal', 'obsidian', 'shadow_rock'])
            colors = {
                'dark_crystal': (80, 20, 120),
                'obsidian': (30, 30, 40),
                'shadow_rock': (60, 60, 80)
            }
            self.blocks.append({
                'x': random.randint(50, WIDTH - 80),
                'y': random.randint(100, HEIGHT - 100),
                'size': 30,
                'type': block_type,
                'color': colors[block_type]
            })
        
    def draw(self, screen):
        # Draw dark background
        screen.fill((20, 20, 40))  # Dark purple/blue
        
        # Draw blocks with glow effect
        for block in self.blocks:
            pygame.draw.rect(screen, block['color'], 
                           (block['x'], block['y'], block['size'], block['size']))
            
            # Add glow effect for crystals
            if block['type'] == 'dark_crystal':
                glow_color = (120, 40, 180, 100)
                glow_surface = pygame.Surface((block['size'] + 10, block['size'] + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, glow_color, (0, 0, block['size'] + 10, block['size'] + 10))
                screen.blit(glow_surface, (block['x'] - 5, block['y'] - 5))

def show_game_over(screen, winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 72)
    text = font.render(f"{winner} WINS!", True, (255, 255, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    small_font = pygame.font.Font(None, 36)
    restart_text = small_font.render("Press R to restart or ESC to quit", True, (200, 200, 200))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
    pygame.display.flip()

def show_stats(screen, player1, player2):
    font = pygame.font.Font(None, 24)
    
    # Player 1 stats
    p1_stats = [
        f"P1: Lvl {player1.level}",
        f"Weapon: {player1.weapon}",
        f"Armor: {player1.armor}",
        f"XP: {player1.experience}/100"
    ]
    
    for i, text in enumerate(p1_stats):
        text_surf = font.render(text, True, (200, 200, 200))
        screen.blit(text_surf, (20, 60 + i * 25))
    
    # Player 2 stats
    p2_stats = [
        f"P2: Lvl {player2.level}",
        f"Weapon: {player2.weapon}",
        f"Armor: {player2.armor}",
        f"XP: {player2.experience}/100"
    ]
    
    for i, text in enumerate(p2_stats):
        text_surf = font.render(text, True, (200, 200, 200))
        screen.blit(text_surf, (WIDTH - 150, 60 + i * 25))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stickman Fight: Shadow Warrior")
    
    # Create shadow warriors
    player1 = ShadowWarrior("Player 1", (100, 300), (255, 0, 0))
    player2 = ShadowWarrior("Player 2", (700, 300), (0, 0, 255))
    
    # Equip starting gear
    player1.equip_weapon("Sword")
    player1.equip_armor("Basic")
    player2.equip_weapon("Nunchaku")
    player2.equip_armor("Basic")
    
    # Create shadow realm
    realm = ShadowRealm()
    
    clock = pygame.time.Clock()
    running = True
    game_over = False
    winner = ""
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    player1 = ShadowWarrior("Player 1", (100, 300), (255, 0, 0))
                    player2 = ShadowWarrior("Player 2", (700, 300), (0, 0, 255))
                    player1.equip_weapon("Sword")
