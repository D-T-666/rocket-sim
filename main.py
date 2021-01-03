import matplotlib.pyplot as plt
import engine

def main():
    results = engine.run()


    fig = plt.figure()
    
    ax1 = fig.add_subplot(211)
    ax1.plot(results["alt"])

    ax2 = fig.add_subplot(223)
    ax2.plot(results["vel"])

    ax3 = fig.add_subplot(224)
    ax3.plot(results["acc"])

    plt.show(block=True)

main()