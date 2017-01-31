#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from itertools import groupby

def plot_time_series(arrive_time):
    data=[int(item) for item in arrive_time]     # Integerization
    data=[len(list(group)) for key,group in groupby(np.sort(data))] # Get time series
    plt.plot(range((len(data))),data)               # Plot
    plt.show()                                      # Show plot