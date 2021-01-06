from controller import Controller


class Simulation:
    def __init__(self, controller, targets, keys=None):
        """ Run a simulation on a Controller object """
        
        self.controller = controller
        self.targets = targets

        # Keys to log
        self.keys = keys
        self.data = {}

    def __iter__(self):
        for i in range(0, duration * timesteps, 1):
            self.controller.update()


def example():
    """ An example test with a rocket launching, hovering, & landing """
    
    controller = Controller()

    r = Rocket(
        dry_mass=100,
        altitude=1,
        fuel=800,
        thrust=9000,
        fuel_consumption=10,
        velocity=0,
        state='hover',
        target_altitude=2000
    )

    # targets = [2000, 1500, 2500, 0]
    targets = [2000, 0]
    timesteps = 50
    frequency = 50

    yield from Simulation(controller, targets, timesteps)[::frequency]