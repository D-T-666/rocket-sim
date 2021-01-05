import matplotlib.pyplot as plt
import numpy as np
import engine
from functions import *


def main():
    results = engine.run()

    plt.style.use('dark_background')
    fig, axs = plt.subplots(2, 3, constrained_layout=True)

    axs[0][0].plot(results["alt"])
    axs[0][0].plot([a-e for a,e in zip(results["alt"], results["ed1"])], '--', alpha=0.3)
    # axs[0][0].plot([a-e for a,e in zip(results["alt"], results["ed2"])], '--', alpha=0.3)
    axs[0][0].plot([0 for a in results["alt"]], '-.')
    axs[0][0].set_title('altitude')

    axs[0][1].plot(results["vel"])
    axs[0][1].plot([0 for a in results["alt"]], '-.')
    axs[0][1].set_title('velocity')

    axs[0][2].plot(results["fuel"])
    axs[0][2].set_title('fuel')

    axs[1][0].plot(results["throttle"])
    axs[1][0].set_title('throttle')

    axs[1][1].plot(results["acc"])
    axs[1][1].plot([0 for a in results["alt"]], alpha=0.5)
    axs[1][1].set_title('acceleration')

    axs[1][2].plot(results["ed1"])
    # axs[1][2].plot(results["ed2"])
    axs[1][2].set_title('estimated distance')

    plt.show(block=True)

main()

# def plot():
#     plt.style.use('dark_background')
#     fig, axs = plt.subplots(2, 2, constrained_layout=True)

# 	axs[0][0] = 0
	
#     plt.show(block=True)

# plot()