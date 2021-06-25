import numpy as np


class Customer:
    tiredness_rate = 1.0
    star_probability = {
        0: 0.5,
        1: 0.2,
        2: 0.15,
        3: 0.1,
        4: 0.05,
    }

    @staticmethod
    def get_tiredness_time():
        return np.random.exponential(scale=1/Customer.tiredness_rate)

    def __init__(self, star, service_type, start_time):
        self.star = star
        self.service_type = service_type
        self.start_time = start_time
        self.tired_time = start_time + Customer.get_tiredness_time()
        self.paziresh_time = None
        self.service_time = None
        self.abandon_time = None
        self.queue_arrival_time = dict()
        self.queue_departure_time = dict()

    def is_tired(self, time):
        return time > self.tired_time
