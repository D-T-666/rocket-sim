class PIDController:
	def __init__(self, a, b, c, initial_error=None):
		# (a, b, c) are the weights for (p, i, d)
		self.a = a
		self.b = b
		self.c = c

		# Proportional, Integral, & Derivative
		self.p = 0
		self.i = 0
		self.d = 0

		# Provided an initial error, self.prepare isn't necessary
		if initial_error is not None:
			self.last_error = initial_error

	def __call__(self, *args):
		self.update(*args)
		return self.output()
		
	def prepare(self, current, target):
		""" Run at start to give the controller an initial error
			from which to calculate the first derivative
		"""
		self.last_error = current - target

	def update(self, error, derivative=None, t=1):
		if derivative is None:
			# Calculate derivate using the current & previous errors
			try:
				derivative = error - self.last_error
			except AttributeError:
				raise RuntimeError(
					f'Controller must be initialized properly, with {type(self).__name__}.prepare')

		# Calculate the PID
		self.p = self.a * error
		self.i += self.b * error / t
		self.d = self.c * derivative

	def output(self):
		return self.p + self.i + self.d