import numpy as np
import math
from functions import *
from rich import print
import pid

class Rocket():
	def __init__(self, dry_mass, alt, fuel, thrust, fuel_consumption, vel, state,
				 target_alt, time_steps, gravity=9.8):
		self.dry_mass = dry_mass
		self.alt = alt
		self.fuel = fuel
		self.thrust = thrust
		self.vel = vel
		self.acc = 0
		self.throttle = 0
		self.fuel_consumption = 10
		self.state = state
		self.p_state = state
		self.state_n = 0
		self.target_alt = target_alt
		self.pid = pid.PID(0.25, 0.0005, 1.8)
		self.pid(self.target_alt-self.alt, time_steps)
		self.time_steps = time_steps
		self.g = gravity
		self.time = 0

		self.k = 0
		self.estimated_touchdown = 0

		self.data_keys = [
			'alt', 'fuel', 'vel', 'acc', 'throttle', 'ed', 't/w', 'state_n', 'state', 'k',
			'desired_throttle', 'pid_p', 'pid_i', 'pid_d', 'desired_acceleration', 'ΔV', 'estimated touchdown'
		]

	def update(self, time_steps=1):
		self.time += 1/time_steps
		self._physics(time_steps)

		self._guidance(time_steps)

		if self.state != self.p_state:
			self.state_n += 1
			self.p_state = self.state

		return {
			'alt': self.alt,
			'vel': self.vel,
			'acc': self.acc,
			'throttle': self.throttle,
			'fuel': self.fuel,
			'ed': self.estimated_distance(),
			'desired_throttle': self.desired_throttle,
			'desired_acceleration': self.desired_acc,
			'pid_p': self.pid.p,
			'pid_i': self.pid.i,
			'pid_d': self.pid.d,
			't/w': self.thrust/(self.dry_mass + self.fuel)/self.g,
			'state_n': self.state_n,
			'state': self.state,
			'ΔV': self.ΔV,
			'k': self.k,
			'estimated touchdown': self.estimated_touchdown
		}

	def _physics(self, time_steps):
		if self.alt <= 0:
			self.alt = 0
			self.vel = 0
			self.acc = 0
			return True

		self.throttle = self.throttle * min(self.fuel/self.fuel_consumption, 1)

		self.acc = self.throttle * self.thrust / (self.dry_mass + self.fuel) - self.g

		self.vel += self.acc / time_steps
		self.alt += self.vel / time_steps

		if self.fuel * time_steps >= self.throttle:
			self.fuel -= self.throttle * self.fuel_consumption / time_steps
			if self.fuel < 0:
				self.fuel = 0

	def _guidance(self, time_steps):
		self.desired_acc = self.pid(self.target_alt-self.alt, time_steps)+self.g

		should_fire = self.should_fire()

		if self.state == 'landing-0':
			if self.estimated_distance() >= self.alt:
				self.desired_throttle = .95
				self.state = 'landing-1'
			else:
				self.desired_throttle = 0

		if self.state == 'landing-1':
			if self.vel < 0:
				if abs(self.estimated_distance() - self.alt) < 0.1:
					self.desired_throttle = .95
					# self.state = 'landing-1'
				elif self.alt - self.estimated_distance() > 0.1:
					self.desired_throttle = 0.9
				elif self.alt - self.estimated_distance() < -0.1:
					self.desired_throttle = 1
			else:
				self.desired_throttle = 0
				self.state = 'landed'

		elif self.state == 'hover':
			self.desired_throttle = self.desired_acc / (self.thrust / (self.dry_mass + self.fuel))

		self.throttle = min(max(0, self.desired_throttle), 1)

	@property
	def ΔV(self):
		self.exhaust_velocity = self.thrust/self.fuel_consumption

		return self.exhaust_velocity*math.log((self.dry_mass + self.fuel)/self.dry_mass)

	def estimated_distance(self):
		x0 = self.g - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 0.0)
		x1 = self.g - self.thrust*.95 / (self.dry_mass + self.fuel - self.fuel_consumption * 1.0)

		# Derivative at x=0 and x=1
		u = x0
		v = x1
		# Initial height at x=0
		y = abs(self.vel)

		return get_positive_area(u, v, y)

	def should_fire(self):
		a = -self.g
		b = self.vel
		c = self.alt
		t = self.thrust * 0.95 / (self.dry_mass + self.fuel)

		k, x = ignition_time(a, b, c, t)
		self.k = k
		self.estimated_touchdown = x

		# Logging:
		if int(self.time*100)%100 == 0:
			print(f'Time: {int(self.time)}\n a: {a} b: {b} c: {c} t: {t}\n k: {k} x: {x}')

		return k <= 1



def run():
	simulation_duration_s = 120
	simulation_timesteps = 50
	data_frequency_p = 10

	data = {}
	r = Rocket(dry_mass=100,
			   alt=1,
			   fuel=450,
			   thrust=6500,
			   fuel_consumption=10,
			   vel=0,
			   state='hover',
			   target_alt=500,
			   time_steps=simulation_timesteps)

	for key in r.data_keys:
		data[key] = []


	for i in range(0, simulation_duration_s*simulation_timesteps):
		for k, v in r.update(time_steps=simulation_timesteps).items():
			if i % data_frequency_p == 0:
				data[k].append(v)

		if i == simulation_duration_s*simulation_timesteps/2:
			r.state = 'landing-0'
			r.target_alt = 0
		
		if i > data_frequency_p*20:
			if data['alt'][-10] <= 0:
				break

	return data
