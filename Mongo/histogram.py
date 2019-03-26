import matplotlib.pyplot as plt
import numpy as np




class Histogram:

    def __init__(self, title="", limit_low="", limit_high="", x_value="", x_label="", y_label=""):

        self.title = title
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.x_value = x_value
        # self.y_value = y_value
        self.x_label = x_label
        self.y_label = y_label

    def show(self):
        # Show histogram.
        n, bins, patches = plt.hist(x=self.x_value, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
        # Show limits.
        plt.hist([self.limit_low] * 10, rwidth=0.3, color='tab:red')
        plt.annotate('limit_low', rotation=-90, xy=(1, 1), xytext=(self.limit_low+0.05, 2))
        plt.hist([self.limit_high] * 10, rwidth=0.3, color='tab:red')
        plt.annotate('limit_high', rotation=-90, xy=(1, 1), xytext=(self.limit_high + 0.05, 2))
        # Show titles, labels grid.
        plt.text(23, 45, r'$\mu=15, b=3$')
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(axis='y', alpha=0.75)
        # plt.grid(True)
        # plot.axis([x_start, x_end, y_start, y_end])
        # plt.ylim(-2, 2)
        # plt.xlim(-2, 2)

        # Set a clean upper y-axis limit.
        max_y = n.max()
        plt.ylim(top=np.ceil(max_y / 10) * 10 if max_y % 10 else max_y + 10)
        plt.show()





