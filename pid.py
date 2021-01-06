class PID:
	def __init__(self):
		self.p = 0
		self.i = 0
		self.d = 0

	def update(self, target_alt, alt, vel, acc, time_steps):
		self.p = 0.4 * (target_alt - alt)
		self.i += 0.001 * (target_alt - alt) / time_steps
		self.d = -2 * vel
	
	def get_value(self):
		return self.p + self.i + self.d