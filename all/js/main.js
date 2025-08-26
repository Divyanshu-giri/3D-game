// Ashes of Aether - Main JavaScript File

// Import necessary modules
import { SceneManager } from './engine/sceneManager.js';
import { CameraController } from './engine/cameraController.js';
import { PhysicsEngine } from './engine/physicsEngine.js';
import { IslandGenerator } from './world/islandGenerator.js';
import { PlayerController } from './player/playerController.js';
import { HUD } from './ui/hud.js';
import { BossAlert } from './ui/bossAlert.js';
import { Pyros } from './bosses/pyros.js';
import { AssetLoader } from './utils/assetLoader.js';

// Initialize the game
const init = () => {
    console.log('Initializing game components...');
    const sceneManager = new SceneManager();
    console.log('SceneManager created.');
    const cameraController = new CameraController(sceneManager);
    const physicsEngine = new PhysicsEngine();
    const islandGenerator = new IslandGenerator(sceneManager);
    const playerController = new PlayerController(sceneManager);
    cameraController.setTarget(playerController.player); // Set the player as the camera target
    const hud = new HUD();
    const bossAlert = new BossAlert();
    const pyros = new Pyros(sceneManager, physicsEngine);

    // Load assets and start the game
    const assetLoader = new AssetLoader();
    console.log('Loading assets and generating islands...');
    Promise.all([
        sceneManager.loadAssets(),
        islandGenerator.generateIslands()
    ]).then(() => {
        sceneManager.start();
        playerController.setup();
        hud.setup();
        bossAlert.setup();

        // Activate the boss for demonstration
        pyros.activate();

        // Start the game loop
        gameLoop(sceneManager, playerController, hud, bossAlert, pyros);
    }).catch(error => {
        console.error('Error initializing the game:', error);
    });
};

// Game loop
const gameLoop = (sceneManager, playerController, hud, bossAlert, pyros) => {
    requestAnimationFrame(() => gameLoop(sceneManager, playerController, hud, bossAlert, pyros));

    // Update components
    playerController.update();
    pyros.update();
    sceneManager.update();

    // Update HUD
    hud.update(playerController.getHealth(), playerController.getResources());

    // Update Boss Alert
    if (pyros.isActive) {
        bossAlert.updateBossStatus(pyros.getHealthPercentage());
    }
};

// Start the game
const startScene = () => {
    init();
};

window.onload = () => {
    startScene();
};
