from collections import deque

import numpy as np
import random


class Server:

    def __init__(self, averages, type_count):
        self.availability = [0] * len(averages)
        self.services = list(list() for _ in range(len(self.availability)))
        self.averages = averages
        self.queues = list(deque() for _ in range(type_count))
        self.clients = [None] * len(self.availability)

    def get_first_available(self):
        return min(self.availability)

    def get_service_time(self, index):
        return np.random.exponential(scale=self.averages[index])

    def reserve(self, time):
        if all((avail > time) for avail in self.availability):
            raise Exception("invalid reserve")
        available_indices = list(item[0] for item in filter(lambda item: item[1] <= time, enumerate(self.availability)))
        selected_index = random.choice(available_indices)
        service_time = self.get_service_time(selected_index)
        self.availability[selected_index] = (time + service_time)
        self.services[selected_index].append(service_time)



