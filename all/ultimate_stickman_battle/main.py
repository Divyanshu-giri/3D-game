from panda3d.core import *
from panda3d.core import GeomVertexWriter, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomNode
from panda3d.core import AmbientLight, DirectionalLight, PointLight, NodePath, Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from panda3d.core import ClockObject
import sys
import random
import math
import time

class UltimateStickmanBattle(ShowBase):
    def __init__(self):
        print("Initializing the game...")
        ShowBase.__init__(self)
        
        # Game configuration
        self.window_size = (1024, 768)
        self.game_state = {
            'running': True,
            'players': [],
            'boss': None,
            'resources': [],
            'terrain': None,
            'phase': 'arena',
            'score': {'player1': 0, 'player2': 0},
            'timer': 0,
            'echoes': []
        }
        
        # Setup systems
        self.setup_camera()
        self.setup_lighting()
        self.load_assets()
        self.create_arena()
        self.setup_controls()
        self.setup_ui()
        
        # Start game loop
        self.taskMgr.add(self.update, "updateGame")
    
    def setup_camera(self):
        """Setup the 3D camera with dynamic positioning"""
        self.disableMouse()
        self.camera.setPos(0, -25, 15)
        self.camera.lookAt(0, 0, 5)
        
    def setup_lighting(self):
        """Setup dynamic 3D lighting"""
        # Ambient light
        ambient_light = AmbientLight('ambientLight')
        ambient_light.setColor((0.4, 0.4, 0.4, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))
        
        # Directional light (main sun)
        directional_light = DirectionalLight('directionalLight')
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        directional_light.setDirection((1, 1, -0.5))
        self.dlight_node = self.render.attachNewNode(directional_light)
        self.render.setLight(self.dlight_node)
        
        # Point light for special effects
        point_light = PointLight('pointLight')
        point_light.setColor((1, 0.5, 0, 1))
        point_light_node = self.render.attachNewNode(point_light)
        point_light_node.setPos(0, 0, 10)
        self.render.setLight(point_light_node)
    
    def setup_ui(self):
        """Setup game UI elements"""
        print("Setting up UI...")
        
        # Health bars
        try:
            self.health_bars = {
                'player1': DirectWaitBar(range=100, pos=(-0.8, 0, -0.9), 
                                       frameColor=(0.5, 0.5, 0.5, 1), 
                                       barColor=(1, 0, 0, 1)),
                'player2': DirectWaitBar(range=100, pos=(0.8, 0, -0.9), 
                                       frameColor=(0.5, 0.5, 0.5, 1), 
                                       barColor=(0, 0, 1, 1))
            }
            
            # Initialize health values
            self.health_bars['player1']['value'] = 100
            self.health_bars['player2']['value'] = 100
            print("Health bars created successfully")
        except Exception as e:
            print(f"Error creating health bars: {e}")
            # Fallback to simple text displays
            self.health_bars = {
                'player1': DirectLabel(text="P1 Health: 100", pos=(-0.8, 0, -0.9), 
                                     text_scale=0.05, text_fg=(1, 0, 0, 1)),
                'player2': DirectLabel(text="P2 Health: 100", pos=(0.8, 0, -0.9), 
                                     text_scale=0.05, text_fg=(0, 0, 1, 1))
            }
        
        # Score display
        self.score_text = DirectLabel(text="0 - 0", pos=(0, 0, 0.9), 
                                    text_scale=0.1, text_fg=(1, 1, 1, 1))
        print("UI setup complete")
    
    def load_assets(self):
        """Load and create 3D models for the game"""
        print("Loading game assets...")
        
        # Create player models with different colors
        self.player_models = {
            'red': self.create_stickman_model((1, 0, 0, 1)),    # Player 1
            'blue': self.create_stickman_model((0, 0, 1, 1)),   # Player 2
            'green': self.create_stickman_model((0, 1, 0, 1)),  # Possible third player
        }
        
        # Create weapon models
        self.weapon_models = {
            'sword': self.create_weapon_model('sword'),
            'nunchaku': self.create_weapon_model('nunchaku'),
            'staff': self.create_weapon_model('staff'),
            'fists': self.create_weapon_model('fists')
        }
        
        # Create environment models
        self.terrain_model = self.create_arena_model()
        self.resource_model = self.create_resource_model()
        self.boss_model = self.create_boss_model()
    
    def create_stickman_model(self, color):
        """Create a 3D stickman model"""
        # Create a simple stick figure using cylinders and spheres
        stickman_node = NodePath('stickman')
        
        # Head (sphere)
        head = self.create_sphere(0.5, color)
        head.reparentTo(stickman_node)
        head.setPos(0, 0, 3.5)
        
        # Body (cylinder)
        body = self.create_cylinder(0.3, 2.5, color)
        body.reparentTo(stickman_node)
        body.setPos(0, 0, 1.5)
        
        # Arms
        left_arm = self.create_cylinder(0.2, 1.5, color)
        left_arm.reparentTo(stickman_node)
        left_arm.setPos(-0.8, 0, 2.5)
        left_arm.setHpr(-45, 0, 0)
        
        right_arm = self.create_cylinder(0.2, 1.5, color)
        right_arm.reparentTo(stickman_node)
        right_arm.setPos(0.8, 0, 2.5)
        right_arm.setHpr(45, 0, 0)
        
        # Legs
        left_leg = self.create_cylinder(0.2, 1.5, color)
        left_leg.reparentTo(stickman_node)
        left_leg.setPos(-0.3, 0, 0.5)
        left_leg.setHpr(0, 0, -10)
        
        right_leg = self.create_cylinder(0.2, 1.5, color)
        right_leg.reparentTo(stickman_node)
        right_leg.setPos(0.3, 0, 0.5)
        right_leg.setHpr(0, 0, 10)
        
        return stickman_node
    
    def create_weapon_model(self, weapon_type):
        """Create 3D weapon models"""
        weapon_node = NodePath(weapon_type)
        
        if weapon_type == 'sword':
            # Sword blade
            blade = self.create_box(0.2, 0.2, 2.0, (0.8, 0.8, 0.8, 1))
            blade.reparentTo(weapon_node)
            blade.setPos(0, 0, 1.0)
            
            # Sword hilt
            hilt = self.create_box(0.3, 0.3, 0.5, (0.5, 0.3, 0.1, 1))
            hilt.reparentTo(weapon_node)
            hilt.setPos(0, 0, -0.25)
            
        elif weapon_type == 'nunchaku':
            # First ball
            ball1 = self.create_sphere(0.3, (0.5, 0.3, 0.1, 1))
            ball1.reparentTo(weapon_node)
            ball1.setPos(-0.5, 0, 0)
            
            # Second ball
            ball2 = self.create_sphere(0.3, (0.5, 0.3, 0.1, 1))
            ball2.reparentTo(weapon_node)
            ball2.setPos(0.5, 0, 0)
            
            # Chain (simplified)
            chain = self.create_cylinder(0.05, 1.0, (0.3, 0.3, 0.3, 1))
            chain.reparentTo(weapon_node)
            
        elif weapon_type == 'staff':
            # Staff shaft
            shaft = self.create_cylinder(0.1, 2.0, (0.1, 0.1, 0.5, 1))
            shaft.reparentTo(weapon_node)
            
            # Staff crystal
            crystal = self.create_sphere(0.3, (0.8, 0.8, 1.0, 0.8))
            crystal.reparentTo(weapon_node)
            crystal.setPos(0, 0, 1.0)
            
        elif weapon_type == 'fists':
            # Simple fists (just use the arm model)
            pass
            
        return weapon_node
    
    def create_arena_model(self):
        """Create the battle arena"""
        arena_node = NodePath('arena')
        
        # Ground plane
        ground = self.create_box(20, 20, 0.5, (0.3, 0.6, 0.3, 1))
        ground.reparentTo(arena_node)
        ground.setPos(0, 0, -0.25)
        
        # Arena walls
        wall_colors = [(0.6, 0.4, 0.2, 1), (0.5, 0.3, 0.1, 1), (0.4, 0.2, 0.0, 1)]
        
        # North wall
        north_wall = self.create_box(20, 1, 3, wall_colors[0])
        north_wall.reparentTo(arena_node)
        north_wall.setPos(0, 10.5, 1.5)
        
        # South wall
        south_wall = self.create_box(20, 1, 3, wall_colors[0])
        south_wall.reparentTo(arena_node)
        south_wall.setPos(0, -10.5, 1.5)
        
        # East wall
        east_wall = self.create_box(1, 20, 3, wall_colors[1])
        east_wall.reparentTo(arena_node)
        east_wall.setPos(10.5, 0, 1.5)
        
        # West wall
        west_wall = self.create_box(1, 20, 3, wall_colors[2])
        west_wall.reparentTo(arena_node)
        west_wall.setPos(-10.5, 0, 1.5)
        
        # Add some obstacles
        obstacles = [
            ((-5, -5, 1), (2, 2, 2), (0.8, 0.6, 0.4, 1)),
            ((5, 5, 1), (1.5, 1.5, 3), (0.7, 0.5, 0.3, 1)),
            ((-7, 7, 0.5), (1, 1, 1), (0.9, 0.7, 0.5, 1))
        ]
        
        for i, (pos, size, color) in enumerate(obstacles):
            obstacle = self.create_box(size[0], size[1], size[2], color)
            obstacle.reparentTo(arena_node)
            obstacle.setPos(pos[0], pos[1], pos[2] + size[2]/2)
            obstacle.setName(f"obstacle_{i}")
        
        return arena_node
    
    def create_resource_model(self):
        """Create resource pickup models"""
        resource_node = NodePath('resource')
        
        # Energy crystal
        crystal = self.create_sphere(0.5, (1, 0.8, 0, 0.8))
        crystal.reparentTo(resource_node)
        
        # Add glow effect
        glow = self.create_sphere(0.7, (1, 1, 0.5, 0.3))
        glow.reparentTo(resource_node)
        
        return resource_node
    
    def create_boss_model(self):
        """Create boss enemy model"""
        boss_node = NodePath('boss')
        
        # Boss body (larger stickman)
        body = self.create_cylinder(0.8, 3.0, (1, 0.5, 0, 1))
        body.reparentTo(boss_node)
        body.setPos(0, 0, 1.5)
        
        # Boss head
        head = self.create_sphere(1.0, (1, 0.3, 0, 1))
        head.reparentTo(boss_node)
        head.setPos(0, 0, 3.5)
        
        # Boss arms (more menacing)
        left_arm = self.create_cylinder(0.4, 2.5, (1, 0.4, 0, 1))
        left_arm.reparentTo(boss_node)
        left_arm.setPos(-1.2, 0, 2.5)
        left_arm.setHpr(-60, 0, 0)
        
        right_arm = self.create_cylinder(0.4, 2.5, (1, 0.4, 0, 1))
        right_arm.reparentTo(boss_node)
        right_arm.setPos(1.2, 0, 2.5)
        right_arm.setHpr(60, 0, 0)
        
        # Boss legs
        left_leg = self.create_cylinder(0.4, 2.0, (1, 0.4, 0, 1))
        left_leg.reparentTo(boss_node)
        left_leg.setPos(-0.5, 0, 0.5)
        left_leg.setHpr(0, 0, -15)
        
        right_leg = self.create_cylinder(0.4, 2.0, (1, 0.4, 0, 1))
        right_leg.reparentTo(boss_node)
        right_leg.setPos(0.5, 0, 0.5)
        right_leg.setHpr(0, 0, 15)
        
        return boss_node
    
    def create_sphere(self, radius, color):
        """Create a colored sphere"""
        # Use Panda3D's built-in sphere creation instead of manual geometry
        sphere = self.loader.loadModel('models/smiley')
        if sphere:
            sphere.setScale(radius)
            sphere.setColor(color[0], color[1], color[2], color[3])
            return sphere
        else:
            # Fallback to simple sphere if model not available
            format = GeomVertexFormat.getV3n3c4()
            vdata = GeomVertexData('sphere', format, Geom.UHStatic)
            
            vertex = GeomVertexWriter(vdata, 'vertex')
            normal = GeomVertexWriter(vdata, 'normal')
            color_writer = GeomVertexWriter(vdata, 'color')
            
            # Create simple sphere vertices
            segments = 8
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                vertex.addData3f(x, y, 0)
                normal.addData3f(x, y, 0)
                color_writer.addData4f(color)
            
            geom = Geom(vdata)
            tris = GeomTriangles(Geom.UHStatic)
            
            # Create simple faces
            for i in range(segments - 2):
                tris.addVertices(0, i + 1, i + 2)
            
            geom.addPrimitive(tris)
            node = GeomNode('sphere')
            node.addGeom(geom)
            
            return NodePath(node)
    
    def create_cylinder(self, radius, height, color):
        """Create a colored cylinder"""
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData('cylinder', format, Geom.UHStatic)
        
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')
        
        # Create cylinder vertices
        segments = 8
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            # Top circle
            vertex.addData3f(x, y, height/2)
            normal.addData3f(x, y, 0)
            color_writer.addData4f(color)
            
            # Bottom circle
            vertex.addData3f(x, y, -height/2)
            normal.addData3f(x, y, 0)
            color_writer.addData4f(color)
        
        geom = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        
        # Create cylinder faces
        for i in range(segments):
            next_i = (i + 1) % segments
            # Side faces
            tris.addVertices(i*2, next_i*2, i*2+1)
            tris.addVertices(i*2+1, next_i*2, next_i*2+1)
            
            # Top face
            tris.addVertices(0, i*2, next_i*2)
            
            # Bottom face
            tris.addVertices(1, next_i*2+1, i*2+1)
        
        geom.addPrimitive(tris)
        node = GeomNode('cylinder')
        node.addGeom(geom)
        
        return NodePath(node)
    
    def create_box(self, width, depth, height, color):
        """Create a colored box"""
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData('box', format, Geom.UHStatic)
        
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')
        
        # Define box vertices
        half_w = width / 2
        half_d = depth / 2
        half_h = height / 2
        
        vertices = [
            (-half_w, -half_d, -half_h), (half_w, -half_d, -half_h),
            (half_w, half_d, -half_h), (-half_w, half_d, -half_h),
            (-half_w, -half_d, half_h), (half_w, -half_d, half_h),
            (half_w, half_d, half_h), (-half_w, half_d, half_h)
        ]
        
        # Define normals for each face
        normals = [
            (0, 0, -1), (0, 0, 1),  # front/back
            (-1, 0, 0), (1, 0, 0),   # left/right
            (0, -1, 0), (0, 1, 0)    # bottom/top
        ]
        
        # Add vertices with appropriate normals
        for v in vertices:
            vertex.addData3f(v[0], v[1], v[2])
            # Simple normal calculation
            normal_vec = Vec3(v[0], v[1], v[2])
            normal_vec.normalize()
            normal.addData3f(normal_vec)
            color_writer.addData4f(color)
        
        geom = Geom(vdata)
        tris = GeomTriangles(Geom.UHStatic)
        
        # Define box faces
        faces = [
            (0, 1, 2, 3),  # front
            (4, 7, 6, 5),  # back
            (0, 4, 5, 1),  # bottom
            (2, 6, 7, 3),  # top
            (0, 3, 7, 4),  # left
            (1, 5, 6, 2)   # right
        ]
        
        for face in faces:
            tris.addVertices(face[0], face[1], face[2])
            tris.addVertices(face[0], face[2], face[3])
        
        geom.addPrimitive(tris)
        node = GeomNode('box')
        node.addGeom(geom)
        
        return NodePath(node)
    
    def create_arena(self):
        """Create the game arena with terrain"""
        self.terrain = self.terrain_model.copyTo(self.render)
        
        # Create players
        print("Creating player 1...")
        player1 = self.create_player((-3, 0, 1), (1, 0, 0, 1), 'player1')  # Player 1 (red)
        print(f"Player 1 created: {player1}")
        
        print("Creating player 2...")
        player2 = self.create_player((3, 0, 1), (0, 0, 1, 1), 'player2')   # Player 2 (blue)
        print(f"Player 2 created: {player2}")
        
        print(f"Total players in game_state: {len(self.game_state['players'])}")
        
        # Create some resources
        for i in range(8):
            pos = (random.uniform(-8, 8), random.uniform(-8, 8), 1)
            self.create_resource(pos)
    
    def create_player(self, position, color, player_id):
        """Create a player character"""
        player_color = 'red' if color[0] > 0.5 else 'blue'
        player = self.player_models[player_color].copyTo(self.render)
        player.setPos(position[0], position[1], position[2])
        
        player_data = {
            'node': player,
            'position': position,
            'velocity': (0, 0, 0),
            'health': 100,
            'stamina': 100,
            'color': color,
            'player_id': player_id,
            'weapon': 'fists',
            'attack_cooldown': 0,
            'level': 1,
            'experience': 0,
            'facing_right': True,
            'on_ground': False,
            'is_jumping': False
        }
        
        self.game_state['players'].append(player_data)
        return player_data
    
    def create_resource(self, position):
        """Create a resource node"""
        resource = self.resource_model.copyTo(self.render)
        resource.setPos(position[0], position[1], position[2])
        
        resource_data = {
            'node': resource,
            'position': position,
            'type': random.choice(['wood', 'stone', 'crystal', 'metal', 'energy']),
            'value': random.randint(1, 10),
            'collected': False
        }
        
        self.game_state['resources'].append(resource_data)
        return resource_data
    
    def create_echo(self, action_type, position, color, delay=2.0):
        """Create an echo effect"""
        echo_data = {
            'action_type': action_type,
            'position': position,
            'color': color,
            'delay': delay,
            'spawn_time': time.time() + delay,
            'active': False,
            'lifetime': 3.0,
            'alpha': 255
        }
        
        self.game_state['echoes'].append(echo_data)
    
    def setup_controls(self):
        """Setup keyboard controls"""
        self.keys = {
            'w': False, 'a': False, 's': False, 'd': False,  # Player 1 movement
            'q': False,  # Player 1 attack
            'arrow_up': False, 'arrow_left': False, 'arrow_down': False, 'arrow_right': False,  # Player 2 movement
            'slash': False,  # Player 2 attack
            'space': False,  # Player 1 jump
            'enter': False   # Player 2 jump
        }
        
        # Player 1 controls
        self.accept('w', self.set_key, ['w', True])
        self.accept('w-up', self.set_key, ['w', False])
        self.accept('a', self.set_key, ['a', True])
        self.accept('a-up', self.set_key, ['a', False])
        self.accept('s', self.set_key, ['s', True])
        self.accept('s-up', self.set_key, ['s', False])
        self.accept('d', self.set_key, ['d', True])
        self.accept('d-up', self.set_key, ['d', False])
        self.accept('q', self.set_key, ['q', True])
        self.accept('q-up', self.set_key, ['q', False])
        self.accept('space', self.set_key, ['space', True])
        self.accept('space-up', self.set_key, ['space', False])
        
        # Player 2 controls
        self.accept('arrow_up', self.set_key, ['arrow_up', True])
        self.accept('arrow_up-up', self.set_key, ['arrow_up', False])
        self.accept('arrow_left', self.set_key, ['arrow_left', True])
        self.accept('arrow_left-up', self.set_key, ['arrow_left', False])
        self.accept('arrow_down', self.set_key, ['arrow_down', True])
        self.accept('arrow_down-up', self.set_key, ['arrow_down', False])
        self.accept('arrow_right', self.set_key, ['arrow_right', True])
        self.accept('arrow_right-up', self.set_key, ['arrow_right', False])
        self.accept('slash', self.set_key, ['slash', True])
        self.accept('slash-up', self.set_key, ['slash', False])
        self.accept('enter', self.set_key, ['enter', True])
        self.accept('enter-up', self.set_key, ['enter', False])
        
        self.accept('escape', self.quit_game)
    
    def set_key(self, key, value):
        """Set keyboard state"""
        self.keys[key] = value
    
    def update(self, task):
        """Main game update loop"""
        if not self.game_state['running']:
            return Task.done
        
        dt = self.taskMgr.globalClock.getDt()
        self.game_state['timer'] += dt
        
        # Update players
        self.update_players(dt)
        
        # Update echoes
        self.update_echoes()
        
        # Update game state
        self.update_game_state(dt)
        
        # Update UI
        self.update_ui()
        
        return Task.cont
    
    def update_players(self, dt):
        """Update player movement and actions"""
        speed = 8.0 * dt
        
        # Player 1 movement (WASD)
        if len(self.game_state['players']) > 0:
            player1 = self.game_state['players'][0]
            move_dir = [0, 0, 0]
            
            if self.keys['w']: move_dir[1] += speed  # Forward
            if self.keys['s']: move_dir[1] -= speed  # Backward
            if self.keys['a']: move_dir[0] -= speed  # Left
            if self.keys['d']: move_dir[0] += speed  # Right
            
            # Handle jumping
            if self.keys['space'] and player1['on_ground']:
                player1['velocity'] = (player1['velocity'][0], player1['velocity'][1], 8.0)
                player1['on_ground'] = False
                player1['is_jumping'] = True
                self.create_echo('jump', player1['position'], player1['color'], 1.0)
            
            # Handle attacking
            if self.keys['q'] and player1['attack_cooldown'] <= 0:
                player1['attack_cooldown'] = 0.5
                self.handle_attack(player1)
                self.create_echo('attack', player1['position'], player1['color'], 1.5)
            
            # Apply gravity
            player1['velocity'] = (
                player1['velocity'][0] * 0.9,  # Friction
                player1['velocity'][1] * 0.9,
                player1['velocity'][2] - 15.0 * dt  # Gravity
            )
            
            # Update position
            new_pos = (
                player1['position'][0] + move_dir[0] + player1['velocity'][0] * dt,
                player1['position'][1] + move_dir[1] + player1['velocity'][1] * dt,
                player1['position'][2] + player1['velocity'][2] * dt
            )
            
            # Ground collision
            if new_pos[2] < 0.5:
                new_pos = (new_pos[0], new_pos[1], 0.5)
                player1['velocity'] = (player1['velocity'][0], player1['velocity'][1], 0)
                player1['on_ground'] = True
                player1['is_jumping'] = False
            
            player1['position'] = new_pos
            player1['node'].setPos(new_pos[0], new_pos[1], new_pos[2])
            
            # Update attack cooldown
            if player1['attack_cooldown'] > 0:
                player1['attack_cooldown'] -= dt
        
        # Player 2 movement (Arrow keys)
        if len(self.game_state['players']) > 1:
            player2 = self.game_state['players'][1]
            move_dir2 = [0, 0, 0]
            
            if self.keys['arrow_up']: move_dir2[1] += speed
            if self.keys['arrow_down']: move_dir2[1] -= speed
            if self.keys['arrow_left']: move_dir2[0] -= speed
            if self.keys['arrow_right']: move_dir2[0] += speed
            
            # Handle jumping
            if self.keys['enter'] and player2['on_ground']:
                player2['velocity'] = (player2['velocity'][0], player2['velocity'][1], 8.0)
                player2['on_ground'] = False
                player2['is_jumping'] = True
                self.create_echo('jump', player2['position'], player2['color'], 1.0)
            
            # Handle attacking
            if self.keys['slash'] and player2['attack_cooldown'] <= 0:
                player2['attack_cooldown'] = 0.5
                self.handle_attack(player2)
                self.create_echo('attack', player2['position'], player2['color'], 1.5)
            
            # Apply gravity
            player2['velocity'] = (
                player2['velocity'][0] * 0.9,
                player2['velocity'][1] * 0.9,
                player2['velocity'][2] - 15.0 * dt
            )
            
            # Update position
            new_pos2 = (
                player2['position'][0] + move_dir2[0] + player2['velocity'][0] * dt,
                player2['position'][1] + move_dir2[1] + player2['velocity'][1] * dt,
                player2['position'][2] + player2['velocity'][2] * dt
            )
            
            # Ground collision
            if new_pos2[2] < 0.5:
                new_pos2 = (new_pos2[0], new_pos2[1], 0.5)
                player2['velocity'] = (player2['velocity'][0], player2['velocity'][1], 0)
                player2['on_ground'] = True
                player2['is_jumping'] = False
            
            player2['position'] = new_pos2
            player2['node'].setPos(new_pos2[0], new_pos2[1], new_pos2[2])
            
            # Update attack cooldown
            if player2['attack_cooldown'] > 0:
                player2['attack_cooldown'] -= dt
    
    def handle_attack(self, attacker):
        """Handle player attacks"""
        attack_range = 2.0
        damage = 10
        
        for player in self.game_state['players']:
            if player['player_id'] != attacker['player_id']:
                dx = player['position'][0] - attacker['position'][0]
                dy = player['position'][1] - attacker['position'][1]
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < attack_range:
                    player['health'] -= damage
                    if player['health'] <= 0:
                        player['health'] = 0
                        self.game_state['score'][attacker['player_id']] += 1
                        self.reset_player(player)
    
    def reset_player(self, player):
        """Reset player position and health"""
        player['health'] = 100
        player['position'] = (random.uniform(-8, 8), random.uniform(-8, 8), 0.5)
        player['node'].setPos(player['position'][0], player['position'][1], player['position'][2])
    
    def update_game_state(self, dt):
        """Update overall game state"""
        # Check for game over conditions
        if self.game_state['timer'] > 300:  # 5 minute time limit
            self.game_state['running'] = False
            print("Game over! Time's up!")
        
        # Check if any player has won
        if self.game_state['score']['player1'] >= 5:
            self.game_state['running'] = False
            print("Player 1 wins!")
        elif self.game_state['score']['player2'] >= 5:
            self.game_state['running'] = False
            print("Player 2 wins!")
    
    def update_echoes(self):
        """Update echo effects"""
        for echo in self.game_state['echoes'][:]:
            if echo['active']:
                # Handle fading and lifetime
                elapsed = time.time() - echo['spawn_time']
                if elapsed >= echo['lifetime']:
                    self.game_state['echoes'].remove(echo)
                else:
                    echo['alpha'] = max(0, 255 * (1 - elapsed / echo['lifetime']))
    
    def update_ui(self):
        """Update UI elements"""
        # Debugging: Print player states
        print("Updating UI...")
        print(f"Players: {self.game_state['players']}")
        
        # Only update UI if players exist
        if len(self.game_state['players']) >= 2:
            player1 = self.game_state['players'][0]
            player2 = self.game_state['players'][1]
            
            print(f"Player 1 Health: {player1['health']}, Player 2 Health: {player2['health']}")
            
            self.health_bars['player1']['value'] = player1['health']
            self.health_bars['player2']['value'] = player2['health']
            self.score_text['text'] = f"{self.game_state['score']['player1']} - {self.game_state['score']['player2']}"
    
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
    game = UltimateStickmanBattle()
    game.run()
