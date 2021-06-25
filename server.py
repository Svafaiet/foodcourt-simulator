from collections import deque

import numpy as np
import random

from customer import Customer
from queue import Queue


class Server:

    def __init__(self, averages):
        self.availability = [0] * len(averages)
        self.services = list(list() for _ in range(len(self.availability)))
        self.averages = averages
        self.clients = [None] * len(self.availability)
        self.queue = Queue()

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

    def update(self, time=-1):
        # print("TIME", time)

        update_time = self.baje.get_first_available()
        while (time == -1 or update_time <= time) and self.q:
            customer_arrived = self.q.pop()
            update_time = max(customer_arrived, self.baje.get_first_available())
            wait_time = update_time - customer_arrived
            # print("HAHA:", time, wait_time, customer_arrived, self.baje.availability)
            if wait_time != 0:
                self.waits.append(wait_time)
            self.baje.reserve(update_time)
            # print("UPDATE", update_time)