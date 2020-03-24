try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import serial

import math
import time

root = Tk()

canvas = Canvas(root,width=1000,height=1000)
canvas.pack()

try:
    ser = serial.Serial('COM3',9600)
except:
    print('Serial Connection Failed')
    quit()

x_offset = 500
y_offset = 500

x = 177
y = -177

x2 = x+222
y2 = y+111

mouse_x = 0
mouse_y = 0
mouse_pressed = False

on_arm1 = False
on_arm2 = False

a1 = 270
a2 = 270

base_turning  = 0

arm1_pixels = []
arm2_pixels = []

class Button:
    def __init__(self,x,y,width,height,color='black',color2='red',text=''):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.color = color
        self.color2 = color2

        self.text = text

        self.pressed = False

        self.available = True

    def is_pressed(self,x,y):
        if x > self.x-self.width/2 and x < self.x+self.width/2:
            if y > self.y-self.height/2 and y < self.y+self.height/2:
                self.pressed = True
                return True
        self.pressed = False
        return False

    def render(self):
        if self.available:
            if not self.pressed:
                canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,self.x+self.width/2,self.y+self.height/2,fill=self.color)
                canvas.create_text(self.x,self.y,text=self.text,font=('TkTextFont',40))
            else:
                canvas.create_rectangle(self.x-self.width/3,self.y-self.height/3,self.x+self.width/3,self.y+self.height/3,fill=self.color2)
                canvas.create_text(self.x,self.y,text=self.text,font=('TkTextFont',30))

            self.pressed = False

for i in range(250):
    arm1_pixels.append([250,500-i])
    arm2_pixels.append([250,250-i])


def mouse_press(event):
    global mouse_pressed,mouse_x,mouse_y

    mouse_pressed = True
    mouse_x = event.x
    mouse_y = event.y

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

joint_1_angle = 0
joint_2_angle = 0

left = Button(200,600,100,50,'blue','red','Left')
right = Button(800,600,100,50,'blue','red','Right')

record = Button(400,650,150,75,'green','red','Record')
stop_record = Button(400,650,150,75,'red','black','Stop')
stop_record.available = False

play = Button(600,650,150,75,'green','red','Play')

recording = 0

r = []

a = 0

connection = True
data_sent = False
debug = False

while True:
    if data_sent and connection and not debug:
        print('Debug Message: ')
        debug = True

    if data_sent and connection and debug:
        #if not ser.readline()[0:-2].decode('ascii') == 'working':
        print(ser.readline().decode('ascii'))


    try:
        canvas.delete(ALL)

        canvas.create_line(x_offset,y_offset,x+x_offset,y+y_offset,width=40)
        canvas.create_line(x+x_offset,y+y_offset,x2+x_offset,y2+y_offset,width=40)

        canvas.create_oval(x+x_offset+30,y+y_offset+30,x+x_offset-30,y+y_offset-30,fill='black')
        canvas.create_oval(x_offset+30,y_offset+30,x_offset-30,y_offset-30,fill='black')
        canvas.create_rectangle(x_offset+100,y_offset+60,x_offset-100,y_offset,fill='gray')

        s = str(0)+','+str(int(joint_1_angle))+','+str(int(-joint_2_angle))+','

        ser.write(s.encode())
        if not data_sent:
            print('Data Successfully Sent')
            data_sent = True

        left.render()
        right.render()

        play.render()

        if mouse_pressed and left.is_pressed(mouse_x,mouse_y):
            base_turning = -1

        elif mouse_pressed and right.is_pressed(mouse_x,mouse_y):
            base_turning = 1

        else:
            base_turning = 0

        if mouse_pressed and stop_record.is_pressed(mouse_x,mouse_y) and stop_record.available and time.time() > a+1:
            recording = 0
            stop_record.available = False
            record.available = True
            a = time.time()

        if mouse_pressed and record.is_pressed(mouse_x,mouse_y) and record.available and time.time() > a+1:
            recording = 1
            record.available = False
            stop_record.available = True
            a = time.time()
            r = []


        if recording == 1:
            r.append([ex,dy1])

        if mouse_pressed and play.is_pressed(mouse_x,mouse_y):
            for i in r:
                dx1 = i[0]
                dy1 = i[1]

                d = get_dist(dx1,dy1,0,0)

                if d > x_offset:
                    a = math.asin(dy1/float(d))
                    if dx1 > 0:
                        dx1 = math.cos(a)*500
                    else:
                        dx1 = -math.cos(a)*500
                    dy1 = math.sin(a)*500
                    d = 500

                ex = dx1

                reversed = 0
                if dx1 < 0:
                    reversed = 1
                    dx1 = -dx1

                if dx1 == 0:
                    dx1 = .1

                a = math.acos(d/500.0)
                o = math.atan(dy1/float(dx1))
                j1 = -a+o
                if reversed:
                    j1 = (-(j1-math.radians(90)))+math.radians(90)

                j2 = math.acos((125000-d**2)/125000.0)

                a = j1

                a2 = math.degrees(-a)

                xs = 250*math.cos(a)
                ys = 250*math.sin(a)

                x = xs
                y = ys

                joint_2_angle = math.degrees(a)

                a = j2+math.radians(90)

                joint_1_angle = math.degrees(a)-90

                xs = 250*math.cos(a)
                ys = 250*math.sin(a)

                x2 = x+xs
                y2 = y+ys

                x2 = ex
                y2 = dy1

                canvas.delete(ALL)

                canvas.create_line(x_offset,y_offset,x+x_offset,y+y_offset,width=40)
                canvas.create_line(x+x_offset,y+y_offset,x2+x_offset,y2+y_offset,width=40)

                canvas.create_oval(x+x_offset+30,y+y_offset+30,x+x_offset-30,y+y_offset-30,fill='black')
                canvas.create_oval(x_offset+30,y_offset+30,x_offset-30,y_offset-30,fill='black')
                canvas.create_rectangle(x_offset+100,y_offset+60,x_offset-100,y_offset,fill='gray')

                canvas.create_text(100,50,text='Top Joint Angle: '+str(int(joint_1_angle))+'\nBottom Joint Angle: '+str(int(joint_2_angle)),font=('TkTextFont',15),fill='purple')

                root.update()


        record.render()
        stop_record.render()

        if mouse_pressed and mouse_y < 550:
            if True:
                if mouse_y > y_offset:
                    mouse_y = y_offset

                dx1 = mouse_x-x_offset
                dy1 = mouse_y-y_offset

                d = get_dist(dx1,dy1,0,0)

                if d > x_offset:
                    a = math.asin(dy1/float(d))
                    if dx1 > 0:
                        dx1 = math.cos(a)*500
                    else:
                        dx1 = -math.cos(a)*500
                    dy1 = math.sin(a)*500
                    d = 500

                ex = dx1

                reversed = 0
                if dx1 < 0:
                    reversed = 1
                    dx1 = -dx1

                if dx1 == 0:
                    dx1 = .1

                a = math.acos(d/500.0)
                o = math.atan(dy1/float(dx1))
                j1 = -a+o
                if reversed:
                    j1 = (-(j1-math.radians(90)))+math.radians(90)

                j2 = math.acos((125000-d**2)/125000.0)

                a = j1

                a2 = math.degrees(-a)

                xs = 250*math.cos(a)
                ys = 250*math.sin(a)

                x = xs
                y = ys

                joint_2_angle = math.degrees(a)

                a = j2+math.radians(90)

                joint_1_angle = math.degrees(a)-90

                xs = 250*math.cos(a)
                ys = 250*math.sin(a)

                x2 = x+xs
                y2 = y+ys

                x2 = ex
                y2 = dy1

            elif not on_arm1:
                for i in arm2_pixels:
                    if get_dist(mouse_x,mouse_y,i[0],i[1]) < 20:
                        on_arm2 = True




        root.update()

    except TclError:
        quit()
