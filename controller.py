from pid import PID
from rocket import Rocket


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
                fuel_consumption=10,
                thrust = 9000
            )
        
        # Initialize and prepare PID controller
        if pid is not None:
            self.pid = pid
        else:
            self.pid = PID(a=0.4, b=0.001, c=-2)
            self.pid.prepare(current=0, target=target_altitude)

    def update(self, t=1):
        """ Steer rocket for t number of time steps """
        
        # Update the physical properties of the rocket
        self.rocket.update()

        # Update PID using current error & velocity
		error = self.target_altitude - self.altitude
		derivative = self.velocity
		self.pid.update(error, derivative=derivative, t=t)

        # Follow protocol based on current state
		if self.state == 'landing-0':
			if self.estimated_distance() > self.rocket.altitude:
				self.rocket.throttle = .95
				self.state = 'landing-1'
			else:
				self.rocket.throttle = 0

		if self.state == 'landing-1':
			if self.rocket.velocity < 0:
				if abs(self.estimated_distance() - self.rocket.altitude) < 0.1:
					self.rocket.throttle = .95

				elif self.rocket.altitude - self.estimated_distance() > 0.1:
					self.rocket.throttle = 0.9

				elif self.rocket.altitude - self.estimated_distance() < -0.1:
					self.rocket.throttle = 1

			else:
				self.rocket.throttle = 7 / (self.rocket.thrust / self.rocket.total_mass)
				self.state = 'landed'

		elif self.state == 'hover':
			desired_acceleration = self.pid.output()
			self.rocket.throttle = desired_acceleration / (self.rocket.thrust / self.rocket.total_mass)

		self.rocket.throttle = min(max(0, self.rocket.throttle), 1)


def example():
    """ An example test with a rocket launching, hovering, & landing """
    
	data = {}

    # Put together parts
    controller = Controller()

	for key in r.data_keys:
		data[key] = []

	simulation_duration_s = 240
	simulation_timesteps = 50
	data_frequency_ps = 50

	for i in range(0, simulation_duration_s * simulation_timesteps, 1):
		for k, v in r.update(time_steps=simulation_timesteps).items():
			if i % data_frequency_ps == 0:
				data[k].append(v)

		if r.altitude <= 0:
			break

	return data