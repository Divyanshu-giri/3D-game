// Pyros, the Flame Leviathan - Fire Element Boss
import { BaseBoss } from './baseBoss.js';

class Pyros extends BaseBoss {
    constructor(sceneManager, physicsEngine) {
        super(sceneManager, physicsEngine);
        this.attackCooldown = 0;
        this.attackPattern = 0;
        this.flameParticles = [];
        this.createBoss();
    }

    createBoss() {
        // Create boss geometry - a fiery creature
        const geometry = new THREE.ConeGeometry(2, 4, 8);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0xff4500,
            emissive: 0xff6b35,
            emissiveIntensity: 0.5
        });
        
        this.boss = new THREE.Mesh(geometry, material);
        this.boss.position.set(0, 10, -20);
        this.boss.castShadow = true;
        
        // Add flame effect
        this.createFlameEffect();
        
        this.sceneManager.addObject(this.boss);
    }

    createFlameEffect() {
        // Create particle system for flames
        const particleCount = 50;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 2;
            positions[i3 + 1] = Math.random() * 3;
            positions[i3 + 2] = (Math.random() - 0.5) * 2;
            
            colors[i3] = Math.random() * 0.5 + 0.5;     // Red
            colors[i3 + 1] = Math.random() * 0.3;       // Green
            colors[i3 + 2] = 0;                        // Blue
        }

        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const particleMaterial = new THREE.PointsMaterial({
            size: 0.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.8
        });

        const particleSystem = new THREE.Points(particles, particleMaterial);
        this.boss.add(particleSystem);
        this.flameParticles.push(particleSystem);
    }

    update() {
        if (!this.isActive) return;

        // Update attack cooldown
        if (this.attackCooldown > 0) {
            this.attackCooldown--;
        } else {
            this.attack();
        }

        // Animate flame particles
        this.animateFlames();
    }

    attack() {
        switch (this.attackPattern) {
            case 0:
                this.fireBreathAttack();
                break;
            case 1:
                this.meteorShower();
                break;
            case 2:
                this.groundFire();
                break;
        }

        this.attackCooldown = 120; // 2 seconds at 60 FPS
        this.attackPattern = (this.attackPattern + 1) % 3;
    }

    fireBreathAttack() {
        console.log("Pyros uses Fire Breath!");
        // Create fire breath effect
        this.createFireBreath();
    }

    meteorShower() {
        console.log("Pyros calls Meteor Shower!");
        // Create meteor projectiles
    }

    groundFire() {
        console.log("Pyros ignites the ground!");
        // Create ground fire effect
    }

    createFireBreath() {
        const fireGeometry = new THREE.ConeGeometry(1, 8, 8);
        const fireMaterial = new THREE.MeshPhongMaterial({
            color: 0xff6b35,
            emissive: 0xff4500,
            transparent: true,
            opacity: 0.7
        });

        const fire = new THREE.Mesh(fireGeometry, fireMaterial);
        fire.position.set(0, 1, -4);
        fire.rotation.x = Math.PI / 2;
        this.boss.add(fire);

        // Animate fire breath
        const scale = { x: 1 };
        const animation = setInterval(() => {
            scale.x += 0.1;
            fire.scale.set(scale.x, scale.x, scale.x);
            
            if (scale.x > 3) {
                clearInterval(animation);
                this.boss.remove(fire);
            }
        }, 50);
    }

    animateFlames() {
        this.flameParticles.forEach(particles => {
            const positions = particles.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                positions[i + 1] += (Math.random() - 0.5) * 0.1;
                if (positions[i + 1] > 3) positions[i + 1] = 0;
            }
            particles.geometry.attributes.position.needsUpdate = true;
        });
    }

    onActivate() {
        console.log("Pyros awakens! The air grows hot...");
        // Play activation sound
        // Show boss health bar
    }

    onDefeat() {
        console.log("Pyros has been defeated! The flames subside...");
        // Play defeat animation
        // Drop loot
        // Unlock new areas
    }

    takeDamage(amount) {
        const damageTaken = super.takeDamage(amount);
        
        // Visual feedback for damage
        if (damageTaken > 0) {
            this.flashRed();
        }
        
        return damageTaken;
    }

    flashRed() {
        const originalColor = this.boss.material.color.clone();
        this.boss.material.color.set(0xff0000);
        
        setTimeout(() => {
            this.boss.material.color.copy(originalColor);
        }, 100);
    }
}

export { Pyros };
