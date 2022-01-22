import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from math import *


def normal(face):
    return tuple(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))


blues = matplotlib.cm.get_cmap('Blues')


def shade(face, color_map=blues, light=(1, 2, 3)):
    return color_map(1 - dot(unit(normal(face)), unit(light)))


faces = [
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    [(1, 0, 0), (0, 0, -1), (0, 1, 0)],
    [(1, 0, 0), (0, 0, 1), (0, -1, 0)],
    [(1, 0, 0), (0, -1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, 0, 1), (0, 1, 0)],
    [(-1, 0, 0), (0, 1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    [(-1, 0, 0), (0, 0, -1), (0, -1, 0)],
]
light = (1, 2, 3)

pygame.init()
display = (400, 400)  # 1
window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # 2

gluPerspective(45, 1, 0.1, 50.0)  # 1 设置透视角度和比例，设置渲染范围
glTranslatef(0.0, 0.0, -5)  # 2  场景位移
glRotatef(0, 0, 1, 1)
glEnable(GL_CULL_FACE)  # 3 自动隐藏视角不可见的面来优化算法
glEnable(GL_DEPTH_TEST)  # 4 根据深度动态检查是否渲染
glCullFace(GL_BACK)  # 5  自动隐藏面向视角，但是被其他物体遮挡的面

clock = pygame.time.Clock()  # 1 利用pygame的clock功能
while True:
    for event in pygame.event.get():  # 2 轮询所有事件，并响应退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    clock.tick()  # 3
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for face in faces:
        color = shade(face, blues, light)
        for vertex in face:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()
    pygame.display.flip()
    print(clock.get_fps())
