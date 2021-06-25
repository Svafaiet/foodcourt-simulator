import pandas as pd


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
