from collections import deque

from customer import Customer


def log_pop(pop_function):
    def pop_with_log(self, time):
        customer = pop_function(self, time)
        departure_time = max(time, customer.queue_arrival_time[self.name])
        customer.queue_departure_time[self.name] = departure_time
        self.departure_times.append(departure_time)
        return customer

    return pop_with_log


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

    @log_pop
    def pop(self, time):
        for queue in self.queues[::-1]:
            if queue and queue[0].queue_arrival_time[self.name] <= time:
                return queue.pop()
        # We should find earliest customer because we don't have any customer in given time
        customers = []
        for queue in self.queues[::-1]:
            if queue:
                customers.append(queue)
        return min(customers, key=lambda q: q[0].queue_arrival_time[self.name]).pop()

    def has_next(self):
        return any(map(lambda queue: queue and len(queue) > 0, self.queues))
