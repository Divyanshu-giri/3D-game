#!/usr/bin/env python3
"""
Panda3D version of Dominion Realms
3D implementation using Panda3D engine
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
import sys
import random
import math

class DominionRealms3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Game configuration
        self.window_size = (1024, 768)
        self.game_state = {
            'running': True,
            'players': [],
            'boss': None,
            'resources': [],
            'terrain': None,
            'phase': 'scavenge'
        }
        
        # Setup camera
        self.setup_camera()
        
        # Setup lighting
        self.setup_lighting()
        
        # Load game assets
        self.load_assets()
        
        # Create game world
        self.create_world()
        
        # Setup controls
        self.setup_controls()
        
        # Start game loop
        self.taskMgr.add(self.update, "updateGame")
    
    def setup_camera(self):
        """Setup the 3D camera"""
        self.disableMouse()
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0, 0, 0)
        
    def setup_lighting(self):
        """Setup 3D lighting"""
        # Ambient light
        ambient_light = AmbientLight('ambientLight')
        ambient_light.setColor((0.3, 0.3, 0.3, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))
        
        # Directional light
        directional_light = DirectionalLight('directionalLight')
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        directional_light.setDirection((1, 1, -1))
        self.render.setLight(self.render.attachNewNode(directional_light))
    
    def load_assets(self):
        """Load 3D models and textures"""
        # Placeholder for asset loading
        # In a real game, you'd load actual 3D models here
        print("Loading assets...")
        
        # Create simple placeholder models
        self.player_model = self.create_cube_model((1, 0, 0, 1))  # Red cube for player
        self.boss_model = self.create_cube_model((1, 0.5, 0, 1))   # Orange cube for boss
        self.resource_model = self.create_sphere_model((0, 1, 0, 1))  # Green sphere for resources
        self.terrain_model = self.create_plane_model((0.5, 0.5, 0.5, 1))  # Gray plane for terrain
    
    def create_cube_model(self, color):
        """Create a simple colored cube"""
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData('cube', format, Geom.UHStatic)
        
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')
        
        # Define cube vertices
        vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # back
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)       # front
        ]
        
        # Define cube faces
        faces = [
            (0, 1, 2, 3),  # back
            (4, 7, 6, 5),  # front
            (0, 4, 5, 1),  # bottom
            (2, 6, 7, 3),  # top
            (0, 3, 7, 4),  # left
            (1, 5, 6, 2)   # right
        ]
        
        # Add vertices and faces
        for v in vertices:
            vertex.addData3f(v[0], v[1], v[2])
            normal.addData3f(v[0], v[1], v[2])
            color_writer.addData4f(color)
        
        geom = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        
        for face in faces:
            tris.addVertices(face[0], face[1], face[2])
            tris.addVertices(face[0], face[2], face[3])
        
        geom.addPrimitive(tris)
        node = GeomNode('cube')
        node.addGeom(geom)
        
        return NodePath(node)
    
    def create_sphere_model(self, color):
        """Create a simple colored sphere"""
        # Simplified sphere creation
        return self.create_cube_model(color)  # Using cube as placeholder
    
    def create_plane_model(self, color):
        """Create a simple colored plane"""
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData('plane', format, Geom.UHStatic)
        
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')
        
        # Create a flat plane
        size = 10
        vertices = [
            (-size, -size, 0), (size, -size, 0),
            (size, size, 0), (-size, size, 0)
        ]
        
        for v in vertices:
            vertex.addData3f(v[0], v[1], v[2])
            normal.addData3f(0, 0, 1)
            color_writer.addData4f(color)
        
        geom = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        tris.addVertices(0, 1, 2)
        tris.addVertices(0, 2, 3)
        
        geom.addPrimitive(tris)
        node = GeomNode('plane')
        node.addGeom(geom)
        
        return NodePath(node)
    
    def create_world(self):
        """Create the 3D game world"""
        # Create terrain
        self.terrain = self.terrain_model.copyTo(self.render)
        self.terrain.setPos(0, 0, 0)
        self.terrain.setScale(5, 5, 1)
        
        # Create players
        self.create_player((-3, 0, 1), (1, 0, 0, 1))  # Player 1 (red)
        self.create_player((3, 0, 1), (0, 0, 1, 1))   # Player 2 (blue)
        
        # Create some resources
        for i in range(5):
            pos = (random.uniform(-8, 8), random.uniform(-8, 8), 1)
            self.create_resource(pos)
    
    def create_player(self, position, color):
        """Create a player character"""
        player = self.player_model.copyTo(self.render)
        player.setPos(position[0], position[1], position[2])
        player.setScale(0.5)
        
        player_data = {
            'node': player,
            'position': position,
            'velocity': (0, 0, 0),
            'health': 100,
            'stamina': 100,
            'color': color
        }
        
        self.game_state['players'].append(player_data)
        return player_data
    
    def create_resource(self, position):
        """Create a resource node"""
        resource = self.resource_model.copyTo(self.render)
        resource.setPos(position[0], position[1], position[2])
        resource.setScale(0.3)
        
        resource_data = {
            'node': resource,
            'position': position,
            'type': random.choice(['wood', 'stone', 'crystal']),
            'value': random.randint(1, 5)
        }
        
        self.game_state['resources'].append(resource_data)
        return resource_data
    
    def setup_controls(self):
        """Setup keyboard controls"""
        self.keys = {
            'w': False, 'a': False, 's': False, 'd': False,  # Player 1
            'arrow_up': False, 'arrow_left': False, 'arrow_down': False, 'arrow_right': False  # Player 2
        }
        
        self.accept('w', self.set_key, ['w', True])
        self.accept('w-up', self.set_key, ['w', False])
        self.accept('a', self.set_key, ['a', True])
        self.accept('a-up', self.set_key, ['a', False])
        self.accept('s', self.set_key, ['s', True])
        self.accept('s-up', self.set_key, ['s', False])
        self.accept('d', self.set_key, ['d', True])
        self.accept('d-up', self.set_key, ['d', False])
        
        self.accept('arrow_up', self.set_key, ['arrow_up', True])
        self.accept('arrow_up-up', self.set_key, ['arrow_up', False])
        self.accept('arrow_left', self.set_key, ['arrow_left', True])
        self.accept('arrow_left-up', self.set_key, ['arrow_left', False])
        self.accept('arrow_down', self.set_key, ['arrow_down', True])
        self.accept('arrow_down-up', self.set_key, ['arrow_down', False])
        self.accept('arrow_right', self.set_key, ['arrow_right', True])
        self.accept('arrow_right-up', self.set_key, ['arrow_right', False])
        
        self.accept('escape', self.quit_game)
    
    def set_key(self, key, value):
        """Set keyboard state"""
        self.keys[key] = value
    
    def update(self, task):
        """Main game update loop"""
        if not self.game_state['running']:
            return Task.done
        
        dt = globalClock.getDt()
        
        # Update players
        self.update_players(dt)
        
        # Update game state
        self.update_game_state(dt)
        
        return Task.cont
    
    def update_players(self, dt):
        """Update player movement and actions"""
        speed = 5.0 * dt
        
        # Player 1 movement (WASD)
        player1 = self.game_state['players'][0]
        move_dir = [0, 0, 0]
        
        if self.keys['w']: move_dir[1] += speed  # Forward
        if self.keys['s']: move_dir[1] -= speed  # Backward
        if self.keys['a']: move_dir[0] -= speed  # Left
        if self.keys['d']: move_dir[0] += speed  # Right
        
        # Update position
        new_pos = (
            player1['position'][0] + move_dir[0],
            player1['position'][1] + move_dir[1],
            player1['position'][2] + move_dir[2]
        )
        
        player1['position'] = new_pos
        player1['node'].setPos(new_pos[0], new_pos[1], new_pos[2])
        
        # Player 2 movement (Arrow keys)
        if len(self.game_state['players']) > 1:
            player2 = self.game_state['players'][1]
            move_dir2 = [0, 0, 0]
            
            if self.keys['arrow_up']: move_dir2[1] += speed
            if self.keys['arrow_down']: move_dir2[1] -= speed
            if self.keys['arrow_left']: move_dir2[0] -= speed
            if self.keys['arrow_right']: move_dir2[0] += speed
            
            new_pos2 = (
                player2['position'][0] + move_dir2[0],
                player2['position'][1] + move_dir2[1],
                player2['position'][2] + move_dir2[2]
            )
            
            player2['position'] = new_pos2
            player2['node'].setPos(new_pos2[0], new_pos2[1], new_pos2[2])
    
    def update_game_state(self, dt):
        """Update overall game state"""
        # Check resource collection
        self.check_resource_collection()
        
        # Update camera to follow players
        self.update_camera()
    
    def check_resource_collection(self):
        """Check if players are collecting resources"""
        collection_radius = 1.5
        
        for player in self.game_state['players']:
            for resource in self.game_state['resources'][:]:
                dx = resource['position'][0] - player['position'][0]
                dy = resource['position'][1] - player['position'][1]
                dz = resource['position'][2] - player['position'][2]
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if distance < collection_radius:
                    print(f"Player collected {resource['type']} worth {resource['value']}")
                    resource['node'].removeNode()
                    self.game_state['resources'].remove(resource)
                    break
    
    def update_camera(self):
        """Update camera to follow the action"""
        if not self.game_state['players']:
            return
        
        # Simple camera following first player
        player_pos = self.game_state['players'][0]['position']
        self.camera.setPos(player_pos[0], player_pos[1] - 10, player_pos[2] + 5)
        self.camera.lookAt(player_pos[0], player_pos[1], player_pos[2])
    
    def quit_game(self):
        """Clean up and quit the game"""
        self.game_state['running'] = False
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up game resources"""
        for player in self.game_state['players']:
            player['node'].removeNode()
        
        for resource in self.game_state['resources']:
            resource['node'].removeNode()
        
        if self.terrain:
            self.terrain.removeNode()

# Run the game
if __name__ == "__main__":
    game = DominionRealms3D()
    game.run()
