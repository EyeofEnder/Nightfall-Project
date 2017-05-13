from . import world as world

import sys

from . import sprite as sprite

from . import utilities as util

import random

sys.path.append("pyglet-1.2.4.whl")

import pyglet

from . import draw_obj as d_obj

class inv_slot(d_obj.draw_obj):

    def __init__(self,item=None,name="test_slot",sprites={"default":".//sprites//item_slot.png"},position=[0,0]):

        self.name = name

        self.item = item

        d_obj.draw_obj.__init__(self,sprites=sprites,position=position)

        self.module = "items"

    def draw(self):

        d_obj.draw_obj.draw()

        if self.item != None:

            self.item.position = self.position

            self.item.draw()

##    def to_string(self):
##
##        s = "items.inv_slot(name='{}',item={})".format(self.name,"items."+self.item.to_string())
##
##        return s
            

class item(d_obj.draw_obj):

    def __init__(self,name="test item please ignore",count=[1,100],sprites = {"default":".//sprites//weapons//lauras_sword.png"},parent=None,tags=[]):

        self.name = name

        d_obj.draw_obj.__init__(self,sprites=sprites)

        self.parent = parent

        self.count = count

        self.sprite_path = None

        self.tags = tags

        self.module = "items"

    def tick(self,dt=100):

##        print(self.name)

        pass

    def draw(self):

        if self.visible == True:

            self.sprite.draw()

    def move(self,new_parent=None):

        self.parent = new_parent

    def attack(self,user=None,target=None,area=None,distance=None):

        print("It's not very effective...")

        taken = target.take_damage(damage="no_damage",weapon=self,attacker=user)

##    def to_string(self):
##
##        out = "item(name='{}',count={},sprites={},parent=None,tags={})".format(self.name,str(self.count),str(self.sprites),str(self.tags))
##
##        return out

class item_sprite(d_obj.draw_obj):

    def __init__(self,item=None,position=[0,0],visible=False):

        self.item = item

        if item != None:

            d_obj.draw_obj.__init__(self,position=position,visible=visible,sprite_path=self.item.sprite_path,global_layer="gui",local_layer=1,tile_layer=0,opacity=255,text_label="")



            
    

class weapon(item):

    def __init__(self,name="One-Punch Gloves",count=[1,1],sprites={"default":".//sprites//weapons//lauras_sword.png"},parent=None,tags=[],dmg_falloff = [[0,100],[100,50]],max_range = 50,acc_falloff = [[0,100],[100,20]],base_acc=60,base_dmg=12,base_pen=82,fire_rate=10):

        item.__init__(self,name=name,count=count,sprites=sprites,parent=parent,tags=tags)

        self.dmg_falloff = dmg_falloff

        self.base_dmg = base_dmg

        self.acc_falloff = acc_falloff

        self.base_acc = base_acc

        self.base_pen = base_pen

        self.max_range = max_range

        self.fire_rate = fire_rate # attacks / turn point

    def attack(self,user=None,target=None,distance=None,area=None):

        if distance == None:

            distance = math.sqrt((user.coords[0]-target.coords[0])**2 + (user.coords[1]-target.coords[1])**2 + (user.coords[1]-target.coords[1])**2)

##        print("Range:"+str(distance))

##        print(area.name)

        rand = random.randrange(1,101)

        if rand <= self.base_acc:

            taken = target.take_damage(damage=self.base_dmg,weapon=self,attacker=user)

            hit = True

        else:

            taken = target.take_damage(damage="miss",weapon=self,attacker=user)

            print("Miss!")

            hit = False


class placeholder_weapon(weapon):

    def __init__(self,name="His/Her Bare Hands",max_range=1,base_dmg=5,base_pen=10,fire_rate=15):

        weapon.__init__(self,name=name,max_range=max_range,base_dmg=base_dmg,base_pen=base_pen,fire_rate=fire_rate)

    def tick(self,dt=100):

        weapon.tick(self,dt=dt)

##        if self.parent.gender=="female":
##
##            prefix = "Her"
##
##        if self.parent.gender=="male":
##
##            prefix="His"
##
##        if self.parent.race=="harpy":
##
##            part="Wings"
##
##        else:
##
##            part="Hands"
##
##        self.name = "{} Bare {}".format(prefix,part)


        

        

        

    
