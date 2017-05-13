from . import utilities as util

from . import draw_obj as draw_obj

import sys  

sys.path.append("pyglet-1.2.4.whl")

import pyglet

class gui(draw_obj.draw_obj):

    def __init__(self,position=[0,0],parent=None,visible=True,sprites={"default":".//sprites//test_gui.png"},name = "test_gui",dimensions=[64,64],components=[],opacity=128,data={"text1":"test"},objects={"creator":None}):

        draw_obj.draw_obj.__init__(self,position = position,sprites = sprites,opacity=opacity)

        self.parent = parent

        self.name = name

        self.objects = objects

        self.dimensions = dimensions

        self.components = components

        self.tbr = False

        self.data = data

        for comp in self.components:

            comp.set_parent(self)

    def click(self,position=[0,0],button=1):

        for comp in self.components:

            if position[0] >= comp.position[0] and position[1] >= comp.position[1] and position[0] <= comp.position[0] + comp.dimensions[0] and position[1] <= comp.position[1] + comp.dimensions[1]:

                comp.click(position)

    def drag(self,position=[0,0],delta=[0,0]):

        for comp in self.components:

            if position[0] >= comp.position[0] and position[1] >= comp.position[1] and position[0] <= comp.position[0] + comp.dimensions[0] and position[1] <= comp.position[1] + comp.dimensions[1]:

                comp.drag(position,delta)

    def offset_func(self,delta=[0,0]):

        self.position = [self.position[0] + delta[0],self.position[1] + delta[1]]

        self.sprite.x, self.sprite.y = self.position[0], self.position[1]

        for comp in self.components:

            comp.update_position()

    def delete(self):

        self.components = []

        self.tbr = True

    def tick(self,dt=100):

        self.data["text1"] = ""

        if hasattr(self.objects["creator"],"inv_slots"):

            self.data["text1"] = self.data["text1"] + str(self.objects["creator"].inv_slots)

        for comp in self.components:

            comp.tick(dt)

    def draw(self):

        draw_obj.draw_obj.draw(self)

        for comp in self.components:

            comp.draw()

    def set_parent(self,parent=None):

        pass

    def add_component(self,component=None):

        component.set_parent(self)

    def update_position(self):

        pass

        

class drag_bar(gui):

    def __init__(self,parent=None,offset=[0,44],dimensions=[44,20]):  # relative position to parent

        self.offset = offset

        if parent != None: 

            self.position = [self.parent.position[0] + offset[0],self.parent.position[1] + offset[1]]

        else:

            self.position = [0,0]

        gui.__init__(self,position = self.position,dimensions=dimensions)

        self.dimensions = dimensions

    def click(self,position=[0,0]):

        pass

    def update_position(self):

        self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

        self.sprite.x, self.sprite.y = self.position[0], self.position[1]

    def set_parent(self,parent=None):

        if parent != None:

            self.parent = parent

            self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

    def draw(self):

        pass

    def tick(self,dt=100):

        pass

    def drag(self,position=[0,0],delta=[0,0]):

        self.parent.offset_func(delta)

class image(gui):

    def __init__(self,sprites={"default":".//sprites//weapons//lauras_sword.png"},offset=[0,0],dimensions=[64,64],name="img1",parent=None):

        self.parent = parent

        self.offset = offset

        if self.parent != None:

            self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

        else:

            self.position = [0,0]

        gui.__init__(self,position=self.position,parent=parent,name=name,sprites=sprites)

    def draw(self):

        draw_obj.draw_obj.draw(self)

    def update_position(self):

        self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

        self.sprite.x, self.sprite.y = self.position[0], self.position[1]

    def set_parent(self,parent=None):

        if parent != None:

            self.parent = parent

            self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

    def click(self,position=[0,0]):

        pass

    def tick(self,dt=100):

        pass

    def drag(self,position=[0,0],delta=[0,0]):

        self.parent.offset_func(delta)

        
class text_label(gui):

    def __init__(self,offset=[5,20],text="Placeholder",parent=None,name="text1"):

        self.text = text

        self.parent = parent

        self.offset = offset

        if self.parent != None:

            self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

        else:

            self.position = [0,0]

        gui.__init__(self,position=self.position,parent=parent,name=name)

##        self.add_text_label(name="label",text=text,offset=[0,0])

        self.label = pyglet.text.Label(text,x=self.position[0]+self.offset[0],y=self.position[1]+self.offset[1],anchor_x="left")

    def draw(self):

        self.label.draw()

    def set_parent(self,parent=None):

        if parent != None:

            self.parent = parent

            self.label.x = self.parent.position[0] + self.offset[0]

            self.label.y = self.parent.position[1] + self.offset[1]

    def update_position(self):

        self.label.x, self.label.y = self.parent.position[0] + self.offset[0], self.parent.position[1] + self.offset[1]

    def update_text(self,text="Text error. Please fix pls"):

        self.label.text = text

    def tick(self,dt=100):

        if self.name in self.parent.data.keys():

            text = str(self.parent.data[self.name])

            self.update_text(text=text)

    def click(self,position=[0,0]):

        pass
        

class button(gui):

    def __init__(self,parent=None,offset=[44,44],dimensions=[20,20],sprites={"default":".//sprites//close_gui.png"},opacity=255):  # relative position to parent

        self.offset = offset

        self.dimensions = dimensions

        if parent != None: 

            self.position = [self.parent.position[0] + offset[0],self.parent.position[1] + offset[1]]

        else:

            self.position = [0,0]

        gui.__init__(self,position = self.position,dimensions=dimensions,sprites=sprites,opacity=opacity)

    def set_parent(self,parent=None):

        if parent != None:

            self.parent = parent

            self.update_position()

    def update_position(self):

        self.position = [self.parent.position[0] + self.offset[0],self.parent.position[1] + self.offset[1]]

        self.sprite.x, self.sprite.y = self.position[0], self.position[1]

    def click(self,position=[0,0]):

        self.parent.delete()

    def tick(self,dt=100):

        pass

class kill_button(button):

    def __init__(self,offset=[0,0]):

        button.__init__(self,offset=offset)

    def click(self,position = [0,0]):

        self.parent.objects["player"].take_damage(1000000)

class 

        

        

    
