// Island Generator - Procedural generation of floating islands
class IslandGenerator {
    constructor(sceneManager) {
        this.sceneManager = sceneManager;
        this.islands = [];
    }

    generateIslands() {
        return new Promise((resolve) => {
            const islandCount = 5; // Number of islands to generate
            const islandSpacing = 20; // Space between islands
            const islandSize = 5; // Size of each island

            for (let i = 0; i < islandCount; i++) {
                const x = (Math.random() - 0.5) * islandSpacing * islandCount;
                const y = Math.random() * 10 + 1; // Height above ground
                const z = (Math.random() - 0.5) * islandSpacing * islandCount;

                const island = this.createIsland(x, y, z, islandSize);
                this.islands.push(island);
                this.sceneManager.addObject(island);
            }
            
            resolve(); // Resolve the promise when islands are generated
        });
    }

    createIsland(x, y, z, size) {
        const geometry = new THREE.CylinderGeometry(size, size, 1, 8);
        const material = new THREE.MeshPhongMaterial({ color: 0x8B4513 }); // Brown color for earth
        const island = new THREE.Mesh(geometry, material);
        
        island.position.set(x, y, z);
        island.rotation.x = Math.random() * Math.PI;
        island.rotation.z = Math.random() * Math.PI;
        island.castShadow = true;
        island.receiveShadow = true;

        return island;
    }
}

export { IslandGenerator };
