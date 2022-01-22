import math
import unittest

import matplotlib.cm

from chapter_03.draw2d import draw2d, Polygon2D
from draw3d import *

octahedron = [
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    [(1, 0, 0), (0, 0, -1), (0, 1, 0)],
    [(1, 0, 0), (0, 0, 1), (0, -1, 0)],
    [(1, 0, 0), (0, -1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, 0, 1), (0, 1, 0)],
    [(-1, 0, 0), (0, 1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    [(-1, 0, 0), (0, 0, -1), (0, -1, 0)],
]
blues = matplotlib.cm.get_cmap('Blues')


def add(*vectors):
    # return tuple(map(sum, zip(*vectors)))
    # 虽然上面的写法更简洁，但并不推荐map，使用下面的列表推导更加具有python风格
    return tuple([sum(coords) for coords in zip(*vectors)])


def length(vector):
    return math.sqrt(sum([x ** 2 for x in vector]))


def scale(scalar, v):
    return tuple(scalar * coord for coord in v)


def vector_with_whole_number_length(max_coord=100):
    for x in range(1, max_coord):
        for y in range(1, x + 1):
            for z in range(1, y + 1):
                if length((x, y, z)).is_integer():
                    yield x, y, z


def dot(vector_1, vector_2):
    # return sum([v[0] * v[1] for v in zip(vector_1, vector_2)])
    # 如果是元组，可以直接接收返回
    return sum([a * b for a, b in zip(vector_1, vector_2)])


def cross(u, v):
    ux, uy, uz = u
    vx, vy, vz = v
    return uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx


def angle_between(v1, v2):
    return math.acos(dot(v1, v2) / (length(v1) * length(v2)))


def vertices(faces):
    # return [vertex for vertex in face for face in faces ]
    # 这个循环竟然是从前往后的，如果写成上面的形式，会提示face未定义
    # set 作用主要是利用集合元素唯一性的特点进行去重
    return list(set([vertex for face in faces for vertex in face]))


def component(v, direction):
    """
    将向量投射到特定方向;
    如分别将一个向量投射到x,y轴就能获取到该向量在xy平面上的投影
    因为处理的是向量的一个维度，所以叫component
    """
    return dot(v, direction) / length(direction)


def vector_to_2d(v):
    return component(v, (1, 0, 0)), component(v, (0, 1, 0))


def face_to_2d(face):
    return [vector_to_2d(vertex) for vertex in face]


def subtract(u, v):
    return tuple([a - b for a, b in zip(u, v)])


def unit(v):
    """获取一个向量的单位向量"""
    return scale(1 / length(v), v)


def normal(face):
    return cross(subtract(face[2], face[0]), subtract(face[1], face[0]))


def render(faces, light=(1, 2, 3), color_map=blues, lines=None):
    polygons = []
    for face in faces:
        # 求平面的法向量
        unit_normal = unit(normal(face))
        if unit_normal[2] > 0:
            c = color_map(dot(unit(normal(face)), unit(light)))
            p = Polygon2D(*face_to_2d(face), fill=c, color=lines)
            polygons.append(p)

    draw2d(*polygons, axes=False, origin=False, grid=None)


def split(face):
    midpoints = tuple(unit(add(face[i], face[(i + 1) % len(face)])) for i in range(0, len(face)))
    triangles = [(face[i], midpoints[i], midpoints[(i - 1) % len(face)]) for i in range(0, len(face))]
    return [midpoints] + triangles


def rec_split(faces, depth=0):
    if depth == 0:
        return faces
    else:
        return rec_split([new_face for face in faces for new_face in split(face)], depth - 1)


def sphere_approx(n):
    """模拟球形"""
    return rec_split(octahedron, n)


class TestStudy(unittest.TestCase):
    def test_draw_sphere(self):
        render(sphere_approx(3), lines='k')

    def test_split(self):
        # points = split([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        points = split([(1, 0), (0, 1)])
        print(points)
        # draw3d(Points3D(*points))

    def test_draw_octahedron(self):
        print(octahedron)
        render(octahedron, color_map=matplotlib.cm.get_cmap('Blues'), lines=black)
        # render(octahedron, light={0, -3, -3}, color_map=matplotlib.cm.get_cmap('Reds'), lines=black)

    def test_vertices(self):
        print("支持去重复: {}".format(vertices([[(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]])))

    def test_zip(self):
        # 先讲对应坐标整理到一个元组内，然后用sum方法求和
        zipped = zip((1, 2, 3), (4, 5, 6), [7, 8, 9])
        # print(list(zipped)) # 通过 list 迭代一次后，再次迭代会为空
        adder = [sum(c) for c in zipped]
        print(adder)
        # tuple 将列表转换为元组
        print(tuple(adder))

    def test_sum(self):
        print("一维列表sum([1,2,3])={}".format(sum([1, 2, 3])))

    def test_subtract(self):
        print(subtract((4, 5, 6), (1, 2, 3)))

    def test_draw_cube(self):
        nums = [-1, 1]
        vector_list = [(x, y, z) for x in nums for y in nums for z in nums]
        draw3d(Points3D(*vector_list))
        edges = [((-1, y, z), (1, y, z)) for y in nums for z in nums] + \
                [((x, -1, z), (x, 1, z)) for x in nums for z in nums] + \
                [((x, y, -1), (x, y, 1)) for x in nums for y in nums]
        draw3d(*[Segment3D(*edge) for edge in edges])
        print("hello")

    def test_draw_points(self):
        draw3d(
            Points3D((2, 2, 2), (1, -2, -2))
        )

    def test_add(self):
        print(add((1, 3, 5), (2, 4, 6), (3, 4, 5)))
        print(add((1, 1, 3), (2, 4, -4), (4, 2, -2)))

    def test_length(self):
        print(length((3, 4, 12)))
        print(add((4, 0, 3), (-1, 0, 1)))
        v1 = (4, 0, 3)
        v2 = (-1, 0, 1)
        draw3d(
            Arrow3D(v1, color=red),
            Arrow3D(v2, color=blue),
            Arrow3D(add(v1, v2), v1, color=green),
            Arrow3D(add(v1, v2), color=purple),
            Arrow3D(v2, add(v1, v2), color=gray)
        )

    def test_draw_helix_shape(self):
        vs = [(math.sin(pi * t / 6), math.cos(pi * t / 6), 1.0 / 3) for t in range(0, 24)]
        running_sum = (0, 0, 0)
        arrows = []
        for v in vs:
            next_sum = add(running_sum, v)
            arrows.append(Arrow3D(next_sum, running_sum))
            running_sum = next_sum
        print(running_sum)
        draw3d(*arrows)

    def test_draw_helix_shape_v2(self):
        vs = [(math.sin(pi * t / 6), math.cos(pi * t / 6), t * 1.0 / 12) for t in range(0, 24)]
        arrows = []
        for i in range(len(vs)):
            arrows.append(Arrow3D(vs[min(i + 1, len(vs) - 1)], vs[i], color=blue))

        draw3d(*arrows)

    def test_scale(self):
        print(scale(2, (1, 3, 5)))
        print(scale(2, (1, 5)))

    def test_whole_number_length(self):
        for v in vector_with_whole_number_length():
            print("{}.length={}".format(v, length(v)))

    def test_dot(self):
        print(dot((1, 2, 3), (4, 5, 6)))
        print("{}*{}={}".format((1, 0), (0, 2), dot((1, 0), (0, 2))))
        print("{}*{}={}".format((0, 3, 0), (0, 0, -5), dot((0, 3, 0), (0, 0, -5))))
        print(dot((3, 4), (2, 3)))
        print(dot(scale(2, (3, 4)), (2, 3)))
        print(dot((3, 4), scale(2, (2, 3))))

    def test_angle_between(self):
        print(angle_between((4, 3), (3, 4)))
        print(angle_between((4, 3, 6), (3, 4, 8)))

    def test_cross(self):
        print(cross((0, 2, 0), (0, 0, -2)))
        print(cross((1, 1, 0), (-2, 1, 0)))
        print(cross((0, 0, 3), (0, -2, 0)))
        print(length((6, 0, 0)))
        u = (4, 1, 9)
        v = (-2, 7, 0)
        print("_____")
        print(length(u) * length(v) * math.sin(angle_between(u, v)))
        print("by cross get {} and length is {}".format(cross(u, v), length(cross(u, v))))
