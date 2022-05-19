'''
this code is not good
2022.4.
增加了用鼠标左键控制平移的操作方式 -2022.5.x

'''


import pygame
import numpy as np
import sys
import math
import copy

def cha(a,b):
    '''根据平面直角坐标计算极坐标中的θ'''
    '''Calculate θ in polar coordinates from plane Cartesian coordinates'''
    r = (a**2+b**2)**(1/2)
    if abs(a /r) < 0.5:
        theta = math.acos(a/r)
        theta = math.pi - np.sign(b)*(math.pi - theta)
    else:
        theta = math.asin(b/r)
        theta = math.pi/2 - np.sign(a)*(math.pi/2 - theta)
    return theta


def cast(vector,plane):
    '''计算一个向量投影在平面上后对应的向量'''
    '''Calculate the vector corresponding to the projection of a vector onto the plane'''
    if abs(plane[0]@plane[1])!=0:
        # raise RuntimeError('平面向量不互相垂直')
        print('平面向量点积:',plane[0]@plane[1])
    plane[0] /= np.sum(plane[0]**2)**(1/2)
    plane[1] /= np.sum(plane[1]**2)**(1/2)
    return np.array([vector@plane[0],vector@plane[1]])

def cast_plane(plane):
    plane = plane.reshape(4,4)
    newPlane = np.zeros((4,2),dtype='float')
    for i in range(4):
        newPlane[i] = cast(plane[i], viewPlane)
    print(newPlane)
    temp = newPlane[2].copy()
    newPlane[2] = newPlane[3]
    newPlane[3] = temp
    return newPlane

def rotate(ori,plane):
    '''计算一个平面沿着某个旋转自由度旋转一定角度（0.02)后返回的平面'''
    '''Calculates the plane returned after a plane is rotated by a certain angle (0.02) along a rotational direction'''
    for i in range(2):
        a=(plane[i][ori[0]]**2+plane[i][ori[1]]**2)**(1/2)
        if a ==0:
            continue
        theta = cha(plane[i][ori[0]], plane[i][ori[1]])

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            theta -= 0.02
        else:
            theta += 0.02
        print('theta: ',theta)
        plane[i][ori[0]] , plane[i][ori[1]]=a*math.cos(theta), a*math.sin(theta)
        print('plane: ',plane)
    return plane

class shape:
    # lines = []
    lineColor = (255,255,255)
    planeColor = (255,25,0)


    def draw_shape(self):
        for plane in self.planes:
            print('画平面')
            print(plane)
            castPlane =cast_plane(plane)
            for i in range(4):
                castPlane[i][0]+=pos[0]
                castPlane[i][1]+=pos[1]
            #pygame.draw.polygon(screen, self.planeColor, castPlane)

        for line1 in self.lines:
            pygame.draw.line(screen, self.lineColor, [cast(line1[0], viewPlane)[0] + pos[0], \
                                                      cast(line1[0], viewPlane)[1] + pos[1]],
                             [cast(line1[1], viewPlane)[0] + pos[0], \
                              cast(line1[1], viewPlane)[1] + pos[1]])


#所有表示一个四维立方体的的点和线
#points and lines that represent a 4-D cube
class cube(shape):
    # points=np.array([[0,0,0,0]])
    # lines = []
    def __init__(self, sideLength=100, startPoint=[[0,0,0,0]], dimension = 4):
        self.lines = np.array([])
        self.points = np.array(startPoint)
        self.planes = np.array([])
        for i in range(0, dimension):
            for plane in self.planes.copy():
                for line in plane:
                    for point in line:
                        point[i]+=sideLength
                self.planes = np.append(self.planes,plane)
            print(self.lines)
            for line in self.lines.copy():
                temp = line.copy()
                line[0][i]+=sideLength
                line[1][i]+=sideLength
                self.lines = np.append(self.lines,line)
                self.planes = np.append(self.planes,np.array([temp,line])).reshape(-1,2,2,4)
                # print('lines:')
                # print(lines)
            for point in self.points.copy():
                temp = copy.deepcopy(point)
                point[i]=point[i]+sideLength
                self.points = np.append(self.points, np.array([point]), 0)
                print('lines',self.lines)
                self.lines = np.append(self.lines, np.array([[temp,point]])).reshape(-1,2,4)


#plane是一个平面，用两个四维向量表示，平面平行于这两个四维向量
viewPlane = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype='float')
# 平面的位置，不重要
pos=[0,0]
cube0 = cube(100,[[50,50,50,50]],4)
cube1 = cube(sideLength=200, dimension=3)
cube0.lineColor = (255,0,255)
cube1.planeColor=(0,255,255)
#pygame框架，不重要
pygame.init()
screen=pygame.display.set_mode((1000,600)) #
pygame.display.set_caption("4D显示")
fClock = pygame.time.Clock()
#主循环：
#控制平面移动时，平面移动的速度
movespeed = 8
# print(cube0.planes)

def main():
    global viewPlane
    global pos 
    global cube0,cube1
    global screen,fClock
    global movespeed

    mousePressed = False

    while True:
        #按键反应，方向键控制平面移动，数字键0123的两两组合控制平面旋转。shift控制是否反向旋转
        rotalist=[]
        if pygame.key.get_pressed()[pygame.K_UP]:
            pos[1] -= movespeed
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            pos[1] += movespeed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            pos[0] += movespeed
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            pos[0] -= movespeed

        # 鼠标左键控制移动    
        if mousePressed:
            rel = pygame.mouse.get_rel()
            pos[0]+=rel[0]
            pos[1]+=rel[1]
        if pygame.key.get_pressed()[pygame.K_1]:
            rotalist.append(0)
        if pygame.key.get_pressed()[pygame.K_2]:
            rotalist.append(1)
        if pygame.key.get_pressed()[pygame.K_3]:
            rotalist.append(2)
        if pygame.key.get_pressed()[pygame.K_4]:
            rotalist.append(3)
        if len(rotalist) == 2:
            viewPlane=rotate(rotalist, viewPlane)

        # 不重要
        screen.fill(pygame.Color('black'))

        # 在屏幕上绘制线
        cube1.draw_shape()
        cube0.draw_shape()

        #不重要
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # 鼠标左键控制移动
            if event.type == pygame.MOUSEBUTTONDOWN:
                rel = pygame.mouse.get_rel()
                mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False

        pygame.display.update()
        pygame.display.set_caption("4D显示"+str(list((map(lambda x:list(map(lambda \
                    x:round(x,2),x)),viewPlane)))))    #后面一长串是显示平面的转角，以标题栏能装下的方式

        # 控制帧率
        fClock.tick(16)

if __name__ == '__main__':
    main()


