class RagdollSystem:
    def __init__(self):
        pass

    def apply_ragdoll(self, entity, force_direction, magnitude):
        # Apply ragdoll physics to an entity
        entity.velocity[0] += force_direction[0] * magnitude
        entity.velocity[1] += force_direction[1] * magnitude

    def update_ragdoll(self, entity, dt):
        # Update ragdoll physics over time
        entity.velocity[0] *= FRICTION
        entity.velocity[1] *= FRICTION
        entity.velocity[1] += GRAVITY * dt  # Apply gravity
