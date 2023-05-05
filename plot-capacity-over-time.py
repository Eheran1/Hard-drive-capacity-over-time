# -*- coding: utf-8 -*-
"""
Created on Fri 05.05.2023
@author: Eheran
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import YearLocator, DateFormatter
from datetime import datetime
import pandas as pd
file_name = 'HDD_dataframe.csv'

# Load the DataFrame from CSV file, ignore comments
data = pd.read_csv(file_name, parse_dates=['Date'], comment='#')

# Create the plot
fig, ax = plt.subplots()
# Choose x and y data, visualize as dots
ax.plot(data['Date'], data['Capacity'], 'o')
#print(data['Date'], data['Capacity'])

# Create regression line:
# Parameter from regression, without outliers in 2007/8/9 and higher weights on the last 20 years
A = -4.7
B = 15.5
C = -7400
D = 3200
E = -0.37

# Create a DataFrame with all the years from 1980.01.01 to 2025.01.01
years = pd.date_range(start='1980-01-01', end='2025-01-01', freq='YS')
df = pd.DataFrame({'date': years})
# Calculate the number of days since the first date (1980.01.01)
df['days_since'] = (df['date'] - df['date'].iloc[0]).dt.days
# Apply the formula (called ExtrValCum(a,b,c,d)) to the 'days_since' column 
# and create a new column with the results
df['Capacity_regression'] = np.exp(A + B * np.exp(-np.exp(-((df['days_since'] - D * E + C) / D))))
# plot the regression result, visualize as blue, dashed line
ax.plot(df['date'], df['Capacity_regression'], 'b--')

# x-axis fortmatting
# Display years only, as YYYY format
years = YearLocator()   
yearsFmt = DateFormatter('%Y')
ax.xaxis.set_major_formatter(yearsFmt)
# Display x and y-ticks on both top and bottom / left and right
ax.tick_params(axis='x', which='both', top=True, bottom=True)
ax.tick_params(axis='y', which='both', left=True, right=True)
# Set the x-axis start and end values to 1980 and 2025
ax.set_xlim(datetime(1980, 1, 1), datetime(2025, 1, 1))
# Creaty a copy of the axis to have a second spine on the rigt side of the plot
ax2 = ax.twinx()


# y-axis fortmatting
# Set the y-axis to log10-scale, do the same for the 2. y-axis
ax.set_yscale('log')
ax2.set_yscale('log')
# Configure y-axis ticks of both y-axis
ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=9))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=(2, 3, 4, 5, 6, 7, 8, 9), numticks=10))
ax2.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=9))
ax2.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=(2, 3, 4, 5, 6, 7, 8, 9), numticks=10))
# Replace the existing y-axis formatter with the custom one
# We want 1 MB... 100 TB instead of 0.001 GB.... 100000 GB
def custom_y_axis_formatter(x, pos):
    if x < 1:
        return f"{x * 1e3:g} MB"
    elif x < 1e3:
        return f"{x / 1e0:g} GB"
    else:
        return f"{x / 1e3:g} TB"
ax.yaxis.set_major_formatter(ticker.FuncFormatter(custom_y_axis_formatter))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(custom_y_axis_formatter))
ax.set_ylim(0.001, 1e5)    # =0.001 GB to 100 TB, the underlying value is still in GB
ax2.set_ylim(ax.get_ylim())

# Add gridlines to the major tick markers of both x and y axis
ax.grid(which='major')
# save file as .svg
plt.savefig('HDD - capacity over time.svg')
plt.show()
