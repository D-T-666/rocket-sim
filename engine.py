import math

import numpy as np
from rich import print

from functions import *
from pid import PIDController


class Rocket():
	def __init__(self, dry_mass, altitude, fuel, thrust, fuel_consumption, velocity, state, target_altitude):
		# Massive properties
		self.dry_mass = dry_mass
		self.fuel = fuel

		# Location & Motion
		self.altitude = altitude
		self.velocity = velocity

		# Operational & Engine
		self.state = state
		self.target_altitude = target_altitude
		
		self.fuel_consumption = fuel_consumption
		self.thrust = thrust
		self.throttle = 0


		# Initialize and prepare PID controller
		self.pid = PIDController(a=0.4, b=0.001, c=-2)
		self.pid.prepare(current=0, target=target_altitude)

		# Which values to collect during execution
		self.data_keys = ['dry_mass', 'altitude', 'fuel', 'thrust', 'velocity', 'acceleration', 'throttle', 'ed']

	def update(self, time_steps=1):
		self._physics(time_steps)

		self._guidance(time_steps)

		return {
			'altitude': self.altitude,
			'velocity': self.velocity,
			'acceleration': self.acceleration,
			'throttle': self.throttle,
			'fuel': self.fuel,
			'ed': self.estimated_distance(False)
		}

	def _physics(self, time_steps):
		if self.altitude <= 0:
			return True

		self.acceleration = self.thrust * (self.throttle
								   if self.fuel >= 1 else self.throttle *
								   self.fuel) / (self.dry_mass + self.fuel) - 9.8

		self.velocity += self.acceleration / time_steps
		self.altitude += self.velocity / time_steps

		if self.fuel * time_steps >= self.throttle:
			self.fuel -= self.throttle * self.fuel_consumption / time_steps
			if self.fuel < 0:
				self.fuel = 0

	def _guidance(self, t=1):
		# Update PID using current error & velocity
		error = self.target_altitude - self.altitude
		derivative = self.velocity
		self.pid.update(error, derivative=derivative, t=t)

		if self.state == 'landing-0':
			if self.estimated_distance() > self.altitude:
				self.throttle = .95
				self.state = 'landing-1'
			else:
				self.throttle = 0

		if self.state == 'landing-1':
			if self.velocity < 0:
				if abs(self.estimated_distance() - self.altitude) < 0.1:
					self.throttle = .95
					# self.state = 'landing-1'
				elif self.altitude - self.estimated_distance() > 0.1:
					self.throttle = 0.9
				elif self.altitude - self.estimated_distance() < -0.1:
					self.throttle = 1
			else:
				self.throttle = 7 / (self.thrust / (self.dry_mass + self.fuel))
				self.state = 'landed'

		elif self.state == 'hover':
			desired_acc = self.pid.output()
			self.throttle = desired_acc / (self.thrust / (self.dry_mass + self.fuel))

		self.throttle = min(max(0, self.throttle), 1)

	def estimated_distance(self, log=True):
		x0 = 9.8 - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 0.0)
		x1 = 9.8 - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 1.0)

		# Derivative at x=0 and x=1
		u = x0
		v = x1
		# Initial height at x=0
		y = abs(self.velocity)

		if log:
			print(f'u: {u}, v: {v}, y: {y}\nEstimated distance: {get_positive_area(u, v, y)}\n')
		
		return get_positive_area(u, v, y)


def run():
	data = {}
	r = Rocket(dry_mass=100,
			   altitude=1,
			   fuel=800,
			   thrust=9000,
			   fuel_consumption=10,
			   velocity=0,
			   state='hover',
			   target_altitude=2000)

	for key in r.data_keys:
		data[key] = []

	simulation_duration_s = 240
	simulation_timesteps = 50
	data_frequency_ps = 50

	for i in range(0, simulation_duration_s*simulation_timesteps, 1):
		# if r.state[:7] == 'landing':
		# 	print(f'step: {i/data_frequency_ps} \nstate: {r.state}')

		for k, v in r.update(time_steps=simulation_timesteps).items():
			if i % data_frequency_ps == 0:
				data[k].append(v)

		# if i == simulation_duration_s*simulation_timesteps/2:
		# 	r.state = 'landing-0'

		if r.altitude <= 0:
			break

	return data
