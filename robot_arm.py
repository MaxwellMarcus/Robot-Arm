try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import math

root = Tk()

canvas = Canvas(root,width=500,height=500)
canvas.pack()

x = 250
y = 250

x2 = 250
y2 = 0

mouse_x = 0
mouse_y = 0
mouse_pressed = False

on_arm1 = False
on_arm2 = False

a1 = 90
a2 = 90

arm1_pixels = []
arm2_pixels = []
for i in range(250):
    arm1_pixels.append([250,500-i])
    arm2_pixels.append([250,250-i])


def mouse_press(event):
    global mouse_pressed

    mouse_pressed = True

def mouse_release(event):
    global mouse_pressed,on_arm1,on_arm2

    mouse_pressed = False
    on_arm1 = False
    on_arm2 = False

def mouse_move(event):
    global mouse_x,mouse_y

    mouse_x = event.x
    mouse_y = event.y

def get_dist(x1,y1,x2,y2):
    x = abs(x1-x2)
    y = abs(y1-y2)
    return math.sqrt(x**2+y**2)

root.bind('<Button-1>',mouse_press)
root.bind('<ButtonRelease-1>',mouse_release)
root.bind('<Motion>',mouse_move)

while True:
    try:
        canvas.delete(ALL)

        canvas.create_line(250,500,x,y,width=20)

        canvas.create_line(x,y,x2,y2,width=20)

        canvas.create_text(100,50,text='Top Joint Angle: '+str(int(a2))+'\nBottom Joint Angle: '+str(int(a1)),font=('TkTextFont',15),fill='purple')

        print('Bottom Joint Angle: ' + str(a1) + '  Top Joint Angle: ' + str(a2))

        if mouse_pressed:
            if on_arm1:
                dx = mouse_x-250
                dy = mouse_y-500

                a = math.atan2(dy,dx)

                a1 = math.degrees(-a)

                xs = math.cos(a)
                ys = math.sin(a)

                x1 = 250
                y1 = 500
                dist = get_dist(250,500,x1,y1)
                arm1_pixels = []
                while dist < 250:
                    x1 += xs
                    y1 += ys

                    arm1_pixels.append([x1,y1])

                    dist = get_dist(250,500,x1,y1)
                x = x1
                y = y1


                xs = arm2_pixels[1][0]-arm2_pixels[0][0]
                ys = arm2_pixels[1][1]-arm2_pixels[0][1]

                x1 = x
                y1 = y
                dist = get_dist(x,y,x1,y1)
                arm2_pixels = []
                while dist < 250:
                    x1 += xs
                    y1 += ys

                    arm2_pixels.append([x1,y1])

                    dist = get_dist(x,y,x1,y1)
                x2 = x1
                y2 = y1
            elif not on_arm2:
                for i in arm1_pixels:
                    if get_dist(mouse_x,mouse_y,i[0],i[1]) < 20:
                        on_arm1 = True

            if on_arm2:
                dx = mouse_x-x
                dy = mouse_y-y

                a = math.atan2(dy,dx)

                a2 = math.degrees(-a)

                xs = math.cos(a)
                ys = math.sin(a)

                x1 = x
                y1 = y
                dist = get_dist(x,y,x1,y1)
                arm2_pixels = []
                while dist < 250:
                    x1 += xs
                    y1 += ys

                    arm2_pixels.append([x1,y1])

                    dist = get_dist(x,y,x1,y1)
                x2 = x1
                y2 = y1
            elif not on_arm1:
                for i in arm2_pixels:
                    if get_dist(mouse_x,mouse_y,i[0],i[1]) < 20:
                        on_arm2 = True




        root.update()

    except TclError:
        quit()
