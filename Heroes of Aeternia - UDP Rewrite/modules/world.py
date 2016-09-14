
class area():

    def __init__(self,contents=[],name="Zverograd Combat Academy"):

        self.contents = contents

        self.name = name

class tile_row():

    def __init__(self,contents = [],parent = None,y = 0):

        self.contents = contents

class tile():

    def __init__(self,position=[0,1,0],base_pixel_position=[0,0],sprite_path=".//sprites//test_sprite.png",opacity = 255,obj_id=1,tags=[],contents=[],parent_id=2,sprite=None):

        self.position = position # grid x, grid y, layer (z), pixel x base, pixel y base

        #self.pixel_base_position = [self.position[0] *  TBD

        self.sprite_path = sprite_path

        self.obj_id = obj_id

        self.tags = tags

        self.parent_id = parent_id

        self.sprite = sprite

        self.hitbox = hitbox

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

    def update_mouse(self,x=0,y=0,click=False):

        if x >= self.sprite.position[0] and x <= self.sprite.position[0] + self.hitbox[0]:

            print("x match" + str(self.sprite.position))

            if y >= self.sprite.position[1] and y <= self.sprite.position[1] + self.hitbox[1]:

                print("x + y match" + str(self.sprite.position))

        if y >= self.sprite.position[1] and y <= self.sprite.position[1] + self.hitbox[1]:

            print("y match" + str(self.sprite.position))

        


        

        

    




        

        
