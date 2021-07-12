import random

import numpy as np


class Customer:
    star_probability = {
        0: 0.5,
        1: 0.2,
        2: 0.15,
        3: 0.1,
        4: 0.05,
    }

    @staticmethod
    def get_tiredness_time(tiredness_rate):
        return int(np.random.exponential(scale=1/tiredness_rate))

    @staticmethod
    def _create_star():
        p = random.uniform(0, 1)
        for key, value in Customer.star_probability.items():
            p -= value
            if p < 0:
                return key

    def __init__(self, service_type, start_time, tiredness_rate):
        self.star = Customer._create_star()
        self.service_type = service_type
        self.start_time = start_time
        self.tired_time = start_time + Customer.get_tiredness_time(tiredness_rate)
        self.tired = False
        self.start_paziresh_time = None
        self.paziresh_time = None
        self.service_time = None
        self.queue_arrival_time = dict()
        self.queue_departure_time = dict()

    def is_tired(self, time):
        return time > self.tired_time

    def get_system_time(self):
        return self.service_time or self.tired_time

    def get_operator_arrival_time(self):
        matching = [s for s in self.queue_arrival_time.keys() if "Op" in s]
        if matching:
            return self.queue_arrival_time[matching[0]]
        return None

    def get_operator_departure_time(self):
        matching = [s for s in self.queue_departure_time.keys() if "Op" in s]
        if matching:
            return self.queue_departure_time[matching[0]]
        return None

    def get_total_service_time(self):
        system_time = self.get_system_time() - self.start_time
        return system_time - self.get_total_wait_time()

    def get_total_wait_time(self):
        wait_time = 0
        for queue_name in self.queue_arrival_time.keys():
            wait_time += self.queue_departure_time[queue_name] - self.queue_arrival_time[queue_name]
        return wait_time

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
