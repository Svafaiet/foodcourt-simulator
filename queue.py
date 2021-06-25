from collections import deque

from customer import Customer


class Queue:
    def __init__(self, name):
        self.name = name
        self.queues = list(deque() for _ in range(len(Customer.star_probability.keys())))
        self.insert_times = []
        self.departure_times = []

    def insert(self, customer: Customer, time):
        customer.queue_arrival_time[self.name] = time
        self.queues[customer.star].appendleft(customer)
        self.insert_times.append(time)

    def pop(self, time):
        for queue in self.queues[::-1]:
            if queue and queue[0].queue_arrival_time[self.name] <= time:
                return queue.pop()

    def has_next(self, time):
        return any((lambda queue: queue and queue[0].queue_arrival_time[self.name] <= time, self.queues))

    def log_pop(self, time, customer):
        customer.queue_arrival_time[self.name] = time
        self.departure_times.append(time)
