import sys

sys.path.append("pyglet-1.2.4.whl")

import pyglet

class sprite():

    def __init__(self,sprite_path="./sprites/test_sheet.png",dimensions=[1,1],sprite_number=63,parent=None,offset=[0,0],position=[0,0],visible=True,opacity=255):

        if parent != None:

            self.parent = parent

            self.position = parent.position

            self.sprite_path = self.parent.sprite_path

        else:

            self.parent = None

            self.position = position

            self.sprite_path = sprite_path

        self.visible = visible

        self.offset = offset

        self.opacity = opacity

        self.dimensions = dimensions

        if self.dimensions == [1,1]:

            self.current_image = pyglet.image.load(self.sprite_path)

            self.is_grid = False

        else:

            self.sprite_number = sprite_number

            self.grid_image = pyglet.image.load(self.sprite_path)

            self.grid_image = pyglet.image.ImageGrid(self.grid_image,self.dimensions[0],self.dimensions[1])

            self.current_image = self.grid_image[self.sprite_number]

            self.is_grid = True

        self.sprite = pyglet.sprite.Sprite(self.current_image,self.position[0] + self.offset[0],self.position[1] + self.offset[1])

    def change_sprite(self,sprite_path = None,dimensions = None,sprite_number = None):

        if dimensions != None:

            self.dimensions = dimensions

        if sprite_number != None:

            self.sprite_number = sprite_number

        if sprite_path != None:

            self.sprite_path = sprite_path

        if self.dimensions == [1,1]:

            self.current_image = pyglet.image.load(self.sprite_path)

            self.is_grid = False

        else:

            self.grid_image=pyglet.image.load(self.sprite_path)

            self.grid_image = pyglet.image.ImageGrid(self.grid_image,self.dimensions[0],self.dimensions[1])

            self.current_image = self.grid_image[self.sprite_number]

            self.is_grid = True

    def draw(self):

        if self.visible == True:

            self.update_sprite()

            self.sprite.draw()

    def switch_sprite(self,sprite_number=None):

        if sprite_number != None and self.is_grid == True:

            self.sprite_number = sprite_number

            self.current_image =  self.grid_image[self.sprite_number]

            self.update_sprite()

    def update_sprite(self):

        self.sprite.image = self.current_image

        if self.parent != None:

            self.position = self.parent.position

        self.sprite.position = (self.position[0] + self.offset[0],self.position[1] + self.offset[1])

        self.sprite.opacity = self.opacity

    def update_parent(self,new_parent = None):

        if new_parent != None:

            self.parent = new_parent

        if self.parent == None:

            pass

        if self.parent != None:

            try:

                self.sprite_path = self.parent.sprite_path

                self.position = [self.parent.position[0]*64,self.parent.position[1]*32]

                self.opacity = self.parent.opacity

                self.visible = visible
                
            except:


                pass

        self.change_sprite(sprite_path = self.sprite_path)
            
        self.update_sprite()
