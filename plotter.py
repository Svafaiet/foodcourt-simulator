from collections import Counter


class SimulatorPlotter:
    def plot_population(self, ax, arrivals, departures, **kwargs):
        c = Counter(arrivals) - Counter(departures)
        x = []
        y = []
        population = 0
        for time, diff in sorted(list(c.items())):
            x.append(time)
            y.append(population)
            population = population + diff
            x.append(time)
            y.append(population)
        ax.plot(x, y, **kwargs)
