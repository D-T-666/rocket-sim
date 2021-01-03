import numpy as np

class Rocket():
    def __init__(self, mass, alt, fuel, thrust, vel, throttle):
        self.mass = mass
        self.alt = alt
        self.fuel = fuel
        self.thrust = thrust
        self.vel = vel
        self.throttle = throttle

        self.data_keys = ['mass', 'alt', 'fuel', 'thrust', 'vel', 'acc']

    def update(self, time_step=1):
        acc = (self.mass - self.thrust * self.throttle)
        self.vel -= acc/time_step
        self.alt += self.vel/time_step

        return { "alt": self.alt, "vel": self.vel, "acc": acc }


def run():
    data = {}
    r = Rocket(
        mass=100,
        alt=100,
        fuel=10,
        thrust=110,
        vel=0,
        throttle=0
    )

    for key in r.data_keys:
        data[key] = []

    for i in range(0, 100, 1):
        for k,v in r.update(time_step=20).items():
            data[k].append(v)

        if i > 50:
            r.throttle = 1

    return data
