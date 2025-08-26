import { SceneManager } from '../engine/sceneManager.js';

// Player Controller - Handles player movement, input, and interactions
class PlayerController {
    constructor(sceneManager) {
        this.sceneManager = sceneManager;
        this.player = null;
        this.velocity = new THREE.Vector3();
        this.direction = new THREE.Vector3();
        this.moveSpeed = 5.0;
        this.jumpStrength = 8.0;
        this.isGrounded = false;
        this.keys = {};

        this.setupEventListeners();
    }

    setup() {
        this.createPlayer();
    }

    createPlayer() {
        const geometry = new THREE.CapsuleGeometry(0.5, 1, 4, 8);
        const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
        this.player = new THREE.Mesh(geometry, material);

        this.player.position.set(0, 5, 0);
        this.player.castShadow = true;

        this.sceneManager.addObject(this.player);
    }

    setupEventListeners() {
        // Keyboard input
        document.addEventListener('keydown', (event) => {
            this.keys[event.code] = true;
        });

        document.addEventListener('keyup', (event) => {
            this.keys[event.code] = false;
        });

        // Mouse click for interactions
        document.addEventListener('click', (event) => {
            this.handleInteraction(event);
        });
    }

    update() {
        this.handleMovement();
        this.applyGravity();
        this.checkGround();
    }

    handleMovement() {
        this.direction.set(0, 0, 0);

        // Forward/backward
        if (this.keys['KeyW']) this.direction.z = -1;
        if (this.keys['KeyS']) this.direction.z = 1;

        // Left/right
        if (this.keys['KeyA']) this.direction.x = -1;
        if (this.keys['KeyD']) this.direction.x = 1;

        // Normalize direction and apply speed
        if (this.direction.length() > 0) {
            this.direction.normalize();
            this.velocity.x = this.direction.x * this.moveSpeed;
            this.velocity.z = this.direction.z * this.moveSpeed;
        } else {
            this.velocity.x = 0;
            this.velocity.z = 0;
        }

        // Jump
        if (this.keys['Space'] && this.isGrounded) {
            this.velocity.y = this.jumpStrength;
            this.isGrounded = false;
        }

        // Apply movement
        this.player.position.x += this.velocity.x * 0.016; // Assuming 60 FPS
        this.player.position.z += this.velocity.z * 0.016;
        this.player.position.y += this.velocity.y * 0.016;
    }

    applyGravity() {
        if (!this.isGrounded) {
            this.velocity.y -= 0.2; // Gravity
        } else {
            this.velocity.y = 0;
        }
    }

    checkGround() {
        // Simple ground check - adjust based on your game's ground level
        if (this.player.position.y <= 0.5) {
            this.player.position.y = 0.5;
            this.isGrounded = true;
        } else {
            this.isGrounded = false;
        }
    }

    handleInteraction(event) {
        // Placeholder for interaction logic
        console.log('Player interaction at:', event.clientX, event.clientY);
    }

    getPosition() {
        return this.player.position.clone();
    }

    setPosition(x, y, z) {
        this.player.position.set(x, y, z);
    }

    // Add methods for player abilities, inventory, etc. here
}

export { PlayerController };
