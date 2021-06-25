from collections import deque

from customer import Customer


class Queue:
    def __init__(self):
        self.queues = list(deque() for _ in range(len(Customer.star_probability.keys())))

    def insert(self, customer: Customer):
        self.queues[customer.star].appendleft(customer)

    def pop(self):
        for queue in self.queues[::-1]:
            if queue:
                return queue.pop()

    def __iter__(self):
        for queue in self.queues:
            for item in queue:
                yield item

    def __bool__(self):
        return any(self.queues)


