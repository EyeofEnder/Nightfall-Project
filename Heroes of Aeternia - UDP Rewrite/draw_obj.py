from . import sprite

import sys

sys.path.append("pyglet-1.2.4.whl")

import pyglet

import random

class text_label(pyglet.text.Label):

    def __init__(self,text="test",position=[0,0],time=None,name="test",offset = [0,0]):

        self.time = time

        self.name = name

        self.offset = offset

        pyglet.text.Label.__init__(self,x=position[0],y=position[1],text=text,anchor_x = "center")

        

        

class draw_obj():

    def __init__(self,position=[0,0],visible=True,sprites={"default":".//sprites//test_sprite.png"},global_layer="world",local_layer=1,tile_layer=0,opacity=255):

        self.position = position

        self.visible = visible

        self.global_layer = global_layer

        self.local_layer = local_layer

        self.opacity = opacity

        self.obj_type = "draw_obj"

        self.sprite_images = {}

        self.sprites = sprites

        self.sprite_paths = sprites

        self.str_keys = ["name","coords","sprites","inv_slots","tags","items","item"]

        self.module = "draw_obj"

        for sprite in sprites:

            self.sprite_images[sprite] = pyglet.image.load(sprites[sprite])

        self.sprite = pyglet.sprite.Sprite(img = self.sprite_images["default"], x = self.position[0],y = self.position[1])

        self.sprite.opacity = self.opacity
        
        self.tile_layer = tile_layer

        ## label object, visible, say time in ms, x offset, y offset

        self.text_labels = []

        self.current_sprite = "default"

    def draw(self):

        if self.visible:

            self.sprite.opacity = self.opacity

            self.sprite.draw()

            for label in self.text_labels:

##                if label["visible"]:
##
##                    label["label"].x=self.position[0]+label["x_offset"]
##
##                    label["label"].y=self.position[1]+label["y_offset"]
##
##                    label["label"].draw()
##
                label.x=self.position[0]+label.offset[0]

                label.y=self.position[1]+label.offset[1]

                label.draw()

    def add_text_label(self,name = "name",say_time=None,offset=[32,112],text=None):

##        self.text_labels.append({"label":pyglet.text.Label(text,x=self.position[0]+offset[0],y=self.position[1]+offset[1],anchor_x="center"),"name":name,"say_time":say_time,"visible":True,"x_offset":offset[0],"y_offset":offset[1]})

        self.text_labels.append(text_label(name=name,text=text,time=say_time,position=[self.position[0] + offset[0],self.position[1] + offset[1]],offset=offset))

    def update_text_label(self,name=None,text=None):

        if name != None:

            for label in self.text_labels:

##                if label["name"] == name:
##
##                    label["label"].text = text

                 if label.name == name:

                    label.text = text


    def load_sprite(self,sprite_path = ".//sprites//test_sprite.png",name = "test"):   # loads from file path

        sprite_image = pyglet.image.load(sprite_path)

        self.sprite_images[name] = sprite_image

    def add_sprite(self,sprite = None,name = "test"):    #  adds from image file

        if sprite != None:

            self.sprite_images[name] = sprite

    def change_sprite(self,name = "default"):

        self.sprite.image = self.sprite_images[name]

        self.current_sprite = name

    def tick(self,delta=100): # delta time in ms

        if self.text_labels != []:

            for label in self.text_labels:

##                if label["say_time"] != None:
##
##                    if label["visible"] and label["say_time"] > 0:
##
##                        label["say_time"] -= delta
##
##                    if label["visible"] and label["say_time"] <= 0:
##
##                        self.text_labels.remove(label)

                 if label.time != None:

                    if label.time > 0:

                        label.time -= delta

                    if label.time <= 0:

                        self.text_labels.remove(label)


    def to_string(self):

        s = self.__class__.__name__

        a = self.__dict__
        
        a_filtered = {}

        at = []

        for key in a.keys():

            a_e = a[key]

            if key in self.str_keys:

                a_filtered[key] = a_e

##        print(str(s) + " " + str(a1))

        for key in a_filtered.keys():

            a_e = a_filtered[key]

            if hasattr(a_e,"to_string"):

                a_e = a_e.to_string()

                at.append("{}={}".format(key,a_e))

            elif type(a_e) == list:

                l = "["

                index = 0

                for e in a_e:

                    if hasattr(e,"to_string"):

                        l += e.to_string()

                    else:

                        l += str(e) 

                    if index < len(a_e) - 1:

                        l += ","

                    index += 1

                l += "]"

                at.append("{}={}".format(key,l))

            elif type(a_e) == str:

                at.append("{}='{}'".format(key,a_e))

            else:

                at.append("{}={}".format(key,a_e))

##        print(self.module)

        ats = "{}(".format(s)

        index = 0

        ats += "\n"

        for e in at:

            ats += (e) 
##
##            if index < len(at) - 1:
##
##               ats += ","

            ats += "\n"

            index += 1

        ats += ")\n"

##        print("")
##
####        print(ats)
##
##        print("")

            

        return ats

        


                



        
