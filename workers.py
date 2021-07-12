from typing import List
import numpy as np
from queue import Queue


class Acceptor:
    def __init__(self, mean_service_time: float, operators: List):
        self.mean_service_time = mean_service_time
        self.operators = operators
        self.service_times = []
        self.queue = Queue("Acc")

    def make_queue(self, customer_iterator):
        for customer in customer_iterator:
            self.queue.insert(customer, customer.start_time)

    def process_queue(self):
        time = 0
        while self.queue.has_next():
            customer = self.queue.pop(time)
            time = max(time, customer.queue_arrival_time[self.queue.name])
            time = self.assign(customer, time)

    def assign(self, customer, time):
        if customer.is_tired(time):
            customer.tired = True
            return time
        service_time = self._generate_service_time()
        self.service_times.append(service_time)
        customer.start_paziresh_time = time
        customer.paziresh_time = time + service_time
        self.operators[customer.service_type].add_customer(customer, time + service_time)
        return service_time + time

    def _generate_service_time(self):
        return int(np.random.exponential(scale=self.mean_service_time))  # TODO: check this distribution


class Operator:

    def __init__(self, operator_name, workers):
        self.queue = Queue(operator_name)
        self.workers = workers

    def add_customer(self, customer, time):
        self.queue.insert(customer, time)

    def process_queue(self):
        time = 0
        while self.queue.has_next():
            customer = self.queue.pop(time)
            worker = self.find_free_worker()
            time = max(worker.end_of_last_work, customer.paziresh_time)
            if customer.is_tired(time):
                customer.tired = True
                continue
            worker.work(customer, time)

    def find_free_worker(self):
        min_free_workers = []
        min_free_time = min(self.workers, key=lambda w: w.end_of_last_work).end_of_last_work
        for worker in self.workers:
            if worker.end_of_last_work == min_free_time:
                min_free_workers.append(worker)
        return min_free_workers[int(np.floor(np.random.uniform(low=0, high=len(min_free_workers))))]


class Worker:

    def __init__(self, mean_service_time):
        self.mean_service_time = mean_service_time
        self.end_of_last_work = 0
        self.done_works = []

    def _generate_service_time(self):
        return int(np.random.exponential(scale=self.mean_service_time))  # TODO: check this distribution

    def is_working(self, time):
        return self.end_of_last_work <= time

    def work(self, customer, time):
        end_time = self._generate_service_time() + time
        if end_time > customer.tired_time:
            customer.tired = True
            end_time = customer.tired_time
        else:
            customer.service_time = end_time
        self.end_of_last_work = end_time
        return end_time
