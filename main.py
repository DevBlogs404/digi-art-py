import math
import random

import numpy as np

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPen

from utils import QColor_HSV, save, Perlin2D
import painter

def draw(width,height,color=200,backgroundColor=(0,0,0),perlinFactorW=2,perlinFactorH=2,step=0.001):
    seed = random.randint(0,100000000)
    np.random.seed(seed)

    p = painter.Painter(width,height)

    #allow smooth drawing
    p.setRenderHint(p.Antialiasing)

    # draw bg color
    p.fillRect(0,0,width,height,QColor(*backgroundColor))

    #set pen color
    p.setPen(QPen(QColor(150,150,225,5),2))

    print('creating noise..')
    p_noise = Perlin2D(width,height,perlinFactorW,perlinFactorH)
    print('noise created')

    maxLength = 2 * width
    stepSize = step * max(width,height)
    num = int(width*height / 1000)
    points = [(random.randint(0,width-1),random.randint(0,height-1)) for i in range(num)]

    for k, (x_s,y_s) in enumerate(points):
        print(f'{100 * (k + 1) / len(points):.1f}'.rjust(5) + '% Complete', end='\r')

        c_len = 0

        while c_len < maxLength:
            sat = 200 * (maxLength -c_len) / maxLength
            hue = (color +130 *(height-y_s)/height) % 360
            p.setPen(QPen(QColor_HSV(hue,sat,255,20),2))

            angle = p_noise[int(x_s),int(y_s)] * math.pi

            x_f = x_s + stepSize * math.cos(angle)
            y_f = y_s + stepSize * math.sin(angle)

            p.drawLine(QPointF(x_s,y_s),QPointF(x_f,y_f))

            c_len +=  math.sqrt((x_f - x_s) ** 2 + (y_f -y_s) **2)

            if x_f < 0 or x_f >= width or y_f < 0 or y_f >= height or c_len > maxLength:
                break
            else:
                x_s,y_s = x_f,y_f

    save(p,fname=f'image_{seed}',folder="./images",overwrite=True)

draw(3000,2000,color=63,perlinFactorW=8,perlinFactorH=4,step=0.35)