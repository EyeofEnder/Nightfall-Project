import modules.world as world

import modules.items as items

import sys,math,random

from . import sprite as sprite

from . import draw_obj as d_obj

from . import utilities as util

from . import gameplay as gp

sys.path.append("pyglet-1.2.4.whl")

import pyglet

class entity(world.grid_obj):

    def __init__(self,name="Storm",sprites={"default":".//sprites//entities//storm.png"},coords=[0,0,0],tags=[["impassable"],["passive"]],visible=True,inv_slots=[items.inv_slot(item=items.placeholder_weapon(),name="current_weapon")],level=1,health=[100,100],speed=5):

        world.grid_obj.__init__(self,sprites=sprites,coords=coords,tags=tags,visible=visible,inv_slots=inv_slots)

        self.module = "entities"

        self.name = name

        self.obj_type = "entity"
        
        self.level = level

        self.pending_actions = []

        self.is_alive = True

        self.turn_info = {"priority":1,"points":[1,1],"my_turn":True}

        self.health = health

        self.speed = speed   # [speed] = u/turn point

        self.add_text_label(name="name",text=self.name)

        self.add_text_label(name="health",text="{}/{}".format(str(self.health[0]),str(self.health[1])),offset=[32,96])

        self.target = None

    def move(self,direction=[0,0,0]):

##        print("move")

        if self.turn_info["my_turn"]:

            c = [self.coords[0],self.coords[1],self.coords[2]]

            passable = self.check_passable(direction)

            flat_distance = math.sqrt(direction[0]**2 + direction[1]**2)

            distance = math.ceil(math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2))

            if passable:

                self.coords[0] += direction[0]

                self.coords[1] += direction[1]

                self.coords[2] += direction[2]

                self.update_position()

                self.parent.move_obj(self,old_pos=c)

                self.turn_action(round(distance/self.speed,3))

##        print(self.turn_info["points"])

    def move_to(self,coords=[0,0]):

        pass

    def ai_tick(self):

##        print("ai_tick")

        directions = [[0,1,0],[-1,0,0],[1,0,0],[0,-1,0]]

        attack = False

        for d in directions:

            targets = self.search_coord(position=d,mode="r")

            if targets != []:

                for t in targets:

                    if t.obj_type == "entity" and t.is_alive:

                        print("Attacking {}".format(t.name))

                        self.attack(t)

                        attack = True

                if attack:

                    break

        if not attack:

            self.move(random.choice(directions))

    def turn(self):

        if self.is_alive:

            self.ai_tick()


        self.update_text_label("name",self.name)

        self.update_text_label("health","{}/{}".format(str(self.health[0]),str(self.health[1])))

    def tick(self,delta = 100):
            
        self.update_text_label("name",self.name)

        self.update_text_label("health","{}/{}".format(str(self.health[0]),str(self.health[1])))

        world.grid_obj.tick(self,delta)

    def draw(self):

        if self.is_alive == True:

            d_obj.draw_obj.draw(self)

    def change_area(self,new_area=None,spawn=[0,0,0]):

        if new_area != None:

            self.parent = new_area

            self.coords = spawn

    def turn_action(self,points=1):

        self.turn_info["points"][0] = round(self.turn_info["points"][0] - points,3)

        if self.turn_info["points"][0] <= 0:

            self.turn_info["my_turn"] = False

    def take_damage(self,damage=0,weapon=None,attacker=None):

        stack = 0

        for l in self.text_labels:

            if l.name == "dmg_log":

                stack += 16

        if damage not in ["miss","bounce","nullified","no_damage"]:

            if self.health[0] - damage > 0:

                self.health[0] -= damage

                self.add_text_label(name="dmg_log",text="-{}".format(str(damage)),offset=[32,128 + stack],say_time=2000)

                print("Hit {} with {} for {}".format(self.name,weapon.name,damage))

                return damage

            else:

                taken = self.health[0]

                self.health[0] = 0

                self.die(last_damage=damage,weapon=weapon,attacker=attacker)

                self.add_text_label(name="dmg_log",text="☠ -{} ☠".format(str(damage)),offset=[32,128],say_time=5000)

                print("Hit {} with {} for {}".format(self.name,weapon.name,taken))

                return taken

        else:

            self.add_text_label(name="dmg_log",text=damage,offset=[32,128 + stack],say_time=2000)

            print("Hit {} with {} for... 0".format(self.name,weapon.name))

            return damage

    def reset_turn(self):

        self.turn_info["my_turn"] = True

        self.turn_info["points"][0] = self.turn_info["points"][1]
                   
    def die(self,last_damage=0,weapon=None,attacker=None):

        self.is_alive = False

        self.passable = True

        print("{} got rekt by {} with {}".format(self.name,attacker.name,weapon.name))

        self.tbr = True

    def attack(self,target=None):

        distance = math.sqrt((self.coords[0]-target.coords[0])**2 + (self.coords[1]-target.coords[1])**2 + (self.coords[2]-target.coords[2])**2)

        weapon = self.search_slot("current_weapon").item

        print(weapon.name)

        if self.turn_info["my_turn"] and weapon != None:
##
##            if self.inv_slots["current_weapon"] != None:

            weapon.attack(self,target,distance,area=self.parent)

            if hasattr(weapon,"fire_rate"):

                self.turn_action(1/weapon.fire_rate)

            else:

                self.turn_action(0.2)

        print("{}'s turn points: {}/{}".format(self.name,self.turn_info["points"][0],self.turn_info["points"][1]))

    def attack_target(self):

        if self.target != None:

            if hasattr(self.target,"health"):

                self.attack(self.target)

            elif type(self.target) in (list,tuple):

                print(self.target)

##    def to_string(self):
##
##        slots = []
##
##        for slot in self.inv_slots:
##
##            slots.append(slot.to_string())
##
##        slots = str(slots).replace('"',"")
##
##        s = "ent.{}(name='{}',inv_slots={},coords={},sprites={},tags={})".format(self.__class__.__name__,self.name,slots,str(self.coords),str(self.sprites),str(self.tags))
##
##        return s
        
class player_test(entity):

    def turn(self):

        pass

    def attack_selected(self):

        sel = self.parent.selected_object

        if sel != None:

            for o in sel:

                if o.obj_type == "entity" and o.is_alive:

                    self.target = o

                    self.attack_target()

        else:

            self.target = None

    def tick(self,delta = 100):
            
        self.update_text_label("name",self.name)

        self.update_text_label("health","{}/{}".format(str(self.health[0]),str(self.health[1])))

        world.grid_obj.tick(self,delta)

    def ai_tick(self):

        pass

    def move_attack(self,direction=[0,0,0]):

        targets = self.search_coord(position=direction,mode="r")

        attack = False

        if targets != []:

            for t in targets:

                if t.obj_type == "entity" and t.is_alive:

                    print("Attacking {}".format(t.name))

                    self.attack(t)

                    attack = True

        if not attack:

            self.move(direction)


class npc(entity):

    def __init__(self,coords=[0,0,0],name = "random",race = "human", gender = "female",tags=[["impassable"],["invulnerable"],["passive"]],health=[100,100]):

        entity.__init__(self,coords=coords,name=name,tags=tags,health=health)

        self.str_keys = ["name","coords","inv_slots","tags","items","item"]

        if name == "random":

            if race == "human":

                if gender == "male":

                    first_name = random.choice(["Aaron","Adam","Alan","Adrian","Brandon","Ben","Brian","Benny","Chris","Dennis"])   # to be continued

                    self.tags.append(["male"])

                elif gender == "female":

                    first_name = random.choice(["Anne","Alina","Bella","Caroline","Charlotte","Denise","Ellen"]) # to be continued

                    self.tags.append(["female"])

                last_name = random.choice(["Adams","Baker","Clares"])  # to be continued

            elif race == "harpy":

                pass

            elif race == "centaur":

                pass

            elif race == "lamia":

                pass

            elif race == "elf":

                pass

            elif race == "dwarf":

                pass

            elif race == "merfolk":

                pass

        self.name = first_name + " " + last_name

        self.gender = gender

        self.race = race
                

class dummy(npc):

    def ai_tick(self):

        self.turn_action(1)
            

