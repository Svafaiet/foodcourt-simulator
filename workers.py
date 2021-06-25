from typing import List

import numpy as np


class Acceptor:
    def __init__(self, mean_service_time: float, operators: List):
        self.mean_service_time = mean_service_time
        self.operators = operators
        self.service_times = []

    def assign(self, customer, time):
        if customer.is_tired(time):
            return time
        service_time = self._generate_service_time()
        self.service_times.append(service_time)
        customer.paziresh_time = time + service_time
        self.operators[customer.service_type].add_customer(customer)
        return service_time + time

    def _generate_service_time(self):
        return np.random.exponential(scale=self.mean_service_time) # TODO: check this distribution


class Operator:

    def __init__(self, workers):
        self.queue = [] # TODO: use heap
        self.workers = workers

    def add_customer(self, customer):
        self.queue.append(customer)

    def process_queue(self):
        # TODO: process queue and remove tired customers
        pass


class Worker:

    def __init__(self, mean_service_time):
        self.mean_service_time = mean_service_time
        self.is_working = False
        self.end_of_last_work = -1
        self.done_works = []

    def _generate_service_time(self):
        return np.random.exponential(scale=self.mean_service_time)  # TODO: check this distribution

    def is_working(self, time):
        return self.end_of_last_work <= time

    def work(self, customer, time):
        service_time = self._generate_service_time()
        self.end_of_last_work = service_time + time
        customer.service_time = service_time + time
