from . import utilities as util

class gui():

    def __init__(self,components=[],layer=0,visible=True):

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

class sprite_component():

    def __init__(self,position=[0,1],parent=None,visible=True,layer=0,sprite=None,sprite_path="sprites/test_gui.png"):

        self.position = position

        self.layer = layer

        self.parent = parent

        self.sprite = sprite

        self.visible = visible

        self.sprite_path = sprite_path

        if self.sprite != None:

            self.sprite.update_parent(new_parent = self)

        if self.parent != None:

            self.layer = self.parent.layer

            self.visible = self.parent.visible

    def draw(self):

        if self.visible == True:

            if self.parent != None:

                self.layer = self.parent.layer

                self.visible = self.parent.visible

            self.sprite.draw()

        

        

    
