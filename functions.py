import math

def lerp(a, b, p):
	return a + (b - a) * p

def ignition_time(a, b, c, t):
	# a - Gravitational acceration
	# b - Current velocity
	# c - Current altitude
	# t - Acceleration on powered descent

	# The discriminant
	D = b**2 - 4*a*c

	# New a
	na = a + t

	# The time (in seconds) until iginition for optimal landing.
	k = -(math.sqrt(t * na * D) + b * t) / (2 * a * t)

	# The time until touchdown if ignition occures at k
	x = (2*t*k - b) / (2 * na)

	return k, x


def get_positive_area(b, v, c):
	# 2a
	_2a = v-b

	# a
	a = _2a/2

	# Discriminant 
	D = b**2 - 4 * a * c

	# Square root of the discriminant if it's not imaginary and if it is, replace it with 0.
	D_ = math.sqrt(D) if D >= 0 else 0

	# The area of the rectangle with 2 edges lying on the positive y and negative x axis and the top edge at y = c where c is the intersection point of the paraboly with the y axis, and the left edge at the x = x₀ where x₀ is the center of the parabola.
	cx0 = c * -b / _2a

	return (D_**3 + b**3) / (12*a**2) + cx0