import modules.world as world

import modules.items as items
import sys
import math

from . import sprite as sprite

from . import draw_obj as d_obj

sys.path.append("pyglet-1.2.4.whl")

import pyglet

import random

class entity(world.grid_obj):

    def __init__(self,name="Storm",sprites={"default":".//sprites//entities//storm.png"},coords=[0,0],tags=[["impassable"],["passive"]],visible=True,inventory_slots=[],level=1,health=[100,100]):

        world.grid_obj.__init__(self,sprites=sprites,coords=coords,tags=tags,visible=visible)
        
        self.inventory_slots = inventory_slots

        self.name = name

        weapon = self.search_slot("current_weapon")
        
        self.active_weapon = weapon.item

        self.obj_type = "entity"
        
        self.level = level

        self.my_turn = True

        self.pending_actions = []

        self.is_alive = True

    def move(self,direction=[0,0]):

        passable = self.check_passable(direction)

        if passable:

            self.coords[0] += direction[0]

            self.coords[1] += direction[1]

            self.update_position()

        return passable

    def move_to(self,coords=[0,0]):

        passable = self.check_passable(coords,mode="a")

        if passable:

            self.coords[0] = coords[0]

            self.coords[1] = coords[1]

            self.update_position()

    def search_slot(self,slot_name=None):

        if slot_name != None and self.inventory_slots != []:

            for slot in self.inventory_slots:

                if slot.name == slot_name:

                    return slot

    def act_exec(self):

        for action in self.pending_actions:

            action_s = action.split()

            if action_s[0] == "move":

                self.move(direction=[int(action_s[1]),int(action_s[2])])

            if action_s[0] == "move_to":

                self.move_to(coords=[int(action_s[1]),int(action_s[2])])

            if action_s[0] == "attack":

                pass

            self.pending_actions.remove(action)

        if self.in_battle:

            self.my_turn = False

    def ai_tick(self):

        direction = random.choice([[0,1],[-1,0],[1,0],[0,-1]])

        self.move(direction)

        for ent in self.parent.entities:

            if ent.coords != self.coords:

                print(str(ent.coords) + " " + ent.name)
                        
    def tick(self,delta = 100):

        print(self.pending_actions)

        if self.my_turn:

            self.ai_tick()

            self.act_exec()

            world.grid_obj.tick(self,delta)

        #self.say(self.name,100,[32,128])

    def draw(self):

        if self.is_alive == True:

            d_obj.draw_obj.draw(self)

    def change_area(self,new_area=None,spawn=[0,0]):

        if new_area != None:

            self.parent = new_area

            self.coords = spawn

    def attack(self,target=[0,0]):

        target = self.search_coords(target)

        self.active_weapon.attack(self,target)


class basic_ai():

    def __init__(self,parent=None):

        self.parent = parent

        self.directions = [[0,1],[-1,0],[1,0],[0,-1]]  # N, W, E, S

    def tick(self):

        pass


class sel_ai(basic_ai):

    def __init__(self,parent=None):

        basic_ai.__init__(self,parent=parent)

    def tick(self,delta=100):

        sel = self.parent.parent.selector.coords

        action = "move_to {} {}".format(str(sel[0]),str(sel[1]))

        self.parent.give_command(action)

class random_ai(basic_ai):

    def __init__(self,parent=None):

        basic_ai.__init__(self,parent=parent)

    def tick(self,delta=100):

        direction = random.choice(self.directions)

        action = "move {} {}".format(str(direction[0]),str(direction[1]))

        self.parent.give_command(action)

        self.parent.ready = True

        for direction in self.directions:

            targets = self.parent.search_coord(position=direction,mode="r")

            if targets != []:

                for target in targets:

                    if hasattr(target,"health") and not self.parent.in_battle:

                        self.parent.enter_combat(enemy=target)

        basic_ai.tick(self)

        

                

                

            

            
        
##class combat_entity(entity):
##
##    def __init__(self,name="Storm",sprites={"default":".//sprites//entities//storm.png"},coords=[0,0,0],tags=[],visible=True,inventory_slots=[],
##                 health=[500,500],energy=[100,100],air_mana=[75,75],ai = None):
##
##        entity.__init__(self,sprites=sprites,coords=coords,tags=tags,visible=visible,ai=ai,inventory_slots=inventory_slots)
##
##        self.name = name
##
##        self.energy = energy
##
##        self.health = health
##
##        self.obj_type = "combat_entity"
##
##        weapon = self.search_slot("current_weapon")
##
##        weapon = weapon.item
##
##        self.in_battle = False
##
##        self.ready = False
##
##    def attack(self,target=[0,0]):
##    
##        weapon = self.search_slot("current_weapon")
##
##        weapon = weapon.item
##
##        target = self.search_coords(target)
##
##        weapon.attack(self,target)
##
##    def draw(self):
##
##        d_obj.draw_obj.draw(self)
##
##        if self.is_alive == True:
##
##            self.say(str(self.health[0])+ "/" + str(self.health[1]),10,[32,112])
##
##    def give_command(self,command = None):
##
##        if command != None:
##
##            self.pending_actions.append(command)
##
##    def tick(self,delta):
##
##        if self.is_alive == True:
##
##            entity.tick(self,delta)
##
##            self.say(str(self.health[0])+ "/" + str(self.health[1]),100,[32,112])
##
##    def take_damage(self,amount=10):
##
##        self.health[0] -= amount
##
##        if self.health[0] <= 0:
##
##            self.is_alive = False

