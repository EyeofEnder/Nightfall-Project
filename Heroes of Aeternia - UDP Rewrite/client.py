import socket,random,time,sys,random

import modules.world as world

import modules.gui as gui

import modules.utilities as util

import modules.items as items

import modules.entities as entities

import modules.sprite as sprite

import modules.draw_obj as draw_obj

import pickle

sys.path.append("pyglet-1.2.4.whl")

import pyglet

main_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

main_socket.setblocking(0)

io_out = []

io_in = []

window_size = [1200,960]

current_area = None

input_text = ""

output_focus = "game"

mouse_position = [0,0]

last_click = [0,0]

in_game = True

title_text = util.read_text_file("lang/title_en.ne",False)

title_text = title_text.split("\n")

key_map = {119:"w",
           97:"a",
           115:"s",
           100:"d",
           113:"q",
           65293:"enter",
           32:"space",
           65288:"backspace",
           65505:"l_shift",
           114:"r",
           102:"f"}

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

print("starting tostring")

test = str(current_area)

print("tostring complete")

##test_item = ent.entity(inv_slots=[items.inv_slot(name="kek",item=items.item())])
##
##s = "s = ent."+test_item.to_string()
##
new_area = world.area()
##
##print(s)
##
##exec(s)

new_area.generate()

new_area.add_object(world.item_drop(inv_slots=[items.inv_slot(item=items.weapon(base_dmg=10000000),name="slot0")],coords=[1,1,1]))

##new_area.add_object(entities.entity(name="Nightfall Harpy Striker 1",coords=[4,5,0],inv_slots={"current_weapon":items.item(name="Wet Pool Noodle")},health=[500,500]))
##
##new_area.add_object(entities.entity(name="Nightfall Harpy Striker 2",coords=[1,2,0],inv_slots={"current_weapon":items.weapon(name="""Royal Armories "Draco" Pattern Longsword""",base_acc=50,base_dmg=130,fire_rate=5)},health=[500,500]))
##
##new_area.add_object(entities.entity(name="Nightfall Harpy Striker 3",coords=[4,1,0],inv_slots={"current_weapon":items.weapon(name="N-4 CQC Knife",base_acc=60,base_dmg=25,fire_rate = 20)},health=[500,500]))

new_area.add_object(entities.dummy(coords=[3,3,1],health=[10000000,10000000]))

new_area.add_object(entities.entity(coords=[3,2,1],health=[10000000,10000000]))

current_character = entities.player_test(coords=[3,1,0],inv_slots=[items.inv_slot(name="current_weapon",item=items.weapon(name="Armorspike Mk.2",base_acc=55,base_dmg=35,fire_rate=17))],health=[1000,1000])

new_area.add_object(current_character)

print("---------------------------- AREA TEXT START -----------------------------------")

s = new_area.to_string()

print(s)

test_area = world.area()

##print(test_area)

print("---------------------------- AREA TEXT END -----------------------------------")

current_area = new_area

current_area.player = current_character

##
##print(s.name,s.item.name)

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

    global input_text, io_out, output_focus,last_button,recent_key,key_map

    print(keys)

    last_button = keys

    recent_key =""

    try:

        key_str = key_map[keys]

    except:

        print("Key mapping error, key number:" + str(keys))

        key_str = "Error"

    print("Map:" + key_str)

    recent_key = key_str

    if in_game:

        if key_str == "w":  # w press

            current_character.move_attack([0,1,0])

        if key_str == "a": # a

            current_character.move_attack([-1,0,0])

        if key_str == "s": # s

            current_character.move_attack([0,-1,0])

        if key_str == "d": # d

            current_character.move_attack([1,0,0])

        if key_str == "q": # q

            current_character.attack_selected()

    if keys == 65293:  # on enter press

        if output_focus == "game":

            output_focus = "chat"

        elif output_focus == "chat":

            print(input_text)

            io_out.append("chat_local " + input_text.replace("\r",""))

            print(io_out)

            input_text = ""

            output_focus = "game"

    if keys == 32: # spacebar

        current_area.current_z += 1

        current_area.offset_func([0,64])

    if keys == 65288:   # on backspace press

        input_text = input_text[:-1]

    if keys == 65505: # left shift

        current_area.current_z -= 1

        current_area.offset_func([0,-64])

    if keys == 114: # r

        current_character.move_attack([0,0,1])

        current_area.current_z += 1

    if keys == 102: # f

        current_character.move_attack([0,0,-1])

        current_area.current_z -= 1
 
    io_out.append(recent_key)
                    
def tick(dt):

    global recent_key,output_focus

    if current_area != None:

        current_area.tick(round(dt,4)*1000)

    if output_focus == "game":

##        current_area.set_debug_value(recent_key)

        pass

    recent_key = None

    

@window.event
def on_draw():

    global mouse_position,window_size,fps_display

    #print(pyglet.clock.get_fps())

    t1 = time.time()

    window.clear()

    if current_area != None:

        current_area.draw(last_click,window_size)

    t1a = time.time()

    fps_display.draw()

    t2 = time.time()

##    print("total dt: {}".format(t2-t1))

##    print("draw time: {}".format(t1a-t1))
    
@window.event
def on_mouse_motion(x, y, dx, dy):

    global mouse_position

    mouse_position = [x,y]
    
@window.event
def on_mouse_press(x, y, button, modifiers): # 1: left button, 4: right button

    global last_click

    print(button)

    last_click = [x,y]

    current_area.click([x,y],button)

    

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

    current_area.drag(position=[x,y],delta=[dx,dy])


@window.event
def on_resize(width,height):

    global window_size

    window_size = [width,height]

    print(window_size)

pyglet.clock.schedule_interval(net_io,0.01)

pyglet.clock.schedule_interval(tick,0.1)

pyglet.app.run()



