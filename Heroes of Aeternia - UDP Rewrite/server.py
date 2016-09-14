import socket,sys,threading,time

sys.path.append("pyglet-1.2.4.whl")

import pyglet

main_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

main_socket.bind(("",50000))

main_socket.setblocking(0)

requests = []

world_time = [0,0,0,0] # year, day, hour, minute

def net_io(dt):

    global requests

    try:

        msg, addr = main_socket.recvfrom(8192)

        msg = msg.decode("ascii")

        if msg != "":

            requests.append([msg,addr,0]) # message string, address, status

    except:

        pass

    for req in requests:

        if req[2] == 3:

            out_msg = req[0].encode("ascii")

            requests.remove(req)

        else:

            out_msg = "None"

            out_msg = out_msg.encode("ascii")


        main_socket.sendto(out_msg,req[1])


def process_messages(dt):

    global requests, world_time

    for req in requests:

        if "time_request" in req[0]:

            req[0] = str(world_time)

        else:

            req[0] += " echo"

        req[2] = 3

def update_game_clock(dt):

    global world_time

    print(world_time)

    if world_time[3] < 59:

        world_time[3] += 1

    else:

        world_time[3] = 0

        if world_time[2] < 23:

            world_time[2] += 1

        else:

            world_time[2] = 0

            if world_time[1] < 415:

                world_time[1] += 1

            else:

                world_time[1] = 0

                world_time[0] += 1


def game_tick(dt):

    global areas

    pass


pyglet.clock.schedule_interval(net_io,0.01)

pyglet.clock.schedule_interval(process_messages,0.01)

pyglet.clock.schedule_interval(update_game_clock,0.1)

pyglet.clock.schedule_interval(game_tick,0.1)

pyglet.app.run()

        



    
    
