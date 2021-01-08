from pid import PID
from rocket import Rocket, GRAVITY


class Controller:
	def __init__(self, state='hover', rocket=None, pid=None):
		self.state = state

		# Build a rocket!
		if rocket is not None:
			self.rocket = rocket
		else:
			self.rocket = Rocket(
				dry_mass = 100,
				fuel = 800,
				altitude=1,
				velocity=0,
				fuel_consumption=1,
				thrust = 9000
			)
		
		# Initialize and prepare PID controller
		if pid is not None:
			self.pid = pid
		else:
			self.pid = PID(P=0.6, I=0.001, D=-2.5)

	def set_target(self, target_altitude):
		if target_altitude > 0:
			self.state = 'hover'
		else:
			self.state = 'landing-0'

		print(f'PID prepared for {target_altitude}, {self.state}')

	def update(self, target_altitude, t=1):
		""" Steer rocket for t number of time steps """

		self.pid_p, self.pid_i, self.pid_d = self.pid.get_pid()
		
		# Update the physical properties of the rocket
		self.rocket.update()

		# Follow protocol based on current state
		if self.state == 'landing-0':
			if self.rocket.estimated_distance() > self.rocket.altitude:
				self.rocket.throttle = .95
				self.state = 'landing-1'
			else:
				self.rocket.throttle = 0

		if self.state == 'landing-1':
			if self.rocket.velocity < 0:
				if abs(self.rocket.estimated_distance() - self.rocket.altitude) < 0.1:
					self.rocket.throttle = .95

				elif self.rocket.altitude - self.rocket.estimated_distance() > 0.1:
					self.rocket.throttle = 0.9

				elif self.rocket.altitude - self.rocket.estimated_distance() < -0.1:
					self.rocket.throttle = 1

			else:
				self.rocket.throttle = 7 / (self.rocket.thrust / self.rocket.total_mass)
				self.state = 'landed'

		elif self.state == 'hover':
			self.desired_acceleration = self.pid(target_altitude - self.rocket.altitude, t=t)
			self.rocket.desired_throttle = self.desired_acceleration / (self.rocket.thrust / self.rocket.total_mass)

		self.rocket.throttle = min(max(0, self.rocket.desired_throttle), 1)

		# Return rocket data for logging
		return self.rocket.dict()