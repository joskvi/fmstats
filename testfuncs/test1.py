import analysis
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline, interp1d

csv_file = 'all_tracks.csv'
alltracks = analysis.read_csv(csv_file)
alltracks = np.array(alltracks, dtype=object)

total_stats = analysis.create_plot(alltracks)
number_of_artists = np.shape(total_stats)[1]
time = np.arange(number_of_artists)

print total_stats

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(time, total_stats[12,:])

interpolation_points = 300
time_smoothed = np.linspace(time.min(),time.max(), interpolation_points)
total_stats_smoothed = np.zeros((number_of_artists, interpolation_points))

for i in range(number_of_artists):
    total_stats_smoothed[i,:] = spline(time, total_stats[i,:], time_smoothed, order=3)

total_stats = total_stats_smoothed
time = time_smoothed

ax.plot(time, total_stats[12,:])

plt.show()