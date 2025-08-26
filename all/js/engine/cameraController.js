import { SceneManager } from '../engine/sceneManager.js';

// Camera Controller - Handles camera movement and behavior
class CameraController {
    constructor(sceneManager) {
        this.sceneManager = sceneManager;
        this.camera = sceneManager.getCamera();
        this.target = null;
        this.offset = new THREE.Vector3(0, 5, 10);
        this.currentOffset = new THREE.Vector3().copy(this.offset);
        this.lerpSpeed = 0.1;
        this.rotationSpeed = 0.005;
        this.isRotating = false;
        this.previousMousePosition = { x: 0, y: 0 };

        this.setupEventListeners();
    }

    setupEventListeners() {
        // Mouse movement for camera rotation
        document.addEventListener('mousedown', (e) => {
            if (e.button === 2) { // Right mouse button
                this.isRotating = true;
                this.previousMousePosition = { x: e.clientX, y: e.clientY };
            }
        });

        document.addEventListener('mouseup', (e) => {
            if (e.button === 2) {
                this.isRotating = false;
            }
        });

        document.addEventListener('mousemove', (e) => {
            if (this.isRotating && this.target) {
                this.handleCameraRotation(e);
            }
        });

        // Prevent context menu on right click
        document.addEventListener('contextmenu', (e) => e.preventDefault());

        // Mouse wheel for zoom
        document.addEventListener('wheel', (e) => {
            this.handleCameraZoom(e);
        }, { passive: false });

        // Touch events for mobile
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                this.isRotating = true;
                this.previousMousePosition = {
                    x: e.touches[0].clientX,
                    y: e.touches[0].clientY
                };
            }
        });

        document.addEventListener('touchend', () => {
            this.isRotating = false;
        });

        document.addEventListener('touchmove', (e) => {
            if (this.isRotating && e.touches.length === 1 && this.target) {
                e.preventDefault();
                this.handleCameraRotation({
                    clientX: e.touches[0].clientX,
                    clientY: e.touches[0].clientY
                });
            }
        });
    }

    handleCameraRotation(event) {
        const deltaX = event.clientX - this.previousMousePosition.x;
        const deltaY = event.clientY - this.previousMousePosition.y;

        // Calculate rotation angles
        const horizontalAngle = -deltaX * this.rotationSpeed;
        const verticalAngle = -deltaY * this.rotationSpeed;

        // Rotate offset around target
        this.offset.applyAxisAngle(new THREE.Vector3(0, 1, 0), horizontalAngle);

        // Apply vertical rotation with limits to prevent flipping
        const currentVerticalAngle = Math.atan2(this.offset.y, Math.sqrt(this.offset.x * this.offset.x + this.offset.z * this.offset.z));
        const newVerticalAngle = Math.max(Math.min(currentVerticalAngle + verticalAngle, Math.PI / 2 - 0.1), -Math.PI / 2 + 0.1);

        const horizontalDistance = Math.sqrt(this.offset.x * this.offset.x + this.offset.z * this.offset.z);
        this.offset.y = horizontalDistance * Math.tan(newVerticalAngle);

        this.previousMousePosition = { x: event.clientX, y: event.clientY };
    }

    handleCameraZoom(event) {
        event.preventDefault();

        const zoomIntensity = 0.1;
        const zoomDirection = event.deltaY > 0 ? 1 : -1;

        // Calculate new offset distance
        const currentDistance = this.offset.length();
        const minDistance = 3;
        const maxDistance = 20;

        let newDistance = currentDistance + zoomDirection * zoomIntensity;
        newDistance = Math.max(minDistance, Math.min(maxDistance, newDistance));

        // Normalize offset and scale to new distance
        this.offset.normalize().multiplyScalar(newDistance);
    }

    setTarget(target) {
        this.target = target;
    }

    update() {
        if (this.target) {
            // Smoothly interpolate camera position
            this.currentOffset.lerp(this.offset, this.lerpSpeed);

            // Calculate target position
            const targetPosition = new THREE.Vector3().copy(this.target.position);

            // Set camera position
            this.camera.position.copy(targetPosition).add(this.currentOffset);

            // Make camera look at target
            this.camera.lookAt(targetPosition);
        }
    }

    // Camera modes
    setFirstPersonMode() {
        this.offset.set(0, 1.6, 0.1);
        this.lerpSpeed = 0.2;
    }

    setThirdPersonMode() {
        this.offset.set(0, 5, 10);
        this.lerpSpeed = 0.1;
    }

    setTopDownMode() {
        this.offset.set(0, 20, 0.1);
        this.lerpSpeed = 0.05;
    }

    // Camera shake effect for impacts
    shakeCamera(intensity = 0.5, duration = 0.3) {
        const originalOffset = this.offset.clone();
        const shakeInterval = setInterval(() => {
            this.offset.x = originalOffset.x + (Math.random() - 0.5) * intensity;
            this.offset.y = originalOffset.y + (Math.random() - 0.5) * intensity;
            this.offset.z = originalOffset.z + (Math.random() - 0.5) * intensity;
        }, 50);

        setTimeout(() => {
            clearInterval(shakeInterval);
            this.offset.copy(originalOffset);
        }, duration * 1000);
    }

    // Get camera state
    getCameraState() {
        return {
            position: this.camera.position.clone(),
            rotation: this.camera.rotation.clone(),
            offset: this.offset.clone(),
            target: this.target ? this.target.position.clone() : null
        };
    }

    // Set camera state (for save/load)
    setCameraState(state) {
        if (state.position) this.camera.position.copy(state.position);
        if (state.rotation) this.camera.rotation.copy(state.rotation);
        if (state.offset) this.offset.copy(state.offset);
        this.currentOffset.copy(this.offset);
    }
}

export { CameraController };
