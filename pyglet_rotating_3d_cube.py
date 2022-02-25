import pyglet
from pyglet import shapes
from pyglet.window import key

from numpy import array
from math import sin, cos

bias = array([320, 240, 0])

def adj_n(i, j):
    count = 0
    if len(i) != len(j):
        return 0
    for g in range(len(i)):
        if i[g] != j[g]:
            count += 1
        else:
            pass
    if count != 1:
        return False
    else:
        return True

class HelloWorldWindow(pyglet.window.Window):
    def __init__(self, depth):
        super(HelloWorldWindow, self).__init__()
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.updated = 1
        
        self.label = pyglet.text.Label('(0, 0)')

        self.p0 = array([0, 0])
        self.rit = 0
        self.rjt = 0
        self.rkt = 0

        self.cube_size = 10

        self.A = array([1, 1, 1])
        self.B = array([1, 1, -1])
        self.C = array([1, -1, -1])
        self.D = array([1, -1, 1])
        self.E = array([-1, 1, 1])
        self.F = array([-1, 1, -1])
        self.G = array([-1, -1, -1])
        self.H = array([-1, -1, 1])

        self.sources = [self.A, self.B, self.C, self.D,
                        self.E, self.F, self.G, self.H]

        self.verts = [self.A, self.B, self.C, self.D,
                      self.E, self.F, self.G, self.H]

        self.lines = []
        for i in range(24):
            self.lines.append(shapes.Line(320, 240, 320, 240, width=4, color=(255, 255, 255), batch=self.batch))

    def on_draw(self):
        self.clear()
        self.label.draw()
        self.batch.draw()

    def update(self, delta_time):
        self.time += delta_time
        if not self.updated:
            self.r0 = array([array([1, 0, 0]),
                             array([0, cos(self.rit), sin(self.rit)]),
                             array([0, -sin(self.rit), cos(self.rit)])]) * self.cube_size
            self.r1 = array([array([cos(self.rjt), 0, -sin(self.rjt)]),
                             array([0, 1, 0]),
                             array([sin(self.rjt), 0, cos(self.rjt)])]) * self.cube_size
            #self.r2 = array([array([cos(self.rkt), sin(self.rkt), 0]),
            #                 array([-sin(self.rkt), cos(self.rkt), 0]),
            #                 array([0, 0, 1])]) * self.cube_size

            for v in range(len(self.sources)):
                self.verts[v] = self.r0.dot(self.r1.dot(self.sources[v])) + bias
        
            self.label = pyglet.text.Label(f'({str(self.p0[0])}, {str(self.p0[1])})')

            count = 0
            for i in range(len(self.verts)):
                for j in range(len(self.verts)):
                    if adj_n(self.sources[i], self.sources[j]):
                        self.lines[count].position = (self.verts[i][0], self.verts[i][1], self.verts[j][0], self.verts[j][1])
                        count += 1
            self.updated = 1

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.cube_size += .2
            self.updated = 0
        elif symbol == key.DOWN:
            self.cube_size -= .2
            self.updated = 0
        elif symbol == key.W:
            self.rit += .1
            self.updated = 0
        elif symbol == key.S:
            self.rit -= .1
            self.updated = 0
        elif symbol == key.D:
            self.rjt += .1
            self.updated = 0
        elif symbol == key.A:
            self.rjt -= .1
            self.updated = 0
        else:
            pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.p0 = array([x, y])
        self.updated = 0
        

if __name__ == '__main__':
    window = HelloWorldWindow(100)
    #event_logger = pyglet.window.event.WindowEventLogger()
    #window.push_handlers(event_logger)
    pyglet.clock.schedule_interval(window.update, 1/30)
    pyglet.app.run()
