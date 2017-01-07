import socket,random,time,sys,random

import modules.world as world

import modules.gui as gui

import modules.utilities as util

import modules.items as items

import modules.entities as ent

import modules.sprite as sprite

import modules.draw_obj as dobj

sys.path.append("pyglet-1.2.4.whl")

import pyglet

main_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

main_socket.setblocking(0)

io_out = []

io_in = []

window_size = [1200,960]

current_area = None

input_text = ""

mouse_position = [0,0]

last_click = [0,0]

username = "EyeofEnder"

current_character = None

highest_graphic_layer = 2

gui_objects = [] 

output_focus = "game"

title_text = util.read_text_file("lang/title_en.txt",False)

title_text = title_text.split("\n")

loaded_sprites = []

recent_key = None

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

new_area = world.area()

#for n in range(1,50):

#   new_area.add_object(world.create_tile_line([50+n,0],[50+n,20]))

new_area.add_object(world.create_tile_line([0,0],[0,10]))

new_area.add_object(world.create_tile_line([0,0],[10,0]))

new_area.add_object(world.create_tile_line([0,10],[10,10]))

new_area.add_object(world.create_tile_line([10,0],[10,10]))

new_area.add_object(world.grass_tile([0,0]))

new_area.add_object(world.create_tile_structure([[10,10],[11,10],[9,10],[10,11],[10,9]]))

new_area.add_object(ent.entity(coords=[3,1],inventory_slots=[items.item_slot(name="current_weapon",item=items.weapon(name="Shatter Strike",base_acc=25,base_dmg=120))],health=[1000,1000]))

new_area.add_object(ent.entity(name="Nightfall Harpy Striker",coords=[6,2],inventory_slots=[items.item_slot(name="current_weapon",item=items.weapon())]))

current_area = new_area

window = pyglet.window.Window(width=window_size[0],height=window_size[1],caption="Nightfall - Heroes of Aeternia : " + random.choice(title_text),resizable=True)

fps_display = pyglet.window.FPSDisplay(window)

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

    global input_text, io_out, output_focus,last_button,recent_key

    print(keys)

    last_button = keys

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
                    
def tick(dt):

    global recent_key,output_focus

    current_area.tick(round(dt,4)*1000)

    if output_focus == "game":

        current_area.set_debug_value(recent_key)

    recent_key = None

    

@window.event
def on_draw():

    global mouse_position,window_size,fps_display

    #print(pyglet.clock.get_fps())

    window.clear()

    current_area.draw(last_click,window_size)

    for gui_obj in gui_objects:

        gui_obj.draw()

    fps_display.draw()
    
@window.event
def on_mouse_motion(x, y, dx, dy):

    global mouse_position

    mouse_position = [x,y]
    
@window.event
def on_mouse_press(x, y, button, modifiers):

    global last_click

    last_click = [x,y]

    

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

    current_area.offset([dx,dy])

@window.event
def on_resize(width,height):

    global window_size

    window_size = [width,height]

    print(window_size)


pyglet.clock.schedule_interval(net_io,0.01)

pyglet.clock.schedule_interval(tick,0.1)

pyglet.app.run()



