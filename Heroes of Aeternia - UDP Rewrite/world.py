import random,math,sys,time

from . import utilities as util

from . import sprite as sprite

from . import draw_obj as draw_obj

from . import gui as gui

from . import items as items

sys.path.append("pyglet-1.2.4.whl")

import pyglet

def direction(direction="n"):

    d = {"n":[0,1],"w":[-1,0],"e":[1,0],"s":[0,-1]}

    direction = d[direction.lower()]

    return direction

class grid_obj(draw_obj.draw_obj):

    def __init__(self,coords=[0,1,0],sprites={"default":".//sprites//block.png"},opacity = 255,tags=[["impassable"]],parent=None,visible=True,inv_slots=[],global_layer="world",name="world_block",additions=[]):

        self.tile_id = None

        self.coords = coords

        self.offset = [0,0]

        self.position = [(self.coords[0] * 64) + self.offset[0],(self.coords[1] * 32) + self.offset[1]]

        self.parent = parent

        self.tags = tags
        
        self.pending_actions = []

        self.name = name

        self.tbr = False
        
        self.obj_type = "grid_obj" 

        draw_obj.draw_obj.__init__(self,position=self.position,visible=visible,opacity=opacity,global_layer=global_layer,sprites=sprites)
        
        self.change_sprite("default")

        self.module = "world"

        self.additions = []

        self.timers = {}

        self.in_battle = False
    
        self.inv_slots = []

        self.inv_slot_names = []

        self.inv_slots = inv_slots
        
        for slot in self.inv_slots:

            slot.item.parent = self

        if additions != []:

            for add in additions:

                add.parent = self

                self.additions.append(add)

    
    def search_slot(self,name=None):

        slot = None

        if name != None and self.inv_slots != []:

            for slot in self.inv_slots:

                if slot.name == name:

                    print("Slot {} found.".format(name))

                    return slot


    def search_coord(self,position=[0,0,0],mode="r"):   # r = relative, a = absolute

        if mode == "r":

            c = (self.coords[0]+position[0],self.coords[1]+position[1],self.coords[2]+position[2])

            if c in self.parent.coord_list.keys():

                return self.parent.coord_list[c]

            else:

                return []

        elif mode == "a":

            if (position[0],position[1]) in self.parent.coord_list.keys():

                return self.parent.coord_list[(position[0],position[1])]

            else:

                return []

    def move(self,direction=[0,0,0]):

##        print("move")

        c = [self.coords[0],self.coords[1],self.coords[2]]

        passable = self.check_passable(direction)

        distance = math.ceil(math.sqrt(pow(direction[0],2) + pow(direction[1],2)))

        if passable:

            self.coords[0] += direction[0]

            self.coords[1] += direction[1]

            self.coords[2] += direction[2]

            self.update_position()

            self.parent.move_obj(self,old_pos=c)

            self.parent.update_draw_order()

    def update_position(self):

        self.position = [(self.coords[0] * 64) + self.offset[0],(self.coords[1] * 32) + self.offset[1]]

        self.sprite.x, self.sprite.y = self.position[0], self.position[1]

    def create_timer(self,name="tick",count=-1,starting_value=10,limit=0):

        self.timers[name] = [starting_value,count,limit]

    def create_gui(self,gui = None):

        self.parent.add_gui(gui=gui)

    def click(self,position=[0,0],button=1):

        if button == 4:

            self.create_gui(gui.gui(position=self.position,components=[gui.drag_bar(),gui.kill_button(),gui.text_label(text=self.name),gui.button()],data={"text1":self.position},objects={"creator":self,"player":self.parent.player}))

    def tick(self,delta):

        draw_obj.draw_obj.tick(self,delta)

        if self.timers != {}:

##            print(self.name,self.timers)

            over = []

            for key in self.timers.keys():

                self.timers[key][0] += self.timers[key][1]

                if self.timers[key][0] == self.timers[key][2]:

                    over.append(key)

            for key in over:

                del self.timers[key]
        
        #self.update_position()

        #print(self)

        if self.inv_slots != []:

            for slot in self.inv_slots:

                slot.item.tick(delta)

    def off_translate(self,offset=[0,0]):

        self.offset[0] += offset[0]

        self.offset[1] += offset[1]

        #  -- Uncomment for glitch art --
##
##        self.offset[0] += random.choice([1,-1])*offset[0]
##
##        self.offset[1] += random.choice([1,-1])*offset[1]

        self.update_position()
        
    def search_radius(self,r=2):

        pass

    def remove(self):    # REMOVE KEBAB

        self.tbr = True

    def find_distance(self,coords=[1,1,1]):

        distance = math.sqrt(pow(self.coords[0]-coords[0],2)+pow(self.coords[1]-coords[1],2))

        return distance

    def check_passable(self,coords=[1,1,0],mode="r"):

        passable = True

        check = self.search_coord([coords[0],coords[1],coords[2]],mode = mode)

        for c in check:

            for tag in c.tags:

                if "impassable" in tag:

                    passable = False

                    break


        return passable

    def add_addition(self,addition=None):

        addition.set_parent(self)

        self.children.append(addition)

        

##    def to_string(self):
##
##        add = []
##
##        slots = []
##
##        for a in self.additions:
##
##            add.append(a)
##
##        add = str(add).replace('"',"")
##
##        for slot in self.inv_slots:
##
##            slots.append(slot.to_string())
##
##        slots = str(slots).replace('"',"")
##
##        s = "world.{}(name='{}',inv_slots={},coords={},sprites={},additions={},tags={})".format(self.__class__.__name__,self.name,slots,str(self.coords),str(self.sprites),add,str(self.tags))

##    def __str__(self):
##
##        sp = ""
##
##        for k in self.sprites.keys():
##
##            sp += k + ":" + self.sprites[k]
##
##        c = str(self.coords).replace(" ","")
##
##        c = c.replace("[","")
##
##        c = c.replace("]","")
##
##        c = c.replace(","," ")
##
##        t = ""
##
##        for tg in self.tags:
##
##            t += str(tg).replace(" ","") + " "
##
##        sp = str(sp).replace(" ","")
##
##        s = "/{} /c {} /t {} /sp {} /id {}".format(self.obj_type,c,t,sp,str(self.tile_id),self.obj_type)

    def give_item(self,give_slot=None,recv_object=None,recv_slot=None):

        given_item = self.search_slot(give_slot).item

        if given_item != None and recv_object != None :

            recv_slot = recv_object.search_slot(recv_slot)

            if hasattr(recv_object,"inv_slots") and recv_slot != None:

                given_item.parent = recv_object

                recv_slot.item = given_item

                self.search_slot(give_slot).item = None

            
            
class multi_tile(grid_obj):

    def __init__(self):

        pass


class addition(grid_obj):

    def __init__(self,sprites={"default":".//sprites//test_vase.png"},tile_layer=10,parent=None,offset=[0,0]):  

        if parent != None:

            self.parent = parent

            self.coords = self.parent.coords

        else:

            self.coords = [0,0]

            self.parent = None

        grid_obj.__init__(self,sprites = sprites,coords = self.coords)

        self.offset = offset

        self.tile_layer = tile_layer

    def set_parent(self,parent=None):

        if parent != None:

            self.parent = parent

            self.coords = self.parent.coords

            self.position = [(self.coords[0] * 64) + self.parent.offset[0] + self.offset[0],(self.coords[1] * 32) + self.parent.offset[1] + self.offset[1]]

    def draw(self):

        self.coords = self.parent.coords

        self.position = [(self.coords[0] * 64) + self.parent.offset[0] + self.offset[0],(self.coords[1] * 32) + self.parent.offset[1] + self.offset[1]]

        draw_obj.draw_obj.draw(self)

    
class tile_cluster():

    def __init__(self,tiles=[]):

        self.batch = pyglet.graphics.Batch()

        self.groups = []

        temp_y = []

        for tile in tiles:

            tile.sprite.batch = self.batch

            temp_y.append(tile.coords[1])

        temp_y = max(temp_y)

        

    def draw(self):

        self.batch.draw()
    


def create_tile_line(point_1=[0,0],point_2=[0,1]):

    tiles = []

    if point_1 == point_2:

        tiles = tile(coords=[point_1[0],point_1[1]])

    elif point_1[0] == point_2[0]:

        for y in range(point_1[1],point_2[1]+1):

            tiles.append(tile(coords=[point_1[0],y]))

    elif point_1[1] == point_2[1]:

        for x in range(point_1[0],point_2[0]+1):

            tiles.append(tile(coords=[x,point_1[1]]))

    return tiles

def create_tile_structure(coords = [[1,0],[2,0]]):

    tiles = []

    for c in coords:

        tiles.append(tile(coords=c))

    return tiles


class selector(grid_obj):

    def __init__(self):

        grid_obj.__init__(self,sprites={"default":".//sprites//cubeselector.png"},visible=False,tags=[])

    def draw(self):

        self.update_position()

        draw_obj.draw_obj.draw(self)

class area():

    def __init__(self,children=[],name="Zverograd_Combat_Academy"):

        self.children = children

        self.name = name

        self.obj_type = "area"

        self.last_tile_id = 1

        self.coord_list = {}

        self.ids = {}

        self.drawable = []

        self.offset = [0,0]

        self.last_tick = 0

        self.entity_count = 0

        self.entities = []

        self.entity_n = 0

        self.new_ent = True

        self.gui = []

        self.current_z = 0

        self.player = None

        self.selected_object = []

        controlled_characters = {}

        self.selector = selector()

    def tick(self,dt=100):

        window_size = [1200,960]

        self.last_tick += 1

        for obj in self.children:

            obj.tick(dt)

            if obj.tbr:

                self.children.remove(obj)


        ent = self.entities[self.entity_n]

        if self.new_ent:

            ent.reset_turn()

        ent.turn()
            
        if self.last_tick >= 2:

            self.update_drawable()

        if not ent.turn_info["my_turn"] or not ent.is_alive:

            print("{}'s turn is over!".format(ent.name))

            if self.entity_n < (len(self.entities) - 1):  

                self.entity_n += 1

            else:

                self.entity_n = 0

            self.new_ent = True

        else:

            self.new_ent = False


        for gui in self.gui:

            gui.tick()

            if gui.tbr:

                self.gui.remove(gui)

##        print(str(self))

    def update_drawable(self):

        window_size = [1200,960]

        self.drawable = []

        for obj in self.children:

            if obj.position[0] + 64 >  0 and obj.position[1] + 96 > 0 and obj.position[0] <= window_size[0] and obj.position[1] <= window_size[1] and obj.coords[2] == self.current_z:

                self.drawable.append(obj)

            self.last_tick = 0

    def update_draw_order(self):

        highest_layer = []

        for obj in self.children:

            highest_layer.append(obj.coords[1])

        self.layers = range(max(highest_layer),min(highest_layer)-1,-1)

    def draw(self,mouse_pos=[0,0],window_size=[1200,960]):

        dt = []

        for layer in self.layers:

            for obj in self.drawable:

                if obj.coords[1] == layer:

                    t1 = time.time()

                    obj.draw()

                    t2 = time.time()

                    dt.append(str(obj.coords) + ": {} ms".format(t2-t1))

            self.selector.draw()

        for gui in self.gui:

            gui.draw()
            
##        print(dt)
                        
                        
    def offset_func(self,offset=[0,0]):

        if offset != [0,0]:

            self.offset[0] += offset[0]

            self.offset[1] += offset[1]

            for obj in self.children:

                obj.off_translate(offset)

            self.selector.off_translate(offset)

    def add_gui(self,gui=None):

        gui.parent = self

        self.gui.append(gui)

    def add_object(self,obj=None,update_order = True):

        if obj != None and type(obj) != list:

            obj.parent = self

            self.children.append(obj)

##            print(obj.coords)

            obj.tile_id = self.last_tile_id

            self.ids[self.last_tile_id] = obj

            self.last_tile_id += 1

##            c = str(obj.coords[0])+" "+str(obj.coords[1])

            c = obj.coords[0],obj.coords[1],obj.coords[2]

            if c not in self.coord_list.keys():

                self.coord_list[c] = [obj]

            else:

                self.coord_list[c].append(obj)

            if obj.obj_type == "entity":

                self.entities.append(obj)

        elif obj != None and type(obj) == list:

            for o in obj:

                self.children.append(o)

                o.parent = self

                o.tile_id = self.last_tile_id

                self.ids[self.last_tile_id] = o

                self.last_tile_id += 1

                #c = str(o.coords[0])+" "+str(o.coords[1])

                c = o.coords[0],o.coords[1],o.coords[2]

                if c not in self.coord_list.keys():

                    self.coord_list[c] = [o]

                else:

                    self.coord_list[c].append(o)

                if o.obj_type == "entity":

                    self.entities.append(o)

        self.entity_count = len(self.entities)

        if update_order:

            self.update_draw_order()

    def move_obj(self,obj=None,old_pos=[0,0,0]):

        if obj != None:

            c = old_pos[0],old_pos[1],old_pos[2]

            self.coord_list[c].remove(obj)

            n = obj.coords[0],obj.coords[1],obj.coords[2]

            if n not in self.coord_list.keys():

                self.coord_list[n] = [obj]

            else:

                self.coord_list[n].append(obj)

        self.update_draw_order()

    def search(self,coords=[None,None],obj_id=None,name=None):

        outp = []

        if obj_id != None:

            for obj in self.children:

                if obj.obj_id == obj_id:

                    outp.append(obj)

        if coords[0] != None and coords[1] != None:

            for obj in self.children:

                if obj.coords[0] == coords[0] and obj.coords[1] == coords[1]:

                    outp.append(obj)

        elif coords[0]!=None:

            for obj in self.children:

                if obj.coords[0] == coords[0]:

                    outp.append(obj)

        elif coords[1]!=None:

            for obj in self.children:

                if obj.coords[1] == coords[1]:

                    outp.append(obj)

        if name != None:

            for obj in self.children:

                if hasattr(obj,"name"):

                    if obj.name == name:

                        outp.append(obj)

        return outp

    def __str__(self):

        s = "area name:{} {} endarea"

        c_s = " "

        for c in self.children:

            c_s = c_s + str(c) + " "

        s = s.format(self.name,c_s)

        return s

    def generate(self):

        # clear all lists

        self.children = []

        self.coord_list = {}

        self.entities = []

        self.drawable = []

        # generation

        f = open(".//map.txt","w")

        heightmap = {}

        coords = []

        t = {}

        x_size = 15

        y_size = 15

        peak_rng = 10

        peak_height = 50

        smoothing_passes = 2

        for x in range(0,x_size + 1):

            for y in range(0,y_size + 1):

                if random.randrange(1,peak_rng) == 2:

                    heightmap[(x,y)] = random.randrange(1,peak_height)

                else:

                    heightmap[(x,y)] = 0

        ##    smoothing algorithm?

        directions = [(1,0),(-1,0),(0,-1),(0,1)]

        keys = heightmap.keys()

        for x in range(0,smoothing_passes + 1):

            for n in keys:

                sums = 0

                for d in directions:

                    if (n[0] + d[0],n[1] + d[1]) in keys:

                        sums += heightmap[(n[0] + d[0],n[1] + d[1])]

                    else:

                        pass

                heightmap[n] = round(sums/4)

        print("Heightmap finished.")
        
        for c in keys:

            for h in range(0,heightmap[c]):

                coords.append([c[0],c[1],h])

        height = []

        for y in range(0,y_size+1):

            temp = []

            for x in range(0,x_size+1):

                temp.append(0)

            height.append(temp)

        for k in heightmap.keys():

            height[k[1]][k[0]] = heightmap[k]

        for y in range(y_size,-1,-1):

            temp = []

            for x in range(0,x_size+1):

                h = heightmap[(x,y)]

                temp.append(h)

            print(temp)

            for t in temp:

                for n in range(0,(3-len(str(t)))+1):

                    f.write(" ")

                f.write(str(t))

            f.write("\n")

        f.close()

        print("Coords calculated.")

        for c in coords:

            if [c[0],c[1],c[2]+1] not in coords:

                self.add_object(tile_floor(coords=[c[0],c[1],c[2]+1]),update_order = False)

            self.add_object(tile(coords=c),update_order = False)


        print("Objects added.")


##        print(heightmap)

        # update values

        self.update_draw_order()

    def click(self,position=[0,0],button=1):

        gui_click = False

        for gui in self.gui:

            if position[0] >= gui.position[0] and position[1] >= gui.position[1] and position[0] <= gui.position[0] + gui.dimensions[0] and position[1] <= gui.position[1] + gui.dimensions[1]:

                gui_click = True

                gui.click(position,button)

        if not gui_click:

            coord_click = (math.floor((position[0] - self.offset[0])/64),math.floor((position[1] - self.offset[1])/32),self.current_z)

            if coord_click in self.coord_list.keys():

                self.selected_object = []

                for item in self.coord_list[coord_click]:

                    item.click(position,button)

                    self.selected_object.append(item)

                for o in self.selected_object:

                    print(o.name)

            if self.selected_object != []:

                self.selector.visible = True

                self.selector.coords = self.selected_object[0].coords

            else:

                self.selector.visible = False

##        print("click at {} with button {}".format(position,button))

    def drag(self,position=[0,0],delta=[0,0]):

        gui_drag = False

        if self.gui != []:

            for gui in self.gui:

                if position[0] >= gui.position[0] and position[1] >= gui.position[1] and position[0] <= gui.position[0] + gui.dimensions[0] and position[1] <= gui.position[1] + gui.dimensions[1]:

                    gui_drag = True

                    gui.drag(position,delta)

##                    print("gui_drag",position)

##                    print(gui.position[0],gui.position[0] + gui.dimensions[0])

        if not gui_drag:

            self.offset_func(delta)

##            print("no_gui_drag",position)

    def update_tile(self,tile_id = 0,tile=None):

        if tile_id in self.ids.keys():

            self.ids[tile.id] = tile

##    def to_string(self):
##
##        ol = []
##
##        for o in self.children:
##
##            ol.append(o.to_string())
##
##        ol = str(ol).replace('"',"")
##
##        s = "world.area(children={},name='{}')".format(ol,self.name)
##
##        return s

    def to_string(self):

        s = self.__class__.__name__ + "(children=["

        a = self.__dict__
        
        a1 = {}

##        for key in a.keys():
##
##            a_e = a[key]
##
##            if key in ["name","children"]:
##
##                if type(a_e) == list:
##
##                    cl = []
##
##                    for c in a_e:
##
##                        if hasattr(c,"to_string"):
##
##                            cl.append(c.to_string())
##
##                        else:
##
##                            cl.append(str(c))
##
##                    a1[key] = str(cl).replace('"',"")
##
##                elif hasattr(a_e,"to_string"):
##
##                    a1[key] = a_e.to_string()
##
##                else:
##
##                    a1[key] = a_e

##        exec("a1 =" + a1)
##
##        for key in a1.keys():
##
##            print(key,a1[key])

        l = ""

        for c in self.children:

            l += c.to_string()

        return l

class tile(grid_obj):

    def __init__(self,coords=[0,1,0],sprites={"default":".//sprites//block_test.png"},opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",inv_slots=[],name="world_block",additions=[]):

        grid_obj.__init__(self,coords=coords,visible=visible,opacity=opacity,global_layer=global_layer,sprites=sprites,additions = additions,tags=tags,name=name,inv_slots=inv_slots)

        self.obj_type = "tile"

    def draw(self):

        layers = []

        if self.additions != []:

            for a in self.additions:

                layers.append(a.tile_layer)

            min_l = min(layers)

            max_l = max(layers)

            for l in range(min_l,0):

                for a in self.additions:

                    if a.tile_layer == l:

                        a.draw()

                        

        grid_obj.draw(self)

        if self.additions != []:

            for l in range(1,max_l+1):

                for a in self.additions:

                    if a.tile_layer == l:

                        a.draw()

    def tick(self,dt):

        pass

class item_drop(grid_obj):

    def __init__(self,inv_slots=[],coords=[0,0,0],sprites={"default":".//sprites//item_drop.png"},name="test",tags=[["impassable"]]):

        grid_obj.__init__(self,coords=coords,sprites=sprites,inv_slots=inv_slots,name=name,tags=tags)

    def tick(self,dt):

        coord_list = self.search_coord()

        for k in coord_list:

            if hasattr(k,"inv_slots") and k.name != self.name:

                for slots in self.inv_slots:

                    if slots.item != None:

                        print("Item {} given to {}".format(slots.item.name,k.name))

                        self.give_item(give_slot=slots.name,recv_object=k,recv_slot="current_weapon")

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
##        s = "world.{}(name='{}',inv_slots={},coords={},sprites={},tags={})".format(self.__class__.__name__,self.name,slots,str(self.coords),str(self.sprites),str(self.tags))
##
##        return s


        

class tile_floor(tile):

    def __init__(self,coords=[0,1,0],sprites={"default":".//sprites//floor.png"},opacity = 255,tags=[],parent=None,visible=True,global_layer="world",name="world_block",additions=[]):

        tile.__init__(self,coords=coords,visible=visible,opacity=opacity,global_layer=global_layer,sprites=sprites,additions = additions,tags=tags,name=name)
        

class block_tile(tile):

    def __init__(self,coords=[0,0,0],sprites={"default":".//sprites//block.png"},name = "Block"):

        tile.__init__(self,coords=coords,sprites=sprites,opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name=name,additions=[])
    

        
class test_tile1(tile):

    def __init__(self,coords=[0,0,0],sprites={"default":".//sprites//block.png"},name = "test1"):

        tile.__init__(self,coords=coords,sprites=sprites,opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name=name,additions=[])

    def tick(self,dt=100):

        grid_obj.tick(self,delta=dt)

        l = self.search_coord([1,0],"r")

        print(l)

        for l1 in l:

            if l1.name == "test2":

                print("Multiblock detected.")
        

class test_tile2(tile):

    def __init__(self,coords=[0,0,0],sprites={"default":".//sprites//block.png"},name = "test2"):

        tile.__init__(self,coords=coords,sprites=sprites,opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name=name,additions=[])
            

        

        

        

    




        

        
