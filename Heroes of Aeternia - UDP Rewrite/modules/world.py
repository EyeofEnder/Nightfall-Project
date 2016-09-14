
class area():

    def __init__(self,contents=[],name="Zverograd Combat Academy"):

        self.contents = contents

        self.name = name

        self.highest_layer = 1

    def update_draw_order(self):

        highest_layer = []

        for obj in self.contents:

            highest_layer.append(obj.position[2])

        self.highest_layer = max(highest_layer)

    def draw(self):

        self.update_draw_order()

        for layer in range(0,self.highest_layer+1):

            for obj in self.contents:

                if obj.position[2] == layer:

                    try:

                        obj.draw()

                    except:

                        print("drawException: Tried to draw non-drawable object")

    def add_object(self,obj=None):

        if obj != None:

            self.contents.append(obj)

        

class hitbox():

    def __init__(self,position = [0,0],size = [64,32],parent = None):

        self.position = position

        self.size = size

        self.parent = parent

    def check(self,x=None,y=None): # check(self) before you wreck(self)

        if x != None and y != None:

            if x >= self.position[0] and x <= self.position[0] + self.size[0]:

                print("x match" + str(self.position))

                if y >= self.position[1] and y <= self.position[1] + self.size[1]:

                    print("x + y match" + str(self.sprite.position))

            if y >= self.position[1] and y <= self.position[1] + self.size[1]:

                print("y match" + str(self.self.position))

    def update(self,new_position = [0,0],new_size = None):

        if self.parent != None:

            self.position = parent.base_pixel_position

        else:

            new_position = [0,0]

        if new_size != None:

            self.size = new_size


            

class tile():

    def __init__(self,position=[0,1,0],base_pixel_position=[0,0],sprite_path=".//sprites//test_sprite.png",opacity = 255,obj_id=1,tags=[],contents=[],parent_id=2,sprite=None):

        self.position = position # grid x, grid y, layer (z), pixel x base, pixel y base

        self.base_pixel_position = [self.position[0] * 64,self.position[1] * 32]

        self.sprite_path = sprite_path

        self.obj_id = obj_id

        self.tags = tags

        self.parent_id = parent_id

        self.sprite = sprite

        self.opacity = opacity

        self.mouse_interaction = [False,False] # hovered over, clicked on

        if self.sprite != None:

            try:

                self.sprite.update_parent(self,new_image=True)

            except:

                pass

    def tick(self):

        pass

    def to_attr_string(self):

        attr_string = "tile position:{0} sprite_file:{1} tags:{2} object_id:{3} parent_id:{4} hitbox:{5} /tile".format(str(self.position),self.sprite_file,str(self.tags),str(self.obj_id),str(self.parent_id),str(self.hitbox))

        return attr_string

    def draw(self):

        if self.sprite != None:

            self.sprite.draw()

    def update_sprite(self):

        if self.sprite != None:

            try:

                self.sprite.update_parent(self)

            except:

                pass

##    def update_mouse(self,x=0,y=0,click=False):
##
##        
        


        

        

    




        

        
