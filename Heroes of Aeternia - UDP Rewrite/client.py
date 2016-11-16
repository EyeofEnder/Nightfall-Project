import socket,random,time,sys

import modules.world as world

import modules.interface as interface

import modules.utilities as util

import modules.items as items

import modules.entities as ent

import modules.sprite as sprite

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

current_character = None

highest_graphic_layer = 2

gui_objects = [] 

output_focus = "game"

my_turn = [True,100]

item = items.item()

slot1 = items.item_slot(item = item)

slot2 = items.item_slot()

print(slot1.item)
print(slot2.item)

slot1.move_item(slot2)

print(slot1.item)
print(slot2.item)

title_text = util.read_text_file("lang/title_en.txt",False)

title_text = title_text.split("\n")

def net_io(dt):

    global main_socket, io_out, io_in

    if io_out != []:

        msg = io_out.pop()

    else:

        msg = ""

    msg = msg.encode("utf-8")

    main_socket.sendto(msg,("localhost",50000))

    try:

        in_msg,addr = main_socket.recvfrom(8192)

        in_msg = in_msg.decode("utf-8")

        if in_msg != "None":

            io_in.append(in_msg)

            print(io_in)

    except:

        pass
    
new_area = world.area(graphic_layer=5)

new_area.add_object(world.tile(position=[0,0,1]))

new_area.add_object(world.tile(position=[0,0,0]))

new_area.add_object(ent.combat_entity(position=[10,0,10]))

current_area = new_area

##gui = interface.gui()
##
##gui.add_component(interface.sprite_component(sprite=sprite()))
##
##game_objects.append(gui)


window = pyglet.window.Window(width=1200,height=960,caption="Nightfall - Heroes of Aeternia : " + random.choice(title_text),resizable=True)

@window.event
def on_close():

    window.close()

@window.event
def on_text(text):
    global input_text

    if output_focus == "chat":

        input_text += text

@window.event
def on_key_press(keys,modifiers):

    global input_text, io_out, output_focus

    print(keys)

    recent_key =""

    if output_focus == "game":

        if keys == 119:  # w press

            print("w")

            recent_key ="w"

        if keys == 97: # a

            print("a")

            recent_key ="a"

        if keys == 115: # s

            print("s")

            recent_key ="s"

        if keys == 100: # d

            print("d")

            recent_key ="d"

    if keys == 65293:  # on enter press

        if output_focus == "game":

            output_focus = "chat"

        elif output_focus == "chat":

            print(input_text)

            io_out.append("chat_local " + username + " " + input_text.replace("\r",""))

            print(io_out)

            input_text = ""

            output_focus = "game"

    if keys == 65288:   # on backspace press

        input_text = input_text[:-1]

    io_out.append(username + " " + recent_key)

                    


@window.event
def on_draw():
    
    #print(pyglet.clock.get_fps())

    window.clear()

    for gui_obj in gui_objects:

        game_obj.draw()

    current_area.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):

    global mouse_position
    
    mouse_position = [x,y]

    #print(mouse_position)
    
@window.event
def on_mouse_press(x, y, button, modifiers):

    print("Click. x = {0}, y = {1}".format(x,y))


pyglet.clock.schedule_interval(net_io,0.01)

pyglet.app.run()



