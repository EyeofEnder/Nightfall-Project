import socket,random,time,sys

import modules.world as world

sys.path.append("pyglet-1.2.4.whl")

import pyglet

main_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

main_socket.setblocking(0)

client_id = random.randrange(1,1000)

io_out = []

io_in = []

current_area = None

input_text = ""

mouse_position = [0,0]

username = "EyeofEnder"

def net_io(dt):

    global main_socket, io_out, io_in

    if io_out != []:

        msg = io_out.pop()

    else:

        msg = ""

    msg = msg.encode("ascii")

    main_socket.sendto(msg,("localhost",50000))

    try:

        in_msg,addr = main_socket.recvfrom(8192)

        in_msg = in_msg.decode("ascii")

        if in_msg != "None":

            print(in_msg)

    except:

        pass

pyglet.clock.schedule_interval(net_io,0.01)

window = pyglet.window.Window(width=600,height=480,caption="Nightfall - Heroes of Aeternia Pre-alpha",resizable=True)
        

class sprite():

    def __init__(self,parent=None,sprite_path = ".//sprites//entities//t8_wildcat.png",base_position = [0,0],layer = 0, offset = [0,0],visible=True,opacity=255):

        self.parent = parent

        if parent == None:

            self.base_position = base_position # [x y] in pixels

            self.sprite_path = sprite_path

            self.visible = visible

            self.opacity = opacity

        if parent != None:

            try:

                self.sprite_path = self.parent.sprite_path

                self.base_position = self.parent.base_pixel_position

                self.opacity = self.parent.opacity

                self.visible = visible

            except:

                pass

        self.layer = layer  # lower layer = further back

        self.offset = offset # [x y] in pixels

        self.image = pyglet.image.load(self.sprite_path)

        self.sprite = pyglet.sprite.Sprite(self.image,self.base_position[0] + self.offset[0],self.base_position[1] + self.offset[1])

        self.sprite.opacity = self.opacity

    def draw(self):


        if self.parent != None:

            #self.update_parent()

            pass

        if self.visible == True:
            
            self.update_sprite()

            self.sprite.draw()

    def update_sprite(self,new_image = False):

        if new_image == True:

            self.image = pyglet.image.load(self.sprite_path)

##            self.sprite = pyglet.sprite.Sprite(self.image,self.base_position[0] + self.offset[0],self.base_position[1] + base_self.offset[1])

            self.sprite.image = self.image

        self.sprite.position = (self.base_position[0] + self.offset[0],self.base_position[1] + self.offset[1])

        self.sprite.opacity = self.opacity

        

    def update_parent(self, new_parent = None, new_image = False):

        if new_parent != None:

            self.parent = new_parent

        if self.parent == None:

            pass

        if self.parent != None:

            try:

                self.sprite_path = self.parent.sprite_path

                self.base_position = self.parent.base_pixel_position 

                self.opacity = self.parent.opacity

                self.visible = visible
                
            except:


                pass
            
        self.update_sprite(new_image)

game_objects = [world.area(contents=[world.tile(position=[4,0,1],sprite=sprite()),world.tile(position=[4,1,0],sprite=sprite())])]


@window.event
def on_close():

    window.close()

@window.event
def on_text(text):

    global input_text

    input_text += text

@window.event
def on_key_press(keys,modifiers):

    global input_text, io_out

    print("Input detected.")

    if keys == 65293:  # on enter press

        print(input_text)

        io_out.append("chat_local " + username + " " + input_text.replace("\r",""))

        print(io_out)

        input_text = ""

    if keys == 65288:   # on backspace press

        input_text = input_text[:-1]

@window.event
def on_draw():

    #print(pyglet.clock.get_fps())

    window.clear()

    for game_obj in game_objects:

        game_obj.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):

    global mouse_position

    for game_obj in game_objects:

        #game_obj.update_mouse(x,y)

        pass
    
    mouse_position = [x,y]

    #print(mouse_position)
    
@window.event
def on_mouse_press(x, y, button, modifiers):

    print("Click. x = {0}, y = {1}".format(x,y))

    for obj in game_objects:

        #obj.update_sprite()

        pass

        
pyglet.app.run()



