from collections import Counter
import matplotlib.pyplot as plot

from simulater import SharifPlus


class SharifPlusAnalysor:
    def __init__(self, sharifplus: SharifPlus, customers):
        self.customers = customers
        self.sharfplus = sharifplus

    def _plot_population(self, ax, arrivals, departures, **kwargs):
        c = Counter(arrivals)
        c.subtract(Counter(departures))
        x = []
        y = []
        population = 0
        for time, diff in sorted(list(c.items())):
            x.append(time)
            y.append(population)
            population = population + diff
            if diff:
                x.append(time)
                y.append(population)
        print(x, y)
        return ax.plot(x, y, **kwargs)

    def plot_time_related(self):
        fig, (ax1, ax2) = plot.subplots(1, 2)
        self._plot_population(
            ax1,
            self.sharfplus.acceptor.queue.insert_times,
            self.sharfplus.acceptor.queue.departure_times,
        )
        # self._plot_population(
        #     ax2,
        #     self.sharfplus.acceptor.queue.insert_times,
        #     self.sharfplus.acceptor.queue.departure_times,
        # )
        fig.show()
