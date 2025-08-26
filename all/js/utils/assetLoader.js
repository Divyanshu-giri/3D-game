// Asset Loader - Handles loading of game assets
class AssetLoader {
    constructor() {
        this.assets = {};
    }

    async loadTexture(url) {
        return new Promise((resolve, reject) => {
            const loader = new THREE.TextureLoader();
            loader.load(url, (texture) => {
                resolve(texture);
            }, undefined, (error) => {
                reject(error);
            });
        });
    }

    async loadModel(url) {
        return new Promise((resolve, reject) => {
            const loader = new THREE.GLTFLoader();
            loader.load(url, (gltf) => {
                resolve(gltf.scene);
            }, undefined, (error) => {
                reject(error);
            });
        });
    }

    async loadAssets() {
        // Load all necessary assets here
        try {
            this.assets.texture = await this.loadTexture('assets/textures/ground.jpg');
            this.assets.model = await this.loadModel('assets/models/player.glb');
            console.log('Assets loaded successfully:', this.assets);
        } catch (error) {
            console.error('Error loading assets:', error);
        }
    }

    // New method to load assets
    async loadAsset(url) {
        // Logic to load a specific asset
        return await this.loadModel(url); // Example for models
    }
}

export { AssetLoader };
