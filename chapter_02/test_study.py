import math
import unittest
from vector_drawing import *


def add(*vectors):
    return tuple([sum(t) for t in zip(*vectors)])


class TestStudy(unittest.TestCase):
    def test_add(self):
        print(add(*[(1, 3), (5, 7)]))

    def test_circle(self):
        vectors = [(math.cos(math.pi * t / 6), math.sin(math.pi * t / 6)) for t in range(0, 36)]
        running_sum = (0, 0)
        # arrows = []
        # for i in range(len(vectors)):
        #    arrows.append(Arrow(vectors[(i + 1) % len(vectors)], vectors[i]))
        #    draw(*arrows)
        arrows = []
        for v in vectors:
            next_sum = add(running_sum, v)
            arrows.append(Arrow(next_sum, running_sum))
            running_sum = next_sum
        draw(*arrows)

    def test_draw_circle1(self):
        vectors = [(math.cos(math.pi * t / 6), math.sin(math.pi * t / 6)) for t in range(0, 36)]
        arrows = []
        for i in range(len(vectors)):
            arrows.append(Arrow(vectors[(i + 1) % len(vectors)], vectors[i]))
        draw(*arrows)
