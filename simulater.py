import random

import numpy as np

from customer import Customer
from workers import Acceptor, Worker, Operator


class CustomerGenerator:
    def __init__(self, arrival_rate, tiredness_rate, service_count):
        self.arrival_rate = arrival_rate
        self.tiredness_rate = tiredness_rate
        self.service_count = service_count

    def generate(self, time):
        inter_arrival_time = np.random.exponential(scale=1 / self.arrival_rate)
        return Customer(service_type=random.randint(0, self.service_count - 1), start_time=time + inter_arrival_time)

    def generate_n(self, n, start_time=0):
        time = start_time
        for _ in range(n):
            customer = self.generate(time)
            time = customer.start_time
            yield customer


class Simulator:
    def __init__(self, arrival_rate, operator_service_rate, tiredness_rate, averages):
        self.operators = []
        for operator_averages in averages:
            workers = list(map(lambda avg: Worker(avg), operator_averages))
            self.operators.append(Operator(workers))
        self.acceptor = Acceptor(operator_service_rate, self.operators)
        self.customer_generator = CustomerGenerator(
            arrival_rate=arrival_rate,
            tiredness_rate=tiredness_rate,
            service_count=len(self.operators)
        )
