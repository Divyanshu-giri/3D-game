class PlayerCombat:
    def __init__(self):
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.last_attack_time = 0

    def attack(self, target_position):
        current_time = pygame.time.get_ticks() / 1000.0  # Get current time in seconds
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            # Implement attack logic (e.g., check if target is within range)
            print(f"Attacking target at {target_position}")
            return PLAYER_ATTACK_DAMAGE
        return 0  # No damage if cooldown is active
