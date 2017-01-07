from . import world as world

import sys

from . import sprite as sprite

from . import utilities as util

import random

sys.path.append("pyglet-1.2.4.whl")

import pyglet

from . import draw_obj as d_obj


class item_slot():

    def __init__(self,parent=None,item=None,name = "inv01",has_item=False,sprites={"default":"sprites/item_slot.png"},position = [0,0],visible = True):

        self.item = item

        self.parent = parent

        self.name = name
        
        self.position = position

        self.sprites = sprites

        self.visible = visible

        if self.item != None:

            self.has_item = True

        else:

            self.has_item = False

    def draw(self):

        if self.visible:

            self.sprite.draw()

            #self.item.draw()

    def remove_item(self):

        self.item = None

        self.has_item = False

    def move_item(self,target_slot=None):

        self.item.move(target_slot)

        target_slot.has_item = True

        target_slot.item = self.item

        self.remove_item()


class item():

    def __init__(self,name="test item please ignore",count=[1,100],sprite_path=None,parent=None,tags=[]):

        self.name = name

        self.parent = parent

        self.count = count

        self.sprite_path = None

        self.tags = tags

        self.sprite_path = sprite_path

        self.sprite = sprite.sprite()

    def draw(self):

        if self.visible == True:

            self.sprite.draw()

    def move(self,new_parent=None):

        self.parent = new_parent

class item_sprite(d_obj.draw_obj):

    def __init__(self,item=None,position=[0,0],visible=False):

        self.item = item

        if item != None:

            d_obj.draw_obj.__init__(self,position=position,visible=visible,sprite_path=self.item.sprite_path,global_layer="gui",local_layer=1,tile_layer=0,opacity=255,text_label="")



            
    

class weapon(item):

    def __init__(self,name="One-Punch Gloves",count=[1,1],sprite_path=None,parent=None,tags=[],dmg_falloff = [[0,100],[100,50]],max_range = 50,acc_falloff = [[0,100],[100,20]],base_acc=60,base_dmg=12,base_pen=82):

        item.__init__(self,name=name,count=count,sprite_path=sprite_path,parent=parent,tags=tags)

        self.dmg_falloff = dmg_falloff

        self.base_dmg = base_dmg

        self.acc_falloff = acc_falloff

        self.base_acc = base_acc

        self.base_pen = base_pen

        self.max_range = max_range

    def attack(self,user=None,target=None):

        rand = random.randrange(1,101)

        print(target.name)

        if rand <= self.base_acc:

            print("Hit!")

            target.take_damage(target.health[0])

        else:

            print("Miss!")




        

        

        

    
