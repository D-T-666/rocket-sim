import numpy as np
import math
from functions import *
from rich import print
import pid

class Rocket():
	def __init__(self, dry_mass, alt, fuel, thrust, fuel_consumption, vel, state,
				 target_alt):
		self.dry_mass = dry_mass
		self.alt = alt
		self.fuel = fuel
		self.thrust = thrust
		self.vel = vel
		self.acc = 0
		self.throttle = 0
		self.fuel_consumption = 10
		self.state = state
		self.target_alt = target_alt
		self.pid = pid.PID()

		self.data_keys = [
			'dry_mass', 'alt', 'fuel', 'thrust', 'vel', 'acc', 'throttle', 'ed'
		]

	def update(self, time_steps=1):
		self._physics(time_steps)

		self._guidance(time_steps)

		return {
			'alt': self.alt,
			'vel': self.vel,
			'acc': self.acc,
			'throttle': self.throttle,
			'fuel': self.fuel,
			'ed': self.estimated_distance(False)
		}

	def _physics(self, time_steps):
		if self.alt <= 0:
			return True

		self.acc = self.thrust * (self.throttle
								   if self.fuel >= 1 else self.throttle *
								   self.fuel) / (self.dry_mass + self.fuel) - 9.8

		self.vel += self.acc / time_steps
		self.alt += self.vel / time_steps

		if self.fuel * time_steps >= self.throttle:
			self.fuel -= self.throttle * self.fuel_consumption / time_steps
			if self.fuel < 0:
				self.fuel = 0

	def _guidance(self, time_steps):
		self.pid.update(self.target_alt, self.alt, self.vel, self.acc, time_steps)

		if self.state == 'landing-0':
			if self.estimated_distance() > self.alt:
				self.throttle = .95
				self.state = 'landing-1'
			else:
				self.throttle = 0

		if self.state == 'landing-1':
			if self.vel < 0:
				if abs(self.estimated_distance() - self.alt) < 0.1:
					self.throttle = .95
					# self.state = 'landing-1'
				elif self.alt - self.estimated_distance() > 0.1:
					self.throttle = 0.9
				elif self.alt - self.estimated_distance() < -0.1:
					self.throttle = 1
			else:
				self.throttle = 7 / (self.thrust / (self.dry_mass + self.fuel))
				self.state = 'landed'

		elif self.state == 'hover':
			desired_acc = self.pid.get_value()
			self.throttle = desired_acc / (self.thrust / (self.dry_mass + self.fuel))

		self.throttle = min(max(0, self.throttle), 1)

	def estimated_distance(self, log=True):
		x0 = 9.8 - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 0.0)
		x1 = 9.8 - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 1.0)

		# Derivative at x=0 and x=1
		u = x0
		v = x1
		# Initial height at x=0
		y = abs(self.vel)

		if log:
			print(f'u: {u}, v: {v}, y: {y}\nEstimated distance: {get_positive_area(u, v, y)}\n')
		
		return get_positive_area(u, v, y)


def run():
	data = {}
	r = Rocket(dry_mass=100,
			   alt=1,
			   fuel=800,
			   thrust=9000,
			   fuel_consumption=10,
			   vel=0,
			   state='hover',
			   target_alt=2000)

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

		if r.alt <= 0:
			break

	return data
