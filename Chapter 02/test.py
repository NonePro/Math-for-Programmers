import random
from math import pi, cos, sin

from vector_drawing import *

dino_vectors = [
    (6, 4), (3, 1), (1, 2), (-1, 5), (-2, 5), (-3, 4), (-4, 4),
    (-5, 3), (-5, 2), (-2, 2), (-5, 1), (-4, 0), (-2, 1), (-1, 0), (0, -3),
    (-1, -4), (1, -4), (2, -3), (1, -2), (3, -1), (5, 1)
]


def add(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def draw_x_power_fun():
    draw(Points([0, 2]))
    draw(
        Points(
            *[(x, x ** 2) for x in range(-10, 10)]
        ),
        grid=(1, 10),
        nice_aspect_ratio=False
    )


def show_vector_add():
    v1 = [-1, 3]
    v2 = [2, 4]
    draw(
        Arrow(v1, color=blue),
        Arrow(v2, color=purple),
        Arrow(add(v1, v2), color=green)
    )


def move_dino():
    t = [-2, -3]
    dino_vectors2 = [add(v, t) for v in dino_vectors]
    arrows = [
        Arrow(add(v, t), v, color=gray) for v in dino_vectors
    ]
    draw(
        *arrows,
        Points(*dino_vectors, color=blue),
        Polygon(*dino_vectors, color=blue),
        Points(*dino_vectors2, color=red),
        Polygon(*dino_vectors2, color=red),
    )


def draw_mult_dino(row_num=10, col_num=10):
    dino_list = [
        Polygon(*[add(v, [i * 12, j * 12]) for v in dino_vectors])  # 整体移动点
        for i in range(col_num)  # 绘制列
        for j in range(row_num)  # 绘制行
    ]
    draw(*dino_list, grid=(10, 10))


def translate(translation, vec_list):
    return [add(v, translation) for v in vec_list]


def draw_mult_dino_v2(row_num=10, col_num=10):
    """
    教程使用方法：这个方法更加强化变换的概念，首先成成了多个变换向量；然后明确的定义了批量变换函数
    个人实现版本没有强调变换函数，上述两个点虽然都有涉及，但都没有强化
    """
    trans = [[i * 10, j * 10] for i in range(col_num) for j in range(row_num)]  # 生成变换向量
    dinos = [Polygon(*translate(tran, dino_vectors)) for tran in trans]  # 调用变换函数
    draw(*dinos, grid=(10, 10))


def scale(s, vec):
    return s * vec[0], s * vec[1]


def liner_components():
    u = [-1, 1]
    v = [1, 1]
    points = [add(scale(random.uniform(-3, 3), u), scale(random.uniform(-1, 1), v)) for _ in range(600)]
    draw(Points(*points))


def to_cartesian(p):
    return [p[0] * cos(p[1]), p[0] * sin(p[1])]


def draw_flower():
    polar_coords = [(cos(x * pi / 100.0), x * pi / 500.0) for x in range(0, 1000)]
    vector_list = [to_cartesian(p) for p in polar_coords]
    draw(Polygon(*vector_list, color=green))


if __name__ == "__main__":
    # move_dino()
    # demo translate

    # vector_list = [
    #    [1, 3], [5, 7], [9, 11]
    # ]
    # t = [4, 5]
    # print("{} translate by {} is {}".format(vector_list, t, translate(t, vector_list)))

    # draw_mult_dino(4, 4)
    # print([[i, j] for i in range(10) for j in range(10)])
    # draw_mult_dino_v2()
    # draw_mult_dino_v2(4, 4)
    # print("hello")

    # liner_components()
    draw_flower()
