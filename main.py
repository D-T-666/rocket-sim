# import matplotlib
# matplotlib.use('Agg')
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

import engine
from functions import *


def main():
	results = engine.run()

	plt.style.use('dark_background')
	fig = plt.figure(figsize=(12, 16))
	axs = [0,0,0,0,0,0]
	axs[0] = fig.add_subplot(3, 1, 1)
	axs[1] = fig.add_subplot(3, 2, 3)
	axs[2] = fig.add_subplot(6, 2, 10)
	axs[3] = fig.add_subplot(6, 2, 12)
	axs[4] = fig.add_subplot(3, 2, 5)
	axs[5] = fig.add_subplot(3, 2, 4)

	axs[0].plot(results["altitude"])
	axs[0].plot([a-e for a,e in zip(results["altitude"], results["ed"])], '--', alpha=0.3)
	axs[0].plot([0 for a in results["altitude"]], '-.')
	axs[0].set_title('altitude')

	axs[1].plot(results["velocity"])
	axs[1].plot([0 for a in results["altitude"]], '-.')
	axs[1].set_title('velocity')

	axs[2].plot(results["fuel"])
	axs[2].set_title('fuel')

	axs[3].plot(results["ed"])
	axs[3].set_title('estimated distance')

	axs[4].plot(results["acceleration"])
	axs[4].plot([0 for a in results["altitude"]], alpha=0.5)
	axs[4].set_title('acceleration')

	axs[5].plot(results["throttle"])
	axs[5].set_title('throttle')

	fig.tight_layout()


	# Save figure to plots folder
	local_directory = os.path.dirname(sys.argv[0])
	plots_directory = os.path.join(local_directory, 'plots')
	file_name = f'fig-{int(time.time())}.svg'
	file_path = os.path.join(plots_directory, file_name)

	if not os.path.exists(plots_directory):
		os.makedirs(plots_directory)

	plt.savefig(file_path)


if __name__ == '__main__':
	main()