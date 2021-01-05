import numpy as np
import math
from functions import *


class Rocket():
	def __init__(self, mass, alt, fuel, thrust, fuel_consumption, vel, state,
				 target_alt):
		self.mass = mass
		self.alt = alt
		self.fuel = fuel
		self.thrust = thrust
		self.vel = vel
		self.acc = 0
		self.throttle = 0
		self.fuel_consumption = 10
		self.state = state
		self.target_alt = target_alt
		self.pid = {'p': 0, 'i': 0, 'd': 0}
		self.a = 0
		self.b = 0
		self.c = 0

		self.data_keys = [
			'mass', 'alt', 'fuel', 'thrust', 'vel', 'acc', 'throttle', 'ed1', 'ed2',
			'fire_alt', 'a', 'b', 'c'
		]

	def update(self, time_steps=1):
		self._physics(time_steps)

		self._guidance(time_steps)

		return {
			'alt': self.alt,
			'vel': self.vel,
			'acc': -self.acc,
			'throttle': self.throttle,
			'fuel': self.fuel,
			'ed1': self.estimated_distance()[0],
			'ed2': self.estimated_distance()[1],
			'a': self.a, 
			'b': self.b,
			'c': self.c
		}

	def _physics(self, time_steps):
		if self.alt <= 0:
			return True

		self.acc = -self.thrust * (self.throttle
								   if self.fuel >= 1 else self.throttle *
								   self.fuel) / (self.mass + self.fuel) + 9.8

		self.vel -= self.acc / time_steps
		self.alt += self.vel / time_steps

		if self.fuel * time_steps >= self.throttle:
			self.fuel -= self.throttle * self.fuel_consumption / time_steps
			if self.fuel < 0:
				self.fuel = 0

	def _guidance(self, time_steps):
		self.pid['p'] = 0.4 * (self.target_alt - self.alt)
		self.pid['i'] += 0.02 * (self.vel) / time_steps
		self.pid['d'] = -2 * self.vel

		if self.state == 'landing':
			if self.estimated_distance()[0] > self.alt+1:
				self.throttle = 1
				self.state = 'out of control'
			else:
				self.throttle = 0

		elif self.state == 'hover':
			self.throttle = (9.8 + self.pid['p'] + self.pid['i'] + self.pid['d']) \
							/ (self.thrust / (self.mass + self.fuel))
			if self.throttle > 1:
				self.throttle = 1
			elif self.throttle < 0:
				self.throttle = 0 

			if abs(self.vel) < 0.01 and self.alt > 110:
				# self.state = 'landing'
				# self.target_alt = 0
				pass

		# if self.vel > 10:
		# 	self.throttle = 9.79/(self.thrust / (self.mass + self.fuel))

	def estimated_distance(self):
		x0 = -9.8 + self.thrust / (self.mass + self.fuel - self.fuel_consumption * 0.0)
		x1 = -9.8 + self.thrust / (self.mass + self.fuel - self.fuel_consumption * 0.01)
		x2 = -9.8 + self.thrust / (self.mass + self.fuel - self.fuel_consumption * 1.0)
		x3 = -9.8 + self.thrust / (self.mass + self.fuel - self.fuel_consumption * 1.01)

		# Derivative at x=0 and x=1
		u = -x1/x0
		v = -x3/x2
		# Initial height at x=0
		y = abs(self.vel)

		# print(u, v, y)

		# ===
		
		mass = self.mass + self.fuel
		net_acc = self.thrust / mass - 9.8
		time_to_stop = self.vel / net_acc
		time_to_stop = time_to_stop if time_to_stop < self.fuel else self.fuel
		estimated_distance = self.vel * time_to_stop / 2 - self.vel / 2
		
		return [get_positive_area(u, v, y), estimated_distance]


def run():
	data = {}
	r = Rocket(mass=100,
			   alt=1,
			   fuel=250,
			   thrust=4500,
			   fuel_consumption=10,
			   vel=0,
			   state='hover',
			   target_alt=1000)

	for key in r.data_keys:
		data[key] = []

	for i in range(0, 600, 1):
		for k, v in r.update(time_steps=10).items():
			data[k].append(v)

		if i == 300:
			r.state = 'landing'

	return data
