from tkinter import *
import math

root = Tk()

canvas = Canvas(root,width=500,height=500)
canvas.pack()

x = 250
y = 250

mouse_x = 0
mouse_y = 0
mouse_pressed = False

def mouse_press(event):
    global mouse_pressed,mouse_x,mouse_y

    mouse_x = event.x
    mouse_y = event.y

    mouse_pressed = True

def mouse_release(event):
    global mouse_pressed

    mouse_pressed = False

root.bind('<Button-1>',mouse_press)
root.bind('<ButtonRelease-1>',mouse_release)

while True:
    try:
        canvas.delete(ALL)

        canvas.create_line(250,500,x,y,width=20)

        if mouse_pressed:
            dx = mouse_x-250
            dy = mouse_y-500

            a = math.atan2(dy,dx)
            x = 1
            y = a/x
            dist = math.sqrt(x**2,y**2)
            while dist < 250:


        root.update()

    except TclError:
        quit()
