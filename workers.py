from typing import List

import numpy as np


class Acceptor:
    def __init__(self, mean_service_time: float, operators: List):
        self.mean_service_time = mean_service_time
        self.operators = operators

    def assign(self, customer):
        self.operators[customer.service_type].add_customer(customer)

    def _generate_service_time(self):
        return np.random.exponential(scale=self.mean_service_time) ## TODO: check this distribution


class Operator:

    def __init__(self, workers):
        self.queue = [] # TODO: use heap
        self.workers = workers

    def add_customer(self, customer):
        self.queue.append(customer)


class Worker:

    def __init__(self, mean_service_time):
        self.mean_service_time = mean_service_time
        # TODO: add other fields and functions