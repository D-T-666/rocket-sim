
import os
import sys
import time

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import engine
from functions import *

def main():
	results = engine.run()
	zero_line = [0 for a in results["alt"]]
	
	# plt.style.use('dark_background')
	# plt.style.use('fivethirtyeight')
	plt.style.use('Solarize_Light2')
	# plt.style.use('seaborn-poster')

	fig = plt.figure(figsize=(18, 14))
	axs = [0] * 13
	axs[0] = fig.add_subplot(3, 2, 1)
	axs[1] = fig.add_subplot(3, 4, 5)
	axs[2] = fig.add_subplot(6, 4, 19)
	axs[3] = fig.add_subplot(6, 4, 23)
	axs[4] = fig.add_subplot(3, 2, 5)
	axs[5] = fig.add_subplot(6, 4, 10)
	axs[6] = fig.add_subplot(6, 4, 11)
	axs[7] = fig.add_subplot(6, 4, 12)
	axs[8] = fig.add_subplot(6, 4, 15)
	axs[9] = fig.add_subplot(6, 4, 16)
	axs[10] = fig.add_subplot(3, 2, 2)
	axs[11] = fig.add_subplot(6, 4, 14)
	axs[12] = fig.add_subplot(3, 4, 12)

	axs[0].plot(results["alt"])
	axs[0].plot([a-e if s[:7] == "landing" else a for a,e,s in zip(results["alt"], results["ed"], results["state"])], '--', alpha=0.3)
	for ax in axs:
		for i in range(len(set(results["state_n"]))-1):
			ax.axvspan(results["state_n"].index(i), results["state_n"].index(i+1), color=['c', 'r', 'g', 'y'][i], alpha=0.1, lw=0)
	axs[0].set_title('altitude')

	axs[1].plot(results["vel"])
	axs[1].set_title('velocity')

	axs[2].plot(results["fuel"])
	axs[2].set_ylim([-10,np.max(results["fuel"])+10])
	axs[2].set_title('fuel')

	axs[3].plot(results["ed"])
	# axs[3].plot(results["k"])
	# axs[3].plot(results["estimated touchdown"])
	axs[3].set_title('estimated distance')

	axs[4].plot(results["acc"])
	axs[4].plot([0 for a in results["alt"]], alpha=0.5)
	axs[4].set_title('acceleration')

	axs[5].plot(results["throttle"])
	axs[5].plot(results["desired_throttle"], '--', color='y', alpha=1, linewidth=2)
	axs[5].set_ylim([-0.1,1.1])
	axs[5].set_title('throttle')

	axs[11].plot(results["throttle"])
	axs[11].set_ylim([-0.1,1.1])
	axs[11].set_xlim([results["state"].index('landing-1')-5, results["state"].index('landed')+5])
	axs[11].set_title('throttle - powered descent')

	axs[6].plot(results["pid_p"])
	axs[6].set_title('pid_p')

	axs[7].plot(results["pid_i"])
	axs[7].set_title('pid_i')

	axs[8].plot(results["pid_d"])
	axs[8].set_title('pid_d')

	axs[9].plot(results["desired_acceleration"], '--')
	axs[9].plot(results["pid_p"], alpha=0.4)
	axs[9].plot(results["pid_i"], alpha=0.4)
	axs[9].plot(results["pid_d"], alpha=0.4)
	axs[9].set_title('pid all')

	axs[10].plot(results["t/w"])
	axs[10].set_title('thrust / weight')

	axs[12].plot(results['ΔV'])
	axs[12].set_title('ΔV left')

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
