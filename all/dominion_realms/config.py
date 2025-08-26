# Game configuration constants
WIDTH = 1024
HEIGHT = 768
FPS = 60

# Physics constants
GRAVITY = 9.8
JUMP_FORCE = -15
FRICTION = 0.9
TERMINAL_VELOCITY = 20
COLLISION_DAMPING = 0.8

# Gameplay constants
BOSS_SPAWN_TIME = 120  # seconds until boss spawns
RESOURCE_SPAWN_RATE = 5  # seconds between resource spawns
CRAFTING_TIME = 2.0  # seconds to craft an item
HEALTH_REGEN_RATE = 0.5  # health per second
STAMINA_DRAIN_RATE = 10  # stamina per action
STAMINA_REGEN_RATE = 5  # stamina per second

# Player constants
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_SPEED = 300
PLAYER_JUMP_FORCE = -500
PLAYER_ATTACK_DAMAGE = 10
PLAYER_ATTACK_COOLDOWN = 0.5

# Boss constants
BOSS_HEALTH = 1000
BOSS_ATTACK_DAMAGE = 25
BOSS_ATTACK_COOLDOWN = 2.0
BOSS_MOVEMENT_SPEED = 150
BOSS_ABILITY_COOLDOWN = 10.0

# Resource types
RESOURCE_TYPES = {
    'wood': {'color': (139, 69, 19), 'value': 1},
    'stone': {'color': (128, 128, 128), 'value': 2},
    'crystal': {'color': (0, 191, 255), 'value': 5},
    'metal': {'color': (192, 192, 192), 'value': 3},
    'energy': {'color': (255, 215, 0), 'value': 10}
}

# Crafting recipes
CRAFTING_RECIPES = {
    'basic_sword': {'wood': 5, 'stone': 3},
    'shield': {'wood': 8, 'metal': 2},
    'armor': {'metal': 10, 'energy': 2},
    'health_potion': {'crystal': 3, 'energy': 1},
    'stamina_boost': {'energy': 2, 'crystal': 1}
}

# Biome types
BIOME_TYPES = {
    'volcanic_crater': {
        'ground_color': (139, 0, 0),
        'obstacle_color': (105, 105, 105),
        'resource_spawns': ['stone', 'metal', 'energy'],
        'boss_type': 'volcano_lord'
    },
    'crystal_cave': {
        'ground_color': (75, 0, 130),
        'obstacle_color': (138, 43, 226),
        'resource_spawns': ['crystal', 'energy', 'stone'],
        'boss_type': 'crystal_guardian'
    },
    'floating_islands': {
        'ground_color': (34, 139, 34),
        'obstacle_color': (107, 142, 35),
        'resource_spawns': ['wood', 'crystal', 'energy'],
        'boss_type': 'sky_tyrant'
    }
}

# Boss types
BOSS_TYPES = {
    'volcano_lord': {
        'health': 1200,
        'damage': 30,
        'speed': 120,
        'abilities': ['lava_pool', 'meteor_shower', 'earthquake'],
        'color': (255, 69, 0)
    },
    'crystal_guardian': {
        'health': 1000,
        'damage': 25,
        'speed': 180,
        'abilities': ['crystal_spikes', 'energy_beam', 'teleport'],
        'color': (0, 191, 255)
    },
    'sky_tyrant': {
        'health': 900,
        'damage': 20,
        'speed': 200,
        'abilities': ['wind_gust', 'lightning_strike', 'aerial_assault'],
        'color': (135, 206, 250)
    }
}

# Ability effects
ABILITY_EFFECTS = {
    'lava_pool': {'damage': 10, 'duration': 5, 'cooldown': 15},
    'meteor_shower': {'damage': 20, 'duration': 3, 'cooldown': 20},
    'earthquake': {'damage': 15, 'duration': 4, 'cooldown': 18},
    'crystal_spikes': {'damage': 12, 'duration': 4, 'cooldown': 12},
    'energy_beam': {'damage': 25, 'duration': 2, 'cooldown': 15},
    'teleport': {'damage': 0, 'duration': 0, 'cooldown': 10},
    'wind_gust': {'damage': 8, 'duration': 3, 'cooldown': 8},
    'lightning_strike': {'damage': 30, 'duration': 1, 'cooldown': 25},
    'aerial_assault': {'damage': 18, 'duration': 2, 'cooldown': 15}
}

# UI colors
UI_COLORS = {
    'health_bar': (255, 0, 0),
    'stamina_bar': (0, 255, 0),
    'boss_health': (255, 165, 0),
    'resource_text': (255, 255, 255),
    'crafting_bg': (50, 50, 50, 200),
    'inventory_bg': (40, 40, 40, 220)
}

# Font sizes
FONT_SIZES = {
    'title': 48,
    'subtitle': 32,
    'normal': 24,
    'small': 18,
    'tiny': 14
}
