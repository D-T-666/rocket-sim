from controller import Controller


class Simulation:
	def __init__(self, controller, targets, timesteps=1, sensitivity=10, failsafe=None):
		""" Run a simulation on a Controller object
		
		targets is a list of tuples each containing duration & altitude
		"""
		
		self.controller = controller
		self.targets = [None, *targets]
		self.timesteps = timesteps
		self.sensitivity = sensitivity

		if failsafe:
			self.failsafe = failsafe
		else:
			# Calculate a reasonable failsafe limit
			total_duration = sum(duration for target, duration in targets)
			total_difference = sum([0] + [
				abs(targets[j][1] - targets[j - 1][1])
				for j in range(1, len(targets))
			])
			wiggle_room = 2000
			self.failsafe = total_duration + total_difference + wiggle_room

	def __iter__(self):
		self.next_target()
		
		i = 0
		target_timer = 0
		while True:
			target, duration = self.targets[0]

			# Count time when stable at target altitude
			distance = abs(self.controller.r.altitude - target)
			if distance <= self.sensitivity:
				target_timer += 1 / self.timesteps

				if target_timer >= duration:
					print(f'Target of {target} is met.')
					self.next_target()
			
			else:
				target_timer = 0

			# if self.targets and i >= self.failsafe:
			# 	break
			# 	raise RuntimeError('Simulation failed to meet all targets')

			if not self.targets:
				break

			if i > 600*self.timesteps:
				break

			yield self.controller.update(target, t=self.timesteps)

			i += 1

	def next_target(self):
		self.targets.pop(0)

		if self.targets:
			target, duration = self.targets[0]
			self.controller.set_target(target)

	


def example():
	""" An example test with a rocket launching, hovering, & landing """
	
	targets = [
		(200, 5),
		(0, 100),
	]
	timesteps = 50
	frequency = 50

	simulation = Simulation(
		controller = Controller(),
		targets = targets,
		timesteps = 50,
		sensitivity = 20
	)

	try:
		for i, data in enumerate(simulation):
			if i % frequency == 0:
				yield data

	except RuntimeError as e:
		print(f'Simulation interupted:\n{e}')