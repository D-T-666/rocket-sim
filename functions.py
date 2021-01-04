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


def area_of_parabola(a, b, c):
	x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
	x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)

	y = ((4*a*c)-(b*b))/(4*a)

	tot_area = abs(x2-x1)*abs(y)*(1/3)

	x1 = b/a

	sub_tot_area = tot_area - c * x1 / 2 

	sub_tot_area -= x1 * (y - c) * (1 / 3)
	
	return tot_area, sub_tot_area