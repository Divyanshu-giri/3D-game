from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class StickmanGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load models and set up the scene
        self.set_background_color(0.1, 0.1, 0.1)  # Dark background
        self.load_environment()
        
    def load_environment(self):
        # Load a simple environment model
        self.environ = self.loader.load_model("models/environment")
        self.environ.reparent_to(self.render)
        self.environ.set_scale(0.25, 0.25, 0.25)
        self.environ.set_pos(-8, 42, 0)
        
        # Add lighting
        ambient_light = AmbientLight("ambient_light")
        ambient_light.set_color((0.5, 0.5, 0.5, 1))
        self.render.set_light(self.render.attach_new_node(ambient_light))
        
        directional_light = DirectionalLight("directional_light")
        directional_light.set_color((1, 1, 1, 1))
        self.render.set_light(self.render.attach_new_node(directional_light))
        
    def update(self):
        # Game update logic goes here
        pass

if __name__ == "__main__":
    game = StickmanGame()
    game.run()
