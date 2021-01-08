class PID:
	def __init__(self, k_p, k_i, k_d):
		self.p = 0
		self.i = 0
		self.d = 0

		self.k_p = k_p
		self.k_i = k_i
		self.k_d = k_d

		self.p_err = None

	def __call__(self, err, t=1):
		if self.p_err is not None:
			self.p = self.k_p * err  # Proportional
			self.i += self.k_i * err / t # Integral
			self.d = self.k_d * (err - self.p_err) * t # Derivative

		self.p_err = err

		return self.p + self.i + self.d

	def get_pid(self):
		return self.p, self.i, self.d
