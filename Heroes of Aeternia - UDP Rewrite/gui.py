from . import utilities as util

from . import draw_obj as draw_obj

class gui_layer():

    def __init__(self,components=[],visible=True):

        self.layer = layer

        self.components = components

        self.visible = visible

        self.obj_type = "gui"

    def draw(self):
        
        if self.visible == True:

            for component in self.components:

                try:
                    
                    component.draw()

                except:

                    pass

    def add_component(self,component):

        component.parent = self

        self.components.append(component)

    def tick(self):

        pass

class gui_component(draw_obj.draw_obj):

    def __init__(self,position=[0,0],parent=None,visible=True,local_layer=0,sprite=None,sprite_path="sprites/test_gui.png",global_layer="gui"):

        draw_obj.draw_obj.__init__(self,position = position,local_layer = local_layer)

    def draw(self):

        if self.visible == True:

            if self.parent != None:

                self.layer = self.parent.layer

                self.visible = self.parent.visible

            self.sprite.draw()

def create_gui():

    pass

    

        

        

    
