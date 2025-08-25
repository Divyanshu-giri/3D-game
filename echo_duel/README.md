# Echo Duel - 3D Enhanced Edition

A 1v1 combat game with innovative echo mechanics, survival elements, and enhanced 3D visual effects built with Pygame.

## 🎮 Game Features

### Core Mechanics
- **1v1 Combat**: Two players battle using different control schemes
- **Echo System**: Every move creates time-delayed echoes that replay actions
- **Survival Elements**: Stamina management and energy shard collection
- **Adaptive Terrain**: Multiple biomes with unique visual themes

### Enhanced 3D Visual Effects
- **Particle Systems**: Dust particles for movement, impact particles for attacks
- **3D-like Shading**: Dynamic lighting effects on players and terrain
- **Realistic Animations**: Smooth particle physics and fading effects
- **Biome Themes**: Crystal caves, decaying temples, and floating islands

## 🎯 Controls

### Player 1 (Red)
- **Movement**: WASD keys
- **Attack**: SPACE key
- **Use Shard**: Q key (restores stamina)

### Player 2 (Green)
- **Movement**: Arrow keys
- **Attack**: ENTER key
- **Use Shard**: / key (restores stamina)

## 🏗️ Technical Implementation

### File Structure
```
echo_duel/
├── main.py              # Main game loop and entry point
├── config.py            # Game configuration and constants
├── player.py           # Player class with 3D effects and particles
├── echo.py            # Echo system implementation
├── terrain.py         # Adaptive terrain with multiple biomes
├── survival.py        # Energy shard system
├── three_d_effects.py # Pseudo-3D visual effects system
├── weapons.py         # Weapon system (placeholder)
├── ai_assistant.py    # AI features (placeholder)
├── narrative.py       # Story generation (placeholder)
└── requirements.txt   # Dependencies
```

### Key Technical Features
- **Pseudo-3D Rendering**: Achieved through shading, particles, and visual effects
- **Real-time Particle Physics**: Dynamic particle movement and fading
- **Modular Biome System**: Easily extensible terrain themes
- **Performance Optimized**: Efficient rendering and collision detection

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game**:
   ```bash
   python echo_duel/main.py
   ```

3. **Play**:
   - Player 1 uses WASD + SPACE
   - Player 2 uses Arrow keys + ENTER
   - Collect energy shards to restore stamina

## 🎨 Visual Enhancements

### 3D Effects Implemented
- **Dynamic Lighting**: Highlight and shadow effects on all game objects
- **Particle Systems**: Realistic dust and impact particles
- **Fading Effects**: Smooth alpha transitions for echoes and particles
- **Color Gradients**: Dynamic color transitions for stamina bars

### Biome Themes
- **Crystal Cave**: Blue/purple theme with crystalline structures
- **Decaying Temple**: Brown/orange theme with ancient pillars
- **Floating Islands**: Green theme with floating platforms

## 🔧 Customization

### Adding New Biomes
Edit `terrain.py` and add new biome definitions to the `biome_colors` dictionary:

```python
self.biome_colors = {
    "new_biome": [(r1, g1, b1), (r2, g2, b2), (r3, g3, b3)],
    # ... existing biomes
}
```

### Modifying Visual Effects
Adjust parameters in `three_d_effects.py` and `player.py` to change:
- Particle count and behavior
- Lighting intensity
- Color schemes
- Animation speeds

## 🎯 Future Enhancements

### Planned Features
- [ ] Weapon system with modular upgrades
- [ ] AI assistant for echo prediction
- [ ] GPT-powered narrative generation
- [ ] Multi-biome transitions
- [ ] Sound effects and music
- [ ] Online multiplayer support

### Technical Roadmap
- [ ] Performance optimization for larger maps
- [ ] Advanced collision detection
- [ ] Save/load game state
- [ ] Custom map editor

## 📊 Performance Notes

The game is optimized for 60 FPS on most systems. Key optimizations include:
- Efficient particle management with object pooling
- Minimal redraw regions
- Optimized collision detection
- Memory-efficient object creation/destruction

## 🤝 Contributing

Feel free to contribute by:
1. Adding new biome themes
2. Implementing additional 3D effects
3. Enhancing the particle system
4. Adding new game mechanics
5. Improving performance

## 📝 License

This project is open source and available under the MIT License.

---

**Echo Duel** - Where every move leaves its mark in time! ⚔️🕰️
