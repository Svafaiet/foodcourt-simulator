from collections import Counter
import matplotlib.pyplot as plot

from simulater import SharifPlus


class SharifPlusAnalysor:
    def __init__(self, sharifplus: SharifPlus, customers):
        self.customers = customers
        self.sharfplus = sharifplus

    def _plot_population(self, ax, arrivals, departures, title, **kwargs):
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
        ax.set_title(title)
        return ax.plot(x, y, **kwargs)

    def plot_time_related(self):
        main_fig, (sys_ax, acc_ax) = plot.subplots(2, constrained_layout=True)
        self._plot_population(
            sys_ax,
            list(customer.start_time for customer in self.customers),
            list(customer.get_system_time() for customer in self.customers),
            title="System Population",
        )
        self._plot_population(
            acc_ax,
            self.sharfplus.acceptor.queue.insert_times,
            self.sharfplus.acceptor.queue.departure_times,
            title="Acceptor Queue Population",
        )
        operator_queue_fig, axs = plot.subplots(len(self.sharfplus.operators), constrained_layout=True)
        if len(self.sharfplus.operators) == 1:
            axs = [axs]
        for index, ax in enumerate(axs):
            self._plot_population(
                ax,
                self.sharfplus.operators[index].queue.insert_times,
                self.sharfplus.operators[index].queue.departure_times,
                title="Operator{} Queue Population".format(index),
            )

    def plot(self):
        plot.show()
