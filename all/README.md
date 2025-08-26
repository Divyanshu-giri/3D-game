# Ashes of Aether 🌌

A 3D survival game set in a shattered sky-world where floating islands drift through the remnants of a forgotten civilization. Players must band together to survive harsh conditions, gather resources, and prepare for epic confrontations against elemental bosses.

## 🎮 Game Features

- **Procedural Floating Islands**: Explore dynamically generated islands in the sky
- **Elemental Boss Battles**: Face off against massive elemental bosses with unique abilities
- **Survival Mechanics**: Scavenge resources, craft tools, and build shelters
- **Modular Design**: Clean, readable code structure perfect for learning and expansion
- **Web-Based**: Runs directly in modern browsers using Three.js and WebGL

## 🧩 Current Implementation

### Core Modules Implemented:
- **Engine**: Three.js scene management, camera controls, physics integration
- **World Generation**: Procedural floating island creation
- **Player System**: Character controller with movement and interaction
- **Boss System**: Base boss class and Pyros (Fire Element boss) implementation
- **UI/UX**: Health/resource HUD, boss alerts, and interactive elements

### Bosses:
- **Pyros, the Flame Leviathan**: Fire-based boss with flame breath and meteor attacks

## 🚀 Getting Started

### Prerequisites
- Modern web browser with WebGL support (Chrome, Firefox, Safari, Edge)
- No installation required - runs directly in the browser

### Running the Game
1. Simply open `index.html` in your web browser
2. Or use a local server for better performance:
   ```bash
   # If you have Python installed:
   python -m http.server 8000
   
   # If you have Node.js installed:
   npx serve . -p 3000
   ```

### Controls
- **WASD**: Move character
- **Mouse**: Look around (right-click and drag)
- **Space**: Jump
- **Mouse Wheel**: Zoom in/out

## 🛠️ Technical Stack

- **3D Engine**: Three.js (WebGL)
- **Physics**: Cannon.js
- **UI**: HTML5, CSS3, JavaScript ES6+
- **Architecture**: Modular ES6 modules

## 📁 Project Structure

```
ashes-of-aether/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Game styles
├── js/
│   ├── main.js         # Game initialization
│   ├── engine/         # Core engine modules
│   │   ├── sceneManager.js
│   │   ├── cameraController.js
│   │   └── physicsEngine.js
│   ├── world/          # World generation
│   │   ├── islandGenerator.js
│   │   ├── terrain.js
│   │   └── biomeSystem.js
│   ├── player/         # Player systems
│   │   ├── playerController.js
│   │   ├── inventory.js
│   │   └── roles.js
│   ├── bosses/         # Boss implementations
│   │   ├── baseBoss.js
│   │   ├── pyros.js
│   │   ├── zephra.js
│   │   └── umbra.js
│   ├── ui/             # User interface
│   │   ├── hud.js
│   │   ├── bossAlert.js
│   │   └── menu.js
│   └── utils/          # Utility functions
│       ├── helpers.js
│       ├── math.js
│       └── assetLoader.js
├── assets/             # Game assets
│   ├── models/
│   ├── textures/
│   └── sounds/
└── package.json        # Project configuration
```

## 🎯 Development Goals

### Short-term:
- [x] Basic Three.js setup and scene management
- [x] Player character with movement controls
- [x] Procedural island generation
- [x] Pyros boss implementation
- [x] Basic UI/HUD system
- [ ] Resource collection system
- [ ] Crafting mechanics
- [ ] Multiplayer foundation

### Long-term:
- [ ] Additional elemental bosses (Zephra, Umbra)
- [ ] Advanced AI behaviors
- [ ] Physics-based terrain deformation
- [ ] Day/night cycle and weather system
- [ ] Save/load system
- [ ] Multiplayer co-op functionality

## 🎨 Art & Assets

The game currently uses programmatically generated geometry. Future development will include:
- Custom 3D models for characters and bosses
- High-quality textures and materials
- Particle effects and visual feedback
- Sound effects and background music

## 🔧 Customization

The modular architecture makes it easy to:
- Add new boss types by extending `BaseBoss` class
- Create new island biomes and terrain features
- Implement new player abilities and roles
- Extend the UI with new gameplay elements

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📞 Support

For questions or support, please open an issue on the GitHub repository.

---

**Built with passion for the art of game development** 🎮
