import pandas as pd
import matplotlib.pyplot as plt


def compute_stats_work_days(data):
    stats = data.describe()
    data.plot(x='date', y='hours')
    plt.show()

    return stats
