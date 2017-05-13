import modules.world as world

import modules.items as items

import sys,math,random

from . import sprite as sprite

from . import draw_obj as d_obj

from . import utilities as util

from . import entities as entities

sys.path.append("pyglet-1.2.4.whl")

import pyglet


class quest():

    def __init__(self,name="First Flight",points={"start":True,"finish":False}):

        self.name = name

        self.points = points

class achievement():

    def __init__(self,name="Hello there!",desc="Start up the game, already got an achievement. EZ.",howto="Simple. Start up the game.",hidden=0,achieved=True): # hidden level: 0 = name,desc and how to visible, 1 = name and desc, 2 = name only, 3 = nothing visible at first

        self.name = name

        self.desc = desc

        self.howto = howto

        self.hidden = hidden

        self.achieved = achieved

    def get(self):

        if not self.achieved:

            self.achieved = True

all_achievements = [achievement(),
                    achievement(name="First Blood",desc="Obligatory first kill achievement.",howto="Kill an enemy. Or anyone. Just not yourself.",hidden=0,achieved=False),
                    
                    
                    ]


                    
