from collections import Counter
import matplotlib.pyplot as plot

from customer import Customer
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

    def _plot_hitograms(self, ax, points, title, **kwargs):
        ax.set_title(title)
        return ax.hist(points, bins=int(len(points)/80) + 1, **kwargs)

    def _fig_close(self):
        plot.figure().clear()
        plot.close()
        plot.cla()
        plot.clf()

    def plot_time_related(self, show):
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
        main_fig.savefig("main-fig.png")
        if not show:
            self._fig_close()
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
        operator_queue_fig.savefig("operators-fig.png")
        if not show:
            self._fig_close()

    def plot_customer_related(self, show):
        customers_grouped_by_star = dict()
        for star in Customer.star_probability.keys():
            customers_grouped_by_star[star] = []
        for customer in self.customers:
            customers_grouped_by_star[customer.star].append(customer)
        wait_fig, wait_axs = plot.subplots(len(Customer.star_probability.keys()), constrained_layout=True)
        for index, ax in enumerate(wait_axs):
            self._plot_hitograms(
                ax,
                list(customer.get_total_wait_time() for customer in customers_grouped_by_star[index]),
                title="Customer {}star Wait Histogram".format(index),
            )
        wait_fig.savefig("waits-fig.png")
        if not show:
            self._fig_close()
        resp_fig, resp_axs = plot.subplots(len(Customer.star_probability.keys()), constrained_layout=True)
        for index, ax in enumerate(resp_axs):
            self._plot_hitograms(
                ax,
                list(customer.get_total_service_time() for customer in customers_grouped_by_star[index]),
                title="Customer {}star Service Histogram".format(index),
            )
        resp_fig.savefig("service-fig.png")
        if not show:
            self._fig_close()

    def plot(self, show):
        if show:
            plot.show()
