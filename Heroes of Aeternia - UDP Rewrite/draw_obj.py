from . import sprite

import sys

sys.path.append("pyglet-1.2.4.whl")

import pyglet

import random

class draw_obj():

    def __init__(self,position=[0,0],visible=True,sprites={"default":".//sprites//test_sprite.png"},global_layer="world",local_layer=1,tile_layer=0,opacity=255,text_label=""):

        self.position = position

        self.visible = visible

        self.global_layer = global_layer

        self.local_layer = local_layer

        self.opacity = opacity

        self.obj_type = "draw_obj"

        self.sprite_images = {}

        self.sprite_paths = sprites

        for sprite in sprites:

            self.sprite_images[sprite] = pyglet.image.load(sprites[sprite])

        self.sprite = pyglet.sprite.Sprite(img = self.sprite_images["default"], x = self.position[0],y = self.position[1])

        self.sprite.opacity = self.opacity
        
        self.tile_layer = tile_layer

        #self.text_labels = [[pyglet.text.Label(str(self.position),x=self.position[0]+32,y=self.position[1]+112,anchor_x="center",anchor_y="bottom",width = 480,multiline=False),True,100,0,0]] # label object, visible, say time in ms, x offset, y offset

        self.text_labels = []

        self.current_sprite = "default"

    def draw(self):

        if self.visible:

            self.sprite.x = self.position[0]

            self.sprite.y = self.position[1]

            self.sprite.opacity = self.opacity

            self.sprite.draw()

            for label in self.text_labels:

                if label[1]:

                    label[0].x=self.position[0]+label[3]

                    label[0].y=self.position[1]+label[4]

                    label[0].draw()

    def say(self,text="test",say_time=10,offset=[32,112]):

        self.text_labels.append([pyglet.text.Label(text,x=self.position[0]+offset[0],y=self.position[1]+offset[1],anchor_x="center"),True,say_time,offset[0],offset[1]])

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

        for label in self.text_labels:

            if label[1] and label[2] > 0:

                label[2] -= delta

            if label[1] and label[2] <= 0:

                self.text_labels.remove(label)

    def __str__(self):

        s = self.obj_type

        return s

        


                

## ------ Old code, requires sprite module -----

##class draw_obj():
##
##    def __init__(self,position=[0,0],visible=True,sprite_path=".//sprites//test_sprite.png",sprite_image=None,global_layer="world",local_layer=1,tile_layer=0,opacity=255,text_label=""):
##
##        self.position = position
##
##        self.visible = visible
##
##        self.sprite_path = sprite_path
##
##        self.sprite_image = sprite_image
##
##        self.global_layer = global_layer
##
##        self.local_layer = local_layer
##
##        self.opacity = opacity
##
##        self.sprite = sprite.sprite(parent=self)
##        
##        self.tile_layer = tile_layer
##
##        self.text_labels = [[pyglet.text.Label(str(self.position),x=self.position[0]+32,y=self.position[1]+112,anchor_x="center",anchor_y="bottom",width = 480,multiline=False),True,100,0,0]]  # label object, visible, say time in ms, x offset, y offset
##
##    def draw(self):
##
##        if self.visible:
##
##            self.sprite.draw()
##
##            for label in self.text_labels:
##
##                if label[1]:
##
##                    label[0].x=self.position[0]+label[3]
##
##                    label[0].y=self.position[1]+label[4]
##
##                    label[0].draw()
##
##    def say(self,text="test",say_time=10,offset=[32,112]):
##
##        self.text_labels.append([pyglet.text.Label(text,x=self.position[0]+offset[0],y=self.position[1]+offset[1],anchor_x="center"),True,say_time,offset[0],offset[1]])
##
##    def tick(self,delta=100): # delta time in ms
##
##        for label in self.text_labels:
##
##            if label[1] and label[2] > 0:
##
##                label[2] -= delta
##
##            if label[1] and label[2] <= 0:
##
##                self.text_labels.remove(label)

        
