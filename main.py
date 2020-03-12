import pygame, sys
import math
import numpy as np
import time
import random
import threading
from vectorClass import Vector, findOrginial

size = width, height = 800,800
black = 0, 0, 0

x_offset = width/2
y_offset = height/2

k = 9*10**9


def visiable(charge_pos, point):
    
    # charge to point will be the second line segment and check against obstacles
    ray = findOrginial(charge_pos,(point[0]+x_offset,point[1]+y_offset)).normal()
    ray = (charge_pos[0],charge_pos[1],charge_pos[0]+ray.x,charge_pos[1]+ray.y)
    # pygame.draw.aaline(screen,(0,255,0),(ray[0],ray[1]),(ray[2],ray[3]))

    closest = None
    for i in obstacles:
        den = (i[0]-i[2])*(ray[1]-ray[3])-(i[1]-i[3])*(ray[0]-ray[2])
        if den == 0:
            continue
        norm = (i[0]-ray[0])*(ray[1]-ray[3])-(i[1]-ray[1])*(ray[0]-ray[2])

        t = norm*1.0/den

        u = -((i[0]-i[2])*(i[1]-ray[1])-(i[1]-i[3])*(i[0]-ray[0]))/1.0*(den)

        if t > 0 and t < 1 and u > 0:
            intersactionpoint = ((i[0]+t*(i[2]-i[0])),(i[1]+t*(i[3]-i[1])))
            intersactionlen = math.sqrt((intersactionpoint[0]-ray[0])**2+(intersactionpoint[1]-ray[1])**2)
            if closest == None or intersactionlen < math.hypot(closest[0]-ray[0],closest[1]-ray[1]):
                closest = intersactionpoint

    if closest != None:
        shadow_ray_len = math.hypot(closest[0]-charge_pos[0],closest[1]-charge_pos[1])
        Point_charge_len = math.hypot(point[0]+x_offset-charge_pos[0],point[1]+y_offset-charge_pos[1])
        if Point_charge_len < shadow_ray_len:
            return None
        else:
            return closest
    else:
        return None


# return magnitude of the electric force at a point 
def fieldAtPoint(Point):
    fieldVector = Vector(0,0,0)
    for i in charges:
        shadow_ray = visiable((i[0],i[1]),Point)
        if shadow_ray != None:
            continue
        i = (i[0]-x_offset,i[1]-y_offset,i[2])
        r = findOrginial(i,Point)
        rlen = r.len
        if r.len == 0:
            # r.len = 0.000000001
            # rlen = r.len
            continue
        r = r.normal()
        E = r.scaleVector((k*i[2])/(rlen)**2)
        fieldVector = fieldVector.add(E)

    # the arctan will set a limit as x approches infinity
    fieldVector = fieldVector.normal().scaleVector(30*math.atan(1/10*(fieldVector.len)))
    fieldVector = Vector(fieldVector.x+Point[0],fieldVector.y+Point[1],0)
    return fieldVector

def chargeClicked(Point):
    for i in charges:
        distance = findOrginial((i[0],i[1]),Point)
        if distance.len <= 15:
            return charges.index(i)
    return -1


pygame.init()
screen = pygame.display.set_mode(size)

# charges list contain (x_postiton,y_position,charge_strength) and obstecales contain the lines as obstecales for the electric field (x1,y1,x2,y2)
charges = []
obstacles = [(300,300,300,600),(300,300,100,300),(500,500,500,700)]

# creates a charge at a random position with a random sign
for i in range(3):
    ch_x = random.randint(0,width)
    ch_y = random.randint(0,height)
    if random.randint(0,1) == 0:
        sign = -1
    else:
        sign = 1
    charges.append((ch_x,ch_y,sign*30*10**-6))

last_pressed_mouse = time.time()
mouse_pressed = 0
pressedCharge = -1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)


    # detect the charge that got pressed and release it on second click
    if time.time()-last_pressed_mouse > 0.18:
        if mouse_pressed == 0 and pygame.mouse.get_pressed()[0] == 1:
            pressedCharge = chargeClicked(pygame.mouse.get_pos())
            if pressedCharge != -1:
                last_pressed_mouse = time.time()
                mouse_pressed = 1
                mouse_pos1 = pygame.mouse.get_pos()
        elif mouse_pressed == 1 and pygame.mouse.get_pressed()[0] == 0:
            charges[pressedCharge] = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],charges[pressedCharge][2])
        elif mouse_pressed == 1 and pygame.mouse.get_pressed()[0] == 1:
            mouse_pressed = 0
            last_pressed_mouse = time.time()


    # draw the charges and the electric fields vectors
    for i in charges:
        if i[2] < 0:
            pygame.draw.circle(screen,(45,0,255),(int(i[0]),int(i[1])),15)
        elif i[2] > 0:
            pygame.draw.circle(screen,(255,0,0),(int(i[0]),int(i[1])),15)

    for i in obstacles:
        pygame.draw.aaline(screen,(0,255,0),(i[0],i[1]),(i[2],i[3]))


    # for future use to implemnt threading
    # for i in range(10):
    #     threading.Thread(target=fieldAtPoint, args=())


    for i in np.linspace(-x_offset,x_offset,40):
        for q in np.linspace(-y_offset,y_offset,40):
            v = fieldAtPoint((i,q))
            if math.hypot(i-v.x,q-v.y) != 0:
                pygame.draw.aaline(screen,(200,200,200),(i+x_offset,q+y_offset),(round(v.x)+x_offset,round(v.y)+y_offset))

    pygame.display.flip()
    pygame.display.update()