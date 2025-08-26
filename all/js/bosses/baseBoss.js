// Base Boss Class - Abstract class for all boss entities
class BaseBoss {
    constructor(sceneManager, physicsEngine) {
        if (new.target === BaseBoss) {
            throw new Error("BaseBoss is an abstract class and cannot be instantiated directly.");
        }
        
        this.sceneManager = sceneManager;
        this.physicsEngine = physicsEngine;
        this.boss = null;
        this.health = 100;
        this.maxHealth = 100;
        this.isActive = false;
        this.attackCooldown = 0;
        this.attackPattern = 0;
    }

    // Abstract methods that must be implemented by subclasses
    createBoss() {
        throw new Error("Method 'createBoss()' must be implemented.");
    }

    update() {
        throw new Error("Method 'update()' must be implemented.");
    }

    attack() {
        throw new Error("Method 'attack()' must be implemented.");
    }

    takeDamage(amount) {
        this.health = Math.max(0, this.health - amount);
        
        if (this.health <= 0) {
            this.defeat();
        }
        
        return this.health;
    }

    defeat() {
        this.isActive = false;
        this.onDefeat();
    }

    onDefeat() {
        // Override in subclasses for specific defeat behavior
        console.log("Boss defeated!");
    }

    activate() {
        this.isActive = true;
        this.onActivate();
    }

    onActivate() {
        // Override in subclasses for specific activation behavior
        console.log("Boss activated!");
    }

    // Common utility methods
    getPosition() {
        return this.boss ? this.boss.position.clone() : new THREE.Vector3();
    }

    setPosition(x, y, z) {
        if (this.boss) {
            this.boss.position.set(x, y, z);
        }
    }

    // Health management
    getHealthPercentage() {
        return (this.health / this.maxHealth) * 100;
    }

    heal(amount) {
        this.health = Math.min(this.maxHealth, this.health + amount);
    }

    // State management
    saveState() {
        return {
            health: this.health,
            position: this.getPosition(),
            isActive: this.isActive,
            attackPattern: this.attackPattern
        };
    }

    loadState(state) {
        if (state.health !== undefined) this.health = state.health;
        if (state.position) this.setPosition(state.position.x, state.position.y, state.position.z);
        if (state.isActive !== undefined) this.isActive = state.isActive;
        if (state.attackPattern !== undefined) this.attackPattern = state.attackPattern;
    }

    // Cleanup
    dispose() {
        if (this.boss) {
            this.sceneManager.removeObject(this.boss);
            this.boss = null;
        }
    }
}

export { BaseBoss };
