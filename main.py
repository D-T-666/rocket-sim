
import os
import sys
import time

import controller
import simulation

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

from functions import *

def main():
	# Get keys of Rocket through a Dummy Controller object
	keys = controller.Controller().rocket.dict().keys()
	results = {key: [] for key in keys}
	
	# Start & collect data from example simulation
	for data in simulation.example():
		for key, value in data.items():
			results[key].append(value)


	plt.style.use('dark_background')
	fig = plt.figure(figsize=(32, 28))
	axs = [0] * 10
	axs[0] = fig.add_subplot(3, 2, 1)
	axs[1] = fig.add_subplot(3, 4, 5)
	axs[2] = fig.add_subplot(6, 4, 18)
	axs[3] = fig.add_subplot(6, 4, 22)
	axs[4] = fig.add_subplot(3, 4, 9)
	axs[5] = fig.add_subplot(3, 4, 6)
	axs[6] = fig.add_subplot(6, 4, 11)
	axs[7] = fig.add_subplot(6, 4, 12)
	axs[8] = fig.add_subplot(6, 4, 15)
	axs[9] = fig.add_subplot(3, 2, 2)

	axs[0].plot(results["altitude"])
	axs[0].plot([a-e for a,e in zip(results["altitude"], results["estimated_distance"])], '--', alpha=0.3)
	axs[0].plot([0 for a in results["altitude"]], '-.')
	axs[0].set_title('altitude')

	axs[1].plot(results["velocity"])
	axs[1].plot([0 for a in results["altitude"]], '-.')
	axs[1].set_title('velocity')

	axs[2].plot(results["fuel"])
	axs[2].set_title('fuel')

	axs[3].plot(results["estimated_distance"])
	axs[3].set_title('estimated_distance')

	axs[4].plot(results["acceleration"])
	axs[4].plot([0 for a in results["altitude"]], alpha=0.5)
	axs[4].set_title('acceleration')

	axs[5].plot(results["throttle"])
	axs[5].plot(results["desired_throttle"], '--', alpha=0.5)
	axs[5].set_title('throttle')


	axs[6].plot(results["pid_p"])
	axs[6].set_title('pid_p')

	axs[7].plot(results["pid_i"])
	axs[7].set_title('pid_i')

	axs[8].plot(results["pid_d"])
	axs[8].set_title('pid_d')

	axs[9].plot(results["pid_p"])
	axs[9].plot(results["pid_i"])
	axs[9].plot(results["pid_d"])
	axs[9].set_title('pid all')


	fig.tight_layout()

	# Save figure to plots folder
	local_directory = os.path.dirname(sys.argv[0])
	plots_directory = os.path.join(local_directory, 'plots')
	# file_name = f'fig-{int(time.time())}.svg'
	file_name = f'fig-refreshing.png'
	file_path = os.path.join(plots_directory, file_name)

	if not os.path.exists(plots_directory):
		os.makedirs(plots_directory)

	plt.savefig(file_path)


if __name__ == '__main__':
	main()
