#! /usr/bin/env python

import pyglet

w = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=w.width//2, y=w.height//2,
                          anchor_x='center', anchor_y='center')

@w.event
def on_draw():
    w.clear()
    label.draw()

pyglet.app.run()
