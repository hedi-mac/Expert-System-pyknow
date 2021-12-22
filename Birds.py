from pyknow import *
import PySimpleGUI as sg
import os.path
import numpy 
import jsons
import string

class Family(Fact):
    pass
class Bird(Fact):
    pass
class Order(Fact):
    pass
class Color(Fact):
    pass

class BirdEngine(KnowledgeEngine):

    @Rule(OR(Order('tubenose'), Fact(size='large'), Fact(wings='long_narrow')))
    def albatross(self):
        self.declare(Family('albatross'))
    
    @Rule(OR(Order('waterfowl'), Color('white'), Fact(neck='long'), Fact(flight='ponderous')))
    def albatross(self):
        self.declare(Family('swan'))
    
    @Rule(OR(Order('waterfowl'), Fact(size='plump'), Fact(flight='powerful')))
    def duck(self):
        self.declare(Family('goose'))

    @Rule(OR(Order('waterfowl'), Fact(feed='on_water_surface'), Fact(flight='agile')))
    def duck(self):
        self.declare(Family('duck'))

    @Rule(AND(Family('albatross'), Color('white')))
    def laysan_albatross(self):
        self.declare(Bird('laysan_albatross'))

    @Rule(AND(Family('albatross'), Color('dark')))
    def black_footed_albatross(self):
        self.declare(Bird('black_footed_albatross'))

    @Rule(AND(Family('duck'), Color('green')))
    def mallard(self):
        self.declare(Bird('mallard'))

# Test : 
engine = BirdEngine()
engine.reset()
engine.declare(Order('tubenose'), Color('white'), Color('green'))
print(engine.facts)
print("-----------")
engine.run()
print(engine.facts)

