# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import engine
from functions import *
import time

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

	axs[0].plot(results["alt"])
	axs[0].plot([a-e for a,e in zip(results["alt"], results["ed"])], '--', alpha=0.3)
	axs[0].plot([0 for a in results["alt"]], '-.')
	axs[0].set_title('altitude')

	axs[1].plot(results["vel"])
	axs[1].plot([0 for a in results["alt"]], '-.')
	axs[1].set_title('velocity')

	axs[2].plot(results["fuel"])
	axs[2].set_title('fuel')

	axs[3].plot(results["ed"])
	axs[3].set_title('estimated distance')

	axs[4].plot(results["acc"])
	axs[4].plot([0 for a in results["alt"]], alpha=0.5)
	axs[4].set_title('acceleration')

	axs[5].plot(results["throttle"])
	axs[5].set_title('throttle')

	fig.tight_layout()

	# plt.savefig('D:\\python\\rocket-sim\plots\\fig-'+str(int(time.time()))+'.svg')
	plt.show()

main()

# def plot():
#     plt.style.use('dark_background')
#     fig, axs = plt.subplots(2, 2, constrained_layout=True)

# 	axs[0][0] = 0
	
#     plt.show(block=True)

# plot()