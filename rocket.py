import math

import numpy as np
from rich import print

from functions import *
from pid import PID


GRAVITY = 9.8


class Rocket:
	def __init__(self, dry_mass, fuel, altitude, velocity, fuel_consumption, thrust):
		# Massive properties
		self.dry_mass = dry_mass
		self.fuel = fuel

		# Location & Motion
		self.altitude = altitude
		self.velocity = velocity
		self.acceleration = 0

		# Operational & Engine
		self.fuel_consumption = fuel_consumption
		self.thrust = thrust
		self.throttle = 0
		
	@property
	def total_mass(self):
		return self.dry_mass + self.fuel

	def dict(self):
		return {
			'dry_mass': self.dry_mass,
			'fuel': self.fuel,

			'altitude': self.altitude,
			'velocity': self.velocity,
			'acceleration': self.acceleration,

			'fuel_consumption': self.fuel_consumption,
			'thrust': self.thrust,
			'throttle': self.throttle,

			'estimated_distance': self.estimated_distance()
		}

	def reset_motion(self):
		self.altitude = 1
		self.velocity = 0
		self.acceleration = 0

	def update(self, t=1):
		""" Update the physical properties """

		# Update acceleration based on available fuel & throttle
		throttle = self.throttle if self.fuel >= 1 else self.throttle * self.fuel
		self.acceleration = self.thrust * throttle / self.total_mass - GRAVITY

		self.velocity += self.acceleration / t
		self.altitude += self.velocity / t
		
		# Collide with the ground
		if self.altitude <= 0:
			self.reset_motion()

		# Update remaining fuel
		if self.fuel * t >= self.throttle:
			self.fuel -= self.throttle * self.fuel_consumption / t
			if self.fuel < 0:
				self.fuel = 0

	def estimated_distance(self, log=False):
		""" Returns the estimated of distance of how far the rocket would go,
			if it would go almost full throttle at this moment
		"""
		
		x0 = GRAVITY - self.thrust*.95 / (self.total_mass - self.fuel_consumption * 0.0)
		x1 = GRAVITY - self.thrust*.95 / (self.total_mass - self.fuel_consumption * 1.0)

		# Derivative at x=0 and x=1
		u = x0
		v = x1
		# Initial height at x=0
		y = abs(self.velocity)

		if log:
			print(f'u: {u}, v: {v}, y: {y}\nEstimated distance: {get_positive_area(u, v, y)}\n')
		
		return get_positive_area(u, v, y)