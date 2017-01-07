import random,math

from . import utilities as util

from . import sprite as sprite

from . import draw_obj as draw_obj

from . import gui as gui

class grid_obj(draw_obj.draw_obj):

    def __init__(self,coords=[0,1],sprites={"default":".//sprites//block.png"},opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name="world_block",additions=[]):

        self.tile_id = None

        self.coords = coords

        self.offset = [0,0]

        self.position = [(self.coords[0] * 64) + self.offset[0],(self.coords[1] * 32) + self.offset[1]]

        self.parent = parent

        self.tags = tags
        
        self.pending_actions = []

        self.name = name
        
        self.obj_type = "grid_obj" 

        draw_obj.draw_obj.__init__(self,position=self.position,visible=visible,opacity=opacity,global_layer=global_layer,sprites=sprites)
        
        self.change_sprite("default")

        self.additions = []

        self.in_battle = False

        for add in additions:

            add.parent = self

            self.additions.append(add)

    def search_coord(self,position=[0,0],mode="r"):   # r = relative, a = absolute

        if mode == "r":

            return self.parent.search(coords=[self.coords[0]+position[0],self.coords[1]+position[1]])

        elif mode == "a":

            return self.parent.search(coords=coords)

        

    def update_position(self):

        self.position = [(self.coords[0] * 64) + self.offset[0],(self.coords[1] * 32) + self.offset[1]]

    def tick(self,delta):

        draw_obj.draw_obj.tick(self,delta)

        for action in self.pending_actions:

            pass
        
        self.update_position()

       # print(self)
        
    def queue_action(self,action="say test"):

        self.pending_actions.append(action)

    def off_translate(self,offset=[0,0]):

        self.offset[0] += offset[0]

        self.offset[1] += offset[1]

        #  -- Uncomment for glitch art --

        #self.offset[0] += random.choice([1,-1])*offset[0]

        #self.offset[1] += random.choice([1,-1])*offset[1]

        self.update_position()
        
    def search_radius(self,r=2):

        pass

    def find_distance(self,coords=[1,1]):

        distance = math.sqrt(pow(self.coords[0]-coords[0],2)+pow(self.coords[1]-coords[1],2))

        return distance

    def check_passable(self,coords=[1,1],mode="r"):

        passable = True

        check = self.search_coord([coords[0],coords[1]],mode = mode)

        for c in check:

            for tag in c.tags:

                if "impassable" in tag:

                    passable = False

                    break


        return passable

    def add_addition(self,addition=None):

        addition.set_parent(self)

        self.children.append(addition)

    def __str__(self):

        sp = []

        for k in self.sprite_paths:

            sp.append([k,self.sprite_paths[k]])

        c = str(self.coords).replace(" ","")

        t = str(self.tags).replace(" ","")

        sp = str(sp).replace(" ","")

        s = "{} c:{} t:{} sp:{} id:{} end{}".format(self.obj_type,c,t,sp,str(self.tile_id),self.obj_type)

        return s

    def enter_combat(self,enemy=None):

        if not self.in_battle:

            print("entered combat")

            self.parent.create_battle([self,enemy])

            self.in_battle = True

            


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

        grid_obj.__init__(self,sprites={"default":".//sprites//cubeselector.png"})

    def snap_to_mouse(self,mouse_position=[0,0]):

        self.coords = [math.floor((mouse_position[0]-self.offset[0])/64),math.floor((mouse_position[1]-self.offset[1])/32)]

    def draw(self):

        self.update_position()

        draw_obj.draw_obj.draw(self)

class area():

    def __init__(self,children=[],name="Zverograd_Combat_Academy"):

        self.children = children

        self.coord_list = []

        self.name = name

        self.highest_layer = 1

        self.obj_type = "area"

        self.selector = selector()

        self.battles = []

        self.debug_value = None

        self.entities = []

        self.last_tile_id = 1

        self.ids = {}

    def tick(self,dt=100):

        self.coord_list = []

        for obj in self.children:

            if obj.obj_type not in ["entity","combat_entity"]:

                obj.tick(dt)

            if obj.obj_type in ["entity","combat_entity"]:

                if not obj.in_battle:

                    obj.tick(dt)

        for obj in self.children:

            if obj.obj_type in ["entity","combat_entity"]:

                if not obj in self.entities:

                    self.entities.append(obj)

            if obj.coords not in self.coord_list:

                self.coord_list.append([obj.coords[0],obj.coords[1]])
                

        for coord in self.coord_list:

            coord_e = [coord[0],coord[1]]

            for obj in self.children:

                if obj.coords == coord_e and obj not in coord:

                    coord.append(obj)

        

        self.update_draw_order()

    def update_draw_order(self):

        highest_layer = []

        for obj in self.children:

            highest_layer.append(obj.coords[1])

        self.highest_layer = max(highest_layer)

    def draw(self,mouse_pos=[0,0],window_size=[1200,960]):

        for layer in range(self.highest_layer,-1,-1):

            for obj in self.children:

                if obj.coords[1] == layer:

                    if obj.position[0]<= window_size[0] and obj.position[1] <= window_size[1]:

                        obj.draw()

        self.selector.snap_to_mouse(mouse_pos)

        self.selector.draw()

    def offset(self,offset=[0,0]):

        if offset != [0,0]:

            self.selector.off_translate(offset)

            for obj in self.children:

                obj.off_translate(offset)

    def create_battle(self,entities=[]):

        self.battles.append(entities)

        for ent in entities:

            ent.tick_trigger = "battle"


    def set_debug_value(self,value=None):

        self.debug_value = value

    def add_object(self,obj=None):

        if obj != None and type(obj) != list:

            obj.parent = self

            self.children.append(obj)

            obj.tile_id = self.last_tile_id

            self.ids[self.last_tile_id] = obj

            self.last_tile_id += 1

        elif obj != None and type(obj) == list:

            for o in obj:

                self.children.append(o)

                o.parent = self

                o.tile_id = self.last_tile_id

                self.ids[self.last_tile_id] = o

                self.last_tile_id += 1

        self.update_draw_order()

        print(self.ids)

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

    def add_action(self,controller=None,command=None):

        for obj in self.children:

            if obj.control[0] == controller and obj.control[1] == True:

                obj.pending_actions.append(command)

    def __str__(self):

        s = "area n:{} {} endarea"

        c_s = ""

        for c in self.children:

            c_s = c_s + str(c) + " "

        s = s.format(self.name,c_s)

        return s

class tile(grid_obj):

    def __init__(self,coords=[0,1],sprites={"default":".//sprites//block.png"},opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name="world_block",additions=[]):

        grid_obj.__init__(self,coords=coords,visible=visible,opacity=opacity,global_layer=global_layer,sprites=sprites,additions = additions,tags=tags)

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

                        

        draw_obj.draw_obj.draw(self)

        if self.additions != []:

            for l in range(1,max_l+1):

                for a in self.additions:

                    if a.tile_layer == l:

                        a.draw()
        

class grass_tile(tile):

    def __init__(self,coords=[0,0]):

        tile.__init__(self,coords=coords,sprites={"default":".//sprites//block.png"},opacity = 255,tags=[["impassable"]],parent=None,visible=True,global_layer="world",name="world_block",additions=[])
    

        

            

        

        

        

    




        

        
