import pygame
import sys
import random
import math
from config import *

class StickmanPlayer:
    def __init__(self, name, position, color):
        self.name = name
        self.position = list(position)
        self.velocity = [0, 0]
        self.health = 100
        self.stamina = 100
        self.color = color
        self.size = 20
        self.attack_cooldown = 0
        self.facing_right = True
        self.is_jumping = False
        self.on_ground = False
        self.attack_animation = 0
        self.hit_animation = 0
        
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
            self.attack_cooldown = 20
            self.attack_animation = 10  # Start attack animation
            return True
        return False
        
    def take_damage(self, amount):
        self.health -= amount
        self.hit_animation = 15  # Start hit animation
        if self.health <= 0:
            self.health = 0
            return True  # Player is defeated
        return False
        
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
                
        # Update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Update animations
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1
            
        # Recover stamina
        self.stamina = min(100, self.stamina + 0.5)
            
    def draw(self, screen):
        # Draw stickman body
        center_x = self.position[0] + self.size // 2
        center_y = self.position[1] + self.size // 2
        
        # Apply hit animation (red flash)
        draw_color = self.color
        if self.hit_animation > 0:
            draw_color = (255, 100, 100)  # Red tint when hit
        
        # Head
        pygame.draw.circle(screen, draw_color, (center_x, center_y - 10), 8)
        
        # Body
        pygame.draw.line(screen, draw_color, (center_x, center_y - 2), (center_x, center_y + 15), 3)
        
        # Arms with attack animation
        if self.attack_animation > 0:
            # Attack animation - arm extended
            attack_angle = 0 if self.facing_right else 180
            arm_x = center_x + math.cos(math.radians(attack_angle)) * 25
            arm_y = center_y + 5 + math.sin(math.radians(attack_angle)) * 25
            pygame.draw.line(screen, draw_color, (center_x, center_y + 5), (arm_x, arm_y), 4)
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
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0] - 10, self.position[1] - 20, 40, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - 10, self.position[1] - 20, 40 * (self.health / 100), 5))

class SimpleTerrain:
    def __init__(self):
        self.blocks = []
        self.generate_terrain()
        
    def generate_terrain(self):
        # Create simple ground only
        for x in range(0, WIDTH, 30):
            self.blocks.append({
                'x': x,
                'y': HEIGHT - 50,
                'size': 30,
                'type': 'grass',
                'color': (86, 125, 70)
            })
        
    def draw(self, screen):
        # Draw background
        screen.fill((135, 206, 235))  # Sky blue
        
        # Draw blocks
        for block in self.blocks:
            pygame.draw.rect(screen, block['color'], 
                           (block['x'], block['y'], block['size'], block['size']))
            # Add block outline
            pygame.draw.rect(screen, (0, 0, 0), 
                           (block['x'], block['y'], block['size'], block['size']), 1)

def show_game_over(screen, winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 72)
    text = font.render(f"{winner} WINS!", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    small_font = pygame.font.Font(None, 36)
    restart_text = small_font.render("Press R to restart or ESC to quit", True, (200, 200, 200))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stickman Duelist")
    
    # Create players
    player1 = StickmanPlayer("Player 1", (100, 300), (255, 0, 0))
    player2 = StickmanPlayer("Player 2", (700, 300), (0, 0, 255))
    
    # Create terrain
    terrain = SimpleTerrain()
    
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
                    player1 = StickmanPlayer("Player 1", (100, 300), (255, 0, 0))
                    player2 = StickmanPlayer("Player 2", (700, 300), (0, 0, 255))
                    game_over = False
                    winner = ""
                # Jump
                elif event.key == pygame.K_SPACE and not game_over:
                    player1.jump()
                elif event.key == pygame.K_RETURN and not game_over:
                    player2.jump()
        
        if not game_over:
            # Handle movement
            keys = pygame.key.get_pressed()
            
            # Player 1 controls (WASD)
            direction1 = [0, 0]
            if keys[pygame.K_w]: direction1[1] = -1
            if keys[pygame.K_s]: direction1[1] = 1
            if keys[pygame.K_a]: direction1[0] = -1
            if keys[pygame.K_d]: direction1[0] = 1
            player1.move(direction1)
            
            # Player 2 controls (Arrow keys)
            direction2 = [0, 0]
            if keys[pygame.K_UP]: direction2[1] = -1
            if keys[pygame.K_DOWN]: direction2[1] = 1
            if keys[pygame.K_LEFT]: direction2[0] = -1
            if keys[pygame.K_RIGHT]: direction2[0] = 1
            player2.move(direction2)
            
            # Handle attacks
            if keys[pygame.K_q] and player1.attack():
                # Check if player2 is in range
                dx = player2.position[0] - player1.position[0]
                dy = player2.position[1] - player1.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 50:
                    if player2.take_damage(10):
                        game_over = True
                        winner = "PLAYER 1"
                    
            if keys[pygame.K_SLASH] and player2.attack():
                # Check if player1 is in range
                dx = player1.position[0] - player2.position[0]
                dy = player1.position[1] - player2.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 50:
                    if player1.take_damage(10):
                        game_over = True
                        winner = "PLAYER 2"
            
            # Update game state
            player1.update()
            player2.update()
            
            # Render
            terrain.draw(screen)
            player1.draw(screen)
            player2.draw(screen)
            
            # Draw UI
            font = pygame.font.Font(None, 36)
            title = font.render("Stickman Duelist", True, (255, 255, 255))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
            
            # Draw controls info
            small_font = pygame.font.Font(None, 20)
            controls = [
                "P1: WASD move, SPACE jump, Q attack",
                "P2: Arrows move, ENTER jump, / attack"
            ]
            for i, text in enumerate(controls):
                text_surf = small_font.render(text, True, (200, 200, 200))
                screen.blit(text_surf, (20, HEIGHT - 40 + i * 20))
        else:
            show_game_over(screen, winner)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
