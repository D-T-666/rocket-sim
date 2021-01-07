from controller import Controller


FAILSAFE_DURATION = 1000


class Simulation:
	def __init__(self, controller, targets, timesteps=1):
		""" Run a simulation on a Controller object
		
		targets is a list of tuples each containing length & altitude
		"""
		
		self.controller = controller
		self.targets = [None, *targets]
		self.timesteps = timesteps

	def __iter__(self):
		self.next_target()
		
		i = 1
		while True:
			target, length = self.targets[0]

			distance = abs(self.controller.rocket.altitude - target)
			if i > length and distance <= 50:
				self.next_target()
				print(f'Target of {target} is met.')

			if self.targets and i >= FAILSAFE_DURATION:
				break
				raise RuntimeError('Simulation failed to meet all targets')

			if not self.targets:
				break

			yield self.controller.update(target, t=self.timesteps)

			i += 1

	def next_target(self):
		self.targets.pop(0)

		if self.targets:
			target, length = self.targets[0]
			self.controller.set_target(target)

	


def example():
	""" An example test with a rocket launching, hovering, & landing """
	
	controller = Controller()

	# targets = [2000, 1500, 2500, 0]
	targets = [
		(2000, 100),
		(3000, 100),
		(0, 100),
		(2000, 100)
	]
	timesteps = 50
	frequency = 1

	simulation = Simulation(
		controller,
		targets,
		timesteps
	)

	try:
		for i, data in enumerate(simulation):
			if i % frequency == 0:
				yield data

	except RuntimeError as e:
		print(f'Simulation interupted:\n{e}')