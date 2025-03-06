import matplotlib.pyplot as plt
import numpy as np

# Generate random data for two datasets
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(1, 1, 1000)

# Define the number of bins for the histogram
bins = 30

# Compute the histogram values for both datasets
count1, bins1, _ = plt.hist(data1, bins=bins, label='Data 1', histtype='stepfilled', align='mid', alpha=0.5)
count2, bins2, _ = plt.hist(data2, bins=bins, label='Data 2', histtype='stepfilled', align='mid', alpha=0.5)

# Adjust positions to ensure histograms are side by side
width = (bins1[1] - bins1[0]) * 0.4  # Adjust the width of the bars
offset = width  # Set an offset for the second histogram

plt.close()

# Replot the histograms with adjusted positions
plt.bar(bins1[:-1] - offset / 2, count1, width=width, alpha=0.5, label='Data 1', edgecolor='black')
plt.bar(bins2[:-1] + offset / 2, count2, width=width, alpha=0.5, label='Data 2', edgecolor='black')

# Add labels and a legend
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

# Show the plot
plt.show()