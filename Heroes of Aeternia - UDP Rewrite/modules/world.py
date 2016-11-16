
test = "yes"

import random

from . import utilities as util

from . import sprite as sprite

list1 = util.read_text_file("lang/test.txt",True)

print(list1)

class grid_obj():

    def __init__(self,position=[0,1,0],sprite_path=".//sprites//test_sprite.png",opacity = 255,obj_id=1,tags=[],parent=None,tile_type=None,visible=True):

        self.position = position
        
        self.base_pixel_position = [self.position[0] * 64,self.position[1] * 32]

        self.sprite_path = sprite_path

        self.opacity = opacity

        self.obj_id = obj_id

        self.parent = parent

        self.sprite = sprite.sprite()

        self.tags = tags

        self.tile_type = tile_type

        self.visible = visible

        self.client_io = []

        self.obj_type = "grid"

        self.pending_actions = []

        if self.sprite != None:

            try:

                self.sprite.update_parent(self)

            except:

                pass

    def tick(self):

        pass

    def draw(self):

        if self.visible == True:

            try:

                self.sprite.draw()

            except:

                pass
        

class area():

    def __init__(self,contents=[],name="Zverograd Combat Academy",graphic_layer=2):

        self.contents = contents

        self.name = name

        self.highest_layer = 1

        self.graphic_layer = graphic_layer

        self.client_io = []

        self.obj_type = "area"

    def update_draw_order(self):

        highest_layer = []

        for obj in self.contents:

            highest_layer.append(obj.position[2])

        self.highest_layer = max(highest_layer)

    def draw(self):

        self.update_draw_order()

        for layer in range(0,self.highest_layer+1):

            for obj in self.contents:

                if obj.position[2] == layer:

                    try:

                        obj.draw()

                    except:

                        print("drawException: Tried to draw non-drawable object")

    def update_client_io(self):

        for obj in self.contents:

            if obj.client_io != []:

                self.client_io.extend(obj.client_io)

    def add_object(self,obj=None):

        if obj != None:

            self.contents.append(obj)

            obj.parent = self

            print(obj.parent)

    def tick(self):

        self.update_client_io()

        for obj in self.contents:

            obj.tick()

    def search(self,position=None,obj_id=None):

        outp = []

        if obj_id != None:

            for obj in self.contents:

                if obj.obj_id == obj_id:

                    outp.append(obj)

        if position[0]!=None:

            for obj in self.contents:

                if obj.position[0] == position[0]:

                    outp.append(obj)

        if position[1]!=None:

            for obj in self.contents:

                if obj.position[1] == position[1]:

                    outp.append(obj)

        return outp

    def add_action(self,controller=None,command=None):

        for obj in self.contents:

            if obj.control[0] == controller and obj.control[1] == True:

                obj.pending_actions.append(command)

                

                

        

        

class hitbox():

    def __init__(self,position = [0,0],size = [64,32],parent = None):

        self.position = position

        self.size = size

        self.parent = parent

    def check(self,x=None,y=None): # check(self) before you wreck(self)

        if x != None and y != None:

            if x >= self.position[0] and x <= self.position[0] + self.size[0]:

                print("x match" + str(self.position))

                if y >= self.position[1] and y <= self.position[1] + self.size[1]:

                    print("x + y match" + str(self.sprite.position))

            if y >= self.position[1] and y <= self.position[1] + self.size[1]:

                print("y match" + str(self.self.position))

    def update(self,new_position = [0,0],new_size = None):

        if self.parent != None:

            self.position = parent.base_pixel_position

        else:

            new_position = [0,0]

        if new_size != None:

            self.size = new_size


            

##class tile():
##
##    def __init__(self,position=[0,1,0],base_pixel_position=[0,0],sprite_path=".//sprites//test_sprite.png",opacity = 255,obj_id=1,tags=[],contents=[],parent_id=2,sprite=None,tile_type="tile"):
##
##        self.position = position # grid x, grid y, layer (z), pixel x base, pixel y base
##
##        self.base_pixel_position = [self.position[0] * 64,self.position[1] * 32]
##
##        self.sprite_path = sprite_path
##
##        self.obj_id = obj_id
##
##        self.tags = tags
##
##        self.parent_id = parent_id
##
##        self.sprite = sprite
##
##        self.opacity = opacity
##
##        self.mouse_interaction = [False,False] # hovered over, clicked on
##
##        self.tile_type = tile_type
##
##        if self.sprite != None:
##
##            try:
##
##                self.sprite.update_parent(self,new_image=True)
##
##            except:
##
##                pass
##
##    def tick(self):
##
##        pass
##
##    def to_attr_string(self):
##
##        attr_string = "tile position:{0} sprite_file:{1} tags:{2} object_id:{3} parent_id:{4} hitbox:{5} /tile".format(str(self.position),self.sprite_file,str(self.tags),str(self.obj_id),str(self.parent_id),str(self.hitbox))
##
##        return attr_string
##
##    def draw(self):
##
##        if self.sprite != None:
##
##            self.sprite.draw()
##
##    def update_sprite(self):
##
##        if self.sprite != None:
##
##            try:
##
##                self.sprite.update_parent(self)
##
##            except:
##
##                pass


class tile(grid_obj):

    pass
        


    

        

            

        

        

        

    




        

        
