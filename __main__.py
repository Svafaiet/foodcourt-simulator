import os

from simulater import Simulator

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

simulator = Simulator(arrival_rate, operator_service_rate, tiredness_rate, averages)
