import pandas as pd
import os
from simulater import Simulator


def read_inputs():
    first_line = input()

    if os.path.exists(first_line):
        with open(first_line, 'r') as f:
            main_args = f.readline()
            other_args = list(f.readlines())

    else:
        main_args = first_line
        other_args = list(input() for _ in range(int(first_line.split()[0])))

    arrival_rate, operator_service_rate, tiredness_rate = tuple(map(float, main_args[1]))
    averages = list(map(lambda operator_arg: list(map(float, operator_arg)), other_args))

    return arrival_rate, operator_service_rate, tiredness_rate, averages


def print_customer_reports(customers):
    system_times = []
    tired_system_times = []
    wait_times = []
    tired_counts = len(list(filter(lambda c: c.tired, customers)))

    for customer in filter(lambda c: not c.tired, customers):
        system_times.append([customer.star, customer.start_time - customer.service_time])

    for customer in filter(lambda c: not c.tired, customers):
        wait_times.append([customer.star, customer.start_time - customer.start_paziresh_time
                           + (customer.paziresh_time - customer.service_time)])

    for customer in filter(lambda c: not c.tired, customers):
        system_times.append([customer.star, customer.start_time - customer.service_time])

    for customer in filter(lambda c: c.tired, customers):
        tired_system_times.append([customer.star, customer.start_time - customer.tired_time])

    index = ["type", "value"]
    print("System times for processed users:")
    print(pd.DataFrame(data=system_times, index=index).groupby("type").mean())
    print("System times for tired users:")
    print(pd.DataFrame(data=tired_system_times, index=index).groupby("type").mean())
    print("Wait times for processed users:")
    print(pd.DataFrame(data=wait_times, index=index).groupby("type").mean())
    print("Number of tired users:", tired_counts)


def main():
    arrival_rate, operator_service_rate, tiredness_rate, averages = read_inputs()
    simulator = Simulator(arrival_rate, operator_service_rate, tiredness_rate, averages)
