from pid import PID
from rocket import Rocket, GRAVITY


class Controller:
	def __init__(self, state='hover', rocket=None, pid=None):
		self.state = state

		# Build a rocket!
		if rocket is not None:
			self.r = rocket
		else:
			self.r = Rocket(
				parent = self,
				dry_mass = 100,
				fuel = 800,
				altitude=1,
				velocity=0,
				fuel_consumption=10,
				thrust = 9000
			)
		
		# Initialize and prepare PID controller
		if pid is not None:
			self.pid = pid
		else:
			self.pid = PID(k_p=0.5, k_i=0.005, k_d=1)

	def set_target(self, target_altitude):
		self.pid.i = 0

		if target_altitude > 0:
			self.state = 'hover'
		else:
			self.state = 'landing-0'

		print(f'PID prepared for {target_altitude}, {self.state}')

	def get_data_channels(self):
		data = self.r.dict()

		return data

	def update(self, target_altitude, t=1):
		""" Steer rocket for t number of time steps """

		self.r.pid_p, self.r.pid_i, self.r.pid_d = self.pid.get_pid()
		
		# Update the physical properties of the rocket
		self.r.update(t)

		# Follow protocol based on current state
		
		# Landing 0 puts the rocket in free fall
		# until continuing to do so would allow it to crash

		# Landing 1 deals with the actual landing of the rocket

		if self.state == 'landing-0':
			# If rocket is predicted to crash, engage thrusters
			if self.r.estimated_distance() > self.r.altitude:
				# Landing burn start
				self.r.throttle = .95
				self.state = 'landing-1'
			else:
				self.r.throttle = 0

		if self.state == 'landing-1':
			if self.r.velocity < 0:
				if abs(self.r.estimated_distance() - self.r.altitude) < 0.1:
					self.r.throttle = .95

				elif self.r.altitude - self.r.estimated_distance() > 0.1:
					self.r.throttle = 0.9

				elif self.r.altitude - self.r.estimated_distance() < -0.1:
					self.r.throttle = 1

			else:
				self.r.throttle = 7 / (self.r.thrust / self.r.total_mass)
				self.state = 'landed'
				# Landing burn shutdown, landing

		elif self.state == 'hover':
			self.r.desired_acceleration = self.pid(target_altitude - self.r.altitude, t=t)
			self.r.desired_throttle = self.r.desired_acceleration / (self.r.thrust / self.r.total_mass)

		self.r.throttle = min(max(0, self.r.desired_throttle), 1)

		# Return rocket data for logging
		return self.r.dict()