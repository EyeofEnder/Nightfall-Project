import sys, random, time

sys.path.append("pyglet-1.2.4.whl")

import pyglet

items = []

batch = pyglet.graphics.Batch()

t_list = []

class sprite():

    def __init__(self,x=0,y=0,image=".//sprites//block.png"):

        global batch

        self.sprite = pyglet.image.load(image)

##        self.sprite = pyglet.sprite.Sprite(self.sprite,x,y,batch = batch)
##
        self.sprite = pyglet.sprite.Sprite(self.sprite,x,y)

    def draw(self):
##
##        self.sprite.x += random.choice([1,-1])
##
##        self.sprite.y += random.choice([1,-1])
##
        self.sprite.draw()



for n in range(1,30):

    for s in range(1,30):

        items.append(sprite(x=n*64,y=s*32))

window = pyglet.window.Window(width=1200,height=960,caption="test",resizable=True)

fps = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():

    global items,fps,window,batch,t_list

    window.clear()

    t1 = time.time()

    for item in items:

        item.draw()

##    batch.draw()

    t2 = time.time()

    print("draw, dt: {}".format(t2-t1))

    t_list.append(t2-t1)

    fps.draw()

def tick(dt):

    global t_list

    print("Avg delta: {}".format(sum(t_list)/len(t_list)))

    t_list = []

def emp(dt):

    pass

pyglet.clock.schedule_interval(tick,1)

pyglet.clock.schedule_interval(emp,0.01)



pyglet.app.run()
        
