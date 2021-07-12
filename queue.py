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

    def _pop(self, time):
        for queue in self.queues[::-1]:
            if queue and queue[-1].queue_arrival_time[self.name] <= time:
                return queue.pop()
        # We should find earliest customer because we don't have any customer in given time
        customers = []
        for queue in self.queues[::-1]:
            if queue:
                customers.append(queue)
        # print(list(q[-1] for q in customers))
        return min(customers, key=lambda q: q[-1].queue_arrival_time[self.name]).pop()

    def _has_next(self):
        return any(map(lambda queue: queue and len(queue) > 0, self.queues))

    def pop(self, time):
        while self._has_next():
            customer = self._pop(time)
            departure_time = max(time, customer.queue_arrival_time[self.name])
            if customer.is_tired(departure_time):
                customer.tired = True
                customer.queue_departure_time[self.name] = customer.tired_time
                self.departure_times.append(customer.tired_time)
                continue
            customer.queue_departure_time[self.name] = departure_time
            self.departure_times.append(departure_time)
            return customer
        return None
