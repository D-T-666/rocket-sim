import math

def lerp(a, b, p):
    return a + (b - a) * p

def get_parabola(u, v):
    a = (v - u) / 2
    b = u
    c = u
    return a, b, c

def area_of_parabola(a, b, c):
	x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
	x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)

	y = ((4*a*c)-(b*b))/(4*a)

	tot_area = abs(x2-x1)*abs(y)*(1/3)

	x1 = b/a

	sub_tot_area = tot_area - c * x1 / 2 

	sub_tot_area -= x1 * (y - c) * (1 / 3)
	
	return tot_area, sub_tot_area