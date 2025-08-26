#!/usr/bin/env python3
"""
Simple Playable Stickman Battle Game
Run this file to play the game immediately!
"""

import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Battle - Play Now!")
clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 20
        self.color = RED
        self.speed = 5
        self.health = 100
        self.stamina = 100
        self.velocity_y = 0
        self.on_ground = False
        self.jump_power = -15
        self.gravity = 0.8
        
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Ground collision
        if self.y + self.radius > HEIGHT - 50:
            self.y = HEIGHT - 50 - self.radius
            self.velocity_y = 0
            self.on_ground = True
            
        # Screen boundaries
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw stickman body
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y + 30), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 15), (self.x - 15, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 15), (self.x + 15, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 30), (self.x - 15, self.y + 45), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 30), (self.x + 15, self.y + 45), 3)

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT - 50 - 20
        self.radius = 20
        self.color = BLUE
        self.speed = 3
        self.health = 50
        
    def update(self, player_x):
        # Simple AI: move towards player
        if self.x < player_x:
            self.x += self.speed
        else:
            self.x -= self.speed
            
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw stickman body
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y + 30), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 15), (self.x - 15, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 15), (self.x + 15, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 30), (self.x - 15, self.y + 45), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 30), (self.x + 15, self.y + 45), 3)

# Particle effect class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size -= 0.1
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))

# Game setup
player = Player()
enemies = [Enemy() for _ in range(3)]
particles = []
font = pygame.font.Font(None, 36)

# Game loop
running = True
score = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Attack - create particles
                for _ in range(10):
                    particles.append(Particle(player.x, player.y))
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Update game state
    player.move(keys)
    
    # Update enemies
    for enemy in enemies:
        enemy.update(player.x)
        
        # Check collision with player
        distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
        if distance < player.radius + enemy.radius:
            player.health -= 1
            # Create hit particles
            for _ in range(5):
                particles.append(Particle(enemy.x, enemy.y))
    
    # Update particles
    particles = [p for p in particles if p.lifetime > 0]
    for particle in particles:
        particle.update()
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 50, WIDTH, 50))
    
    # Draw player
    player.draw()
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
    
    # Draw particles
    for particle in particles:
        particle.draw()
    
    # Draw UI
    health_text = font.render(f"Health: {player.health}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(health_text, (20, 20))
    screen.blit(score_text, (20, 60))
    
    # Draw instructions
    instructions = font.render("Arrow keys to move, SPACE to attack", True, BLACK)
    screen.blit(instructions, (WIDTH // 2 - 200, HEIGHT - 100))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)
    
    # Game over check
    if player.health <= 0:
        game_over_text = font.render("GAME OVER! Press any key to quit", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

pygame.quit()
print("Thanks for playing Stickman Battle!")
print("Your final score:", score)
