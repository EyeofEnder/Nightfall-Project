import modules.world as world

import modules.items as items
import sys

from . import sprite as sprite

sys.path.append("pyglet-1.2.4.whl")

import pyglet

class entity(world.grid_obj):

    def __init__(self,name="Storm",sprite_path=".//sprites//entities//storm.png",position=[0,0,0],tags=[],control=[None,True],visible=True,tile_type="entity",inventory_slots=[items.item_slot(name="current_weapon")]):

        world.grid_obj.__init__(self,sprite_path=sprite_path,position=position,tags=tags,visible=visible,tile_type=tile_type)

        self.control = control

        self.inventory_slots = inventory_slots

        self.name = name

        self.text_stats = [True,10]

        self.text_label = pyglet.text.Label("lol",x=self.position[0]*64+32,y=self.position[1]*32+112,anchor_x="center",anchor_y="bottom",width = 480,multiline=False)

    def move(self,direction=[0,0]):

        self.position[0] += direction[0]

        self.position[1] += direction[1]

        print(self.position)

        self.sprite.update_sprite()

    def say(self,text="Hello",say_time=10):

        self.text_stats = [True,say_time]

        self.text_label = pyglet.text.Label(text,x=self.position[0]*64+32,y=self.position[1]*32+112,anchor_x="center")

    def tick(self):

        print("tick")

        for action in self.pending_actions:

            print(action)

    def search_area(self,position=None,obj_id=None):

        return self.parent.search(position = position,obj_id=obj_id)

    def draw(self):

        if self.visible == True:

            try:

                self.sprite.draw()

            except:

                pass

        if self.text_stats[0] == True:

            self.text_label.draw()

class combat_entity(entity):

    def __init__(self,name="Storm",sprite_path=".//sprites//entities//storm.png",position=[0,0,0],tags=[],control=["player_EyeofEnder",True],visible=True,tile_type="entity",inventory_slots=[],
                 health=[100,100],energy=[100,100],air_mana=[75,75],attack=10):

        entity.__init__(self,sprite_path=sprite_path,position=position,tags=tags,visible=visible,tile_type=tile_type)

        self.control = control

        self.inventory_slots = inventory_slots

        self.name = name

        self.energy = energy

        self.attack = attack

        self.health = health
        

    def attack(self,entity=None):

        if entity != None:

            entity.health[0] -= self.attack
