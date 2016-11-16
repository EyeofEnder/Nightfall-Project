import modules.world as world

import sys

from . import sprite as sprite

sys.path.append("pyglet-1.2.4.whl")

import pyglet


class item_slot():

    def __init__(self,parent=None,item=None,name = "inv01",has_item=False):

        self.item = item

        self.parent = parent

        self.name = name

        if self.item != None:

            self.has_item = True

        else:

            self.has_item = False

    def remove_item(self):

        self.item = None

        self.has_item = False

    def move_item(self,target_slot=None):

        self.item.move(target_slot)

        target_slot.has_item = True

        target_slot.item = self.item

        self.remove_item()


class item():

    def __init__(self,name="test item please ignore",count=[1,100],sprite_path=None,parent=None,position=[0,0],visible=False,tags=[]):

        self.name = name

        self.parent = parent

        self.count = count

        self.sprite_path = None

        self.tags = tags

        self.sprite = sprite.sprite()

        print(self.name)

    def draw(self):

        if self.visible == True:

            self.sprite.draw()

    def move(self,new_parent=None):

        self.parent = new_parent

class weapon(item):

    def __init__(self,name="test item please ignore",count=[1,1],sprite_path=None,parent=None,position=[0,0],visible=False,tags=[],damage=):

        item.__init__(name=name,count=count,sprite_path=sprite_path,parent=parent,position=position,visible=visible,tags=tags)

    
