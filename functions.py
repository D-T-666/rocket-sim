import math
import numpy as np





def lerp(a, b, p):
    return a + (b - a) * p


def get_parabola(u, v, y):
    a = (v - u) / 2
    b = u
    c = y
    return a, b, c


def get_area(w, h):
    return w * h * (2 / 3)


def get_vertex(a, b, c):
    x = -b / (2 * a)
    y = a*x**2 + b*x + c
    return x, y


def get_width(a, b, c):
    # Find the intersections
    # and define the width as the distance inbetween
    r1, r2 = np.roots([a, b, c])

    if np.iscomplex(r1) or np.iscomplex(r2):
        raise ValueError('Roots for parabola may not be complex')

    w = abs(r2 - r1)
    return w


def get_positive_area(u, v, y):
    # Extract a, b, c for the parabola
    a, b, c = get_parabola(u, v, y)

    # Vertex of the parabola
    px, py = get_vertex(a, b, c)

    # Area of the big parabola
    w_big = get_width(a, b, c)
    area_big = get_area(w_big, py)

    # Area of the small parabola
    w_small = get_width(a, b, 0)
    h_small = py - y
    area_small = get_area(w_small, h_small)

    # Area of the inferior rectangle
    area_rect = w_small * y

    # The difference between the big parabola
    # and the small parabola plus the rectangle
    final_area = area_big - area_small - area_rect

    # Divide by 2 before returning, to only include the righthand side
    return final_area / 2