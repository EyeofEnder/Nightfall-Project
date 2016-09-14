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

    def __init__(self,parent=None,sprite_path = ".//sprites//entities//t8_wildcat.png",position = [0,0,0,0,0],visible=True,opacity=255,layer=0):

        self.parent = parent

        if parent == None:

            self.position = position # [x y layer temp_x_offset temp_y_offset], where lower layer = further back

            self.sprite_path = sprite_path

            self.visible = visible

            self.opacity = opacity

        if parent != None:

            try:

                self.sprite_path = self.parent.sprite_path

                self.position = [self.parent.position[3],self.parent.position[4],0]

                self.opacity = self.parent.opacity

                self.visible = visible

            except:

                pass

        self.image = pyglet.image.load(self.sprite_path)

        self.sprite = pyglet.sprite.Sprite(self.image,self.position[0],self.position[1])

        self.sprite.opacity = self.opacity

    def draw(self):


        if self.parent != None:

            self.update_parent()

        if self.visible == True:
            
            self.update_sprite()

            self.sprite.draw()

    def update_sprite(self,new_image = False):

        if new_image == True:

            self.image = pyglet.image.load(self.sprite_path)

            self.sprite = pyglet.sprite.Sprite(self.image,self.position[0] + self.position[3],self.position[1] + self.position[4])

        else:

            self.sprite.position = (self.position[0] + self.position[3],self.position[1] + self.position[4])

        self.sprite.opacity = self.opacity

        

    def update_parent(self, new_parent = None, new_image = False):

        if new_parent != None:

            self.parent = new_parent

        if self.parent == None:

            pass

        if self.parent != None:

            try:

                self.sprite_path = self.parent.sprite_path

                self.position[0] = self.parent.position[0] * 64

                self.position[1] = self.parent.position[1] * 32

                self.opacity = self.parent.opacity

                self.visible = visible
                
            except:


                pass
            
        self.update_sprite(new_image)

game_objects = [world.tile(position=[4,0,0],sprite=sprite())]

game_objects.append(world.tile(position=[5,0,0],sprite=sprite()))

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

        game_obj.update_mouse(x,y)
    
    mouse_position = [x,y]

    #print(mouse_position)
    
@window.event
def on_mouse_press(x, y, button, modifiers):

    print("Click. x = {0}, y = {1}".format(x,y))

    for obj in game_objects:

        obj.update_sprite()

        
pyglet.app.run()



