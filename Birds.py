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

'''
# Test : 
engine = BirdEngine()
engine.reset()
engine.declare(Order('tubenose'), Color('white'), Color('green'))
print(engine.facts)
print("-----------")
engine.run()
print(engine.facts)
'''

list_column = [
    [
        sg.Text("Bird    "),
        sg.InputText(size=(25, 1), enable_events=True, key="-BIRD-"),
        sg.Button("enter"),
    ],
    [
        sg.Text("Family"),
        sg.InputText(size=(35, 1), enable_events=True, key="-FAMILY-"),
    ],
    [
        sg.Text("Color  "),
        sg.InputText(size=(35, 1), enable_events=True, key="-COLOR-"),
    ],
    [
        sg.Text("Order  "),
        sg.InputText(size=(35, 1), enable_events=True, key="-ORDER-"),
    ],
    [
        sg.Text("Facts  "),
        sg.InputText(size=(35, 2), enable_events=True, key="-FACTS-"),
    ],
    [
        sg.Text("Initial facts        "),
        sg.Listbox(
            values=[], enable_events=True, size=(25, 4), key="-LISTF-"
        )
    ],
    [
        sg.Text("Concluded facts"),
        sg.Listbox(
            values=[], enable_events=True, size=(25, 7), key="-LIST-"
        )
    ]
]

layout = [
    [
        sg.Column(list_column),
    ]
]

window = sg.Window("Birds", layout)
lst = numpy.array([])
lstF = numpy.array([])
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "enter":
        lst = numpy.array([])
        lstF = numpy.array([])
        color = values["-COLOR-"]
        order = values["-ORDER-"]
        bird = values["-BIRD-"]
        family = values["-FAMILY-"]
        facts = values["-FACTS-"].split()
        engine = BirdEngine()
        engine.reset()
        #engine.declare(Fact(size='large'))
        for fac in facts : 
            # size :
            if(fac[0:fac.index('=')] == 'size') : 
                engine.declare(Fact(size=fac[fac.index("'")+1:len(fac)-1]))
            # wings : 
            if(fac[0:fac.index('=')] == 'wings') : 
                engine.declare(Fact(wings=fac[fac.index("'")+1:len(fac)-1]))
            # flight : 
            if(fac[0:fac.index('=')] == 'flight') : 
                engine.declare(Fact(flight=fac[fac.index("'")+1:len(fac)-1]))
            # feed : 
            if(fac[0:fac.index('=')] == 'feed') : 
                engine.declare(Fact(feed=fac[fac.index("'")+1:len(fac)-1]))
        if(bird!=''):
            engine.declare(Bird(bird))
        if(family!=''):
            engine.declare(Family(family))
        if(color!=''):
            engine.declare(Color(color))
        if(order!=''):
            engine.declare(Order(order))
        for f in engine.facts:
            i = 0;
            for k, v in engine.facts[f].items(): 
                if(i%2 == 0) : 
                    if(v != 0.0) :
                        lstF = numpy.append(lstF, [v])
                i+=1
                
        window["-LISTF-"].update(lstF)

        engine.run()
        
        for f in engine.facts:
            i = 0;
            for k, v in engine.facts[f].items(): 
                if(i%2 == 0) : 
                    if(v != 0.0) :
                        lst = numpy.append(lst, [v])
                i+=1
                
        window["-LIST-"].update(lst)
