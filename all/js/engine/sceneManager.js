// No self-import needed

// Scene Manager - Core Three.js setup and management
class SceneManager {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.clock = null;
        this.mixers = [];
        this.assets = {};

        this.init();
    }

    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a1a);

        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 5, 10);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        // Add renderer to DOM
        document.body.appendChild(this.renderer.domElement);

        // Setup clock
        this.clock = new THREE.Clock();

        // Setup lighting
        this.setupLighting();

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // Directional light (sun)
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);

        // Point light for ambient glow
        const pointLight = new THREE.PointLight(0xff6b35, 1, 100);
        pointLight.position.set(0, 20, 0);
        this.scene.add(pointLight);
    }

    async loadAssets() {
        // Create placeholder assets since the actual assets don't exist
        console.log('Creating placeholder assets...');
        this.createPlaceholderAssets();
        return Promise.resolve(); // Return resolved promise to continue game initialization
    }

    async loadModel(url) {
        return new Promise((resolve, reject) => {
            const loader = new THREE.GLTFLoader();
            loader.load(
                url,
                (gltf) => resolve(gltf.scene),
                null,
                (error) => reject(error)
            );
        });
    }

    createPlaceholderAssets() {
        // Create placeholder geometry for testing
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({ color: 0xff6b35 });
        this.assets.playerModel = new THREE.Mesh(geometry, material);
    }

    addObject(object) {
        this.scene.add(object);
    }

    removeObject(object) {
        this.scene.remove(object);
    }

    update() {
        const delta = this.clock.getDelta();
        console.log('Updating scene with delta:', delta);

        // Update animation mixers
        this.mixers.forEach(mixer => {
            mixer.update(delta);
            console.log('Updated mixer:', mixer);
        });

        // Render the scene
        this.renderer.render(this.scene, this.camera);
        console.log('Rendered scene');
    }

    start() {
        // Hide loading screen
        document.getElementById('loading').style.display = 'none';
        document.getElementById('ui').style.display = 'block';

        // Start animation loop
        this.animate();
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.update();
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // Utility methods
    getScene() {
        return this.scene;
    }

    getCamera() {
        return this.camera;
    }

    getRenderer() {
        return this.renderer;
    }

    addMixer(mixer) {
        this.mixers.push(mixer);
    }

    removeMixer(mixer) {
        const index = this.mixers.indexOf(mixer);
        if (index > -1) {
            this.mixers.splice(index, 1);
        }
    }
}

export { SceneManager };
