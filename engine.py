import numpy as np
import math
from functions import *


class Rocket():
    def __init__(self, mass, alt, fuel, thrust, fuel_consumption, vel, state,
                 target_alt):
        self.mass = mass
        self.alt = alt
        self.fuel = fuel
        self.thrust = thrust
        self.vel = vel
        self.acc = 0
        self.throttle = 0
        self.fuel_consumption = 10
        self.state = state
        self.target_alt = target_alt
        self.pid = {'p': 0, 'i': 0, 'd': 0}
        self.a = 0
        self.b = 0
        self.c = 0

        self.data_keys = [
            'mass', 'alt', 'fuel', 'thrust', 'vel', 'acc', 'throttle', 'ed',
            'fire_alt', 'a', 'b', 'c'
        ]

    def update(self, time_steps=1):
        self._physics(time_steps)

        self._guidance(time_steps)

        return {
            'alt': self.alt,
            'vel': self.vel,
            'acc': -self.acc,
            'throttle': self.throttle,
            'fuel': self.fuel,
            'ed': self.estimated_distance(),
            'a': self.a, 
            'b': self.b,
            'c': self.c
        }

    def _physics(self, time_steps):
        if self.alt <= 0:
            return True

        self.acc = -self.thrust * (self.throttle
                                   if self.fuel >= 1 else self.throttle *
                                   self.fuel) / (self.mass + self.fuel) + 9.8

        self.vel -= self.acc / time_steps
        self.alt += self.vel / time_steps

        if self.fuel * time_steps >= self.throttle:
            self.fuel -= self.throttle * self.fuel_consumption / time_steps

    def _guidance(self, time_steps):
        self.pid['p'] = 0.6 * (self.target_alt - self.alt)
        self.pid['i'] += 0.05 * self.vel / time_steps
        self.pid['d'] = -2 * self.vel

        if self.state == 'landing':
            if self.estimated_distance() > self.alt+1:
                self.throttle = 1
                self.state = 'out of control'
            else:
                self.throttle = 0

        elif self.state == 'hover':
            self.throttle = (self.pid['p'] + self.pid['i'] + self.pid['d']) \
                            / (self.thrust / (self.mass + self.fuel))
            if self.throttle > 1:
                self.throttle = 1
            elif self.throttle < 0:
                self.throttle = 0 

            if abs(self.vel) < 0.01 and self.alt > 110:
                self.state = 'landing'

        elif self.state == 'launch':
            pass

    def estimated_distance(self):
        # mass = self.mass + self.fuel
        # net_acc = self.thrust / mass - 9.8
        # time_to_stop = self.vel / net_acc
        # time_to_stop = time_to_stop if time_to_stop < self.fuel else self.fuel
        # estimated_distance = self.vel * time_to_stop / 2 - self.vel / 2
        # return estimated_distance

        # ===

        # Derivative at x=0 and x=1
        u = -self.thrust / (self.mass + self.fuel) - 9.8
        v = -self.thrust / (self.mass + self.fuel - 1) - 9.8
        # Initial height at x=0
        y = self.thrust / (self.mass + self.fuel) - 9.8

        return get_positive_area(u, v, y)


def run():
    data = {}
    r = Rocket(mass=100,
               alt=1,
               fuel=250,
               thrust=4500,
               fuel_consumption=10,
               vel=0,
               state='hover',
               target_alt=120)

    for key in r.data_keys:
        data[key] = []

    for i in range(0, 300, 1):
        for k, v in r.update(time_steps=5).items():
            data[k].append(v)

    return data
