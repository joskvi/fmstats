import xml.etree.cElementTree as ET
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

# FILE I/O FUNCTIONS

def read_csv(csv_file):

    alltracks = []
    with open(csv_file, 'rb') as csvfile:
        csv_tracks = csv.reader(csvfile, delimiter='\t')
        for track in csv_tracks:
            track[0] = int(track[0])
            alltracks.append(track)
    return alltracks

# ANALYSIS FUNCTIONS

def count_tracks_per_month(alltracks):
    # Returns a list of playings per month, starting from most recent month

    tracks_per_month = [0]
    current_month = int(str(alltracks[0,0])[4:6])

    for i in alltracks[:,0]:
        m = int(str(i)[4:6])
        if m == current_month:
            tracks_per_month[-1]+=1
        else:
            current_month = m
            tracks_per_month.append(1)

    return tracks_per_month

def group_plays(alltracks):
    # Returns an array consisting of arrays with the played tracks for each month, and info on which month each group is
    # The grouping is sorted starting with the most recent month

    monthly = count_tracks_per_month(alltracks)
    monthly.insert(0,0)
    monthly = [sum(monthly[0:i+1]) for i in range(len(monthly))]
    alltracks_grouped = np.zeros((len(monthly)-1, 2), dtype=object)

    for i in range(len(monthly)-1):
        alltracks_grouped[i,0] = alltracks[monthly[i]:monthly[i+1],:] # Get play data for this group
        alltracks_grouped[i,1] = int(str(alltracks[monthly[i]][0])[0:6]) # Get the month of the this group

    return alltracks_grouped

def most_played(alltracks, top_list_length, sort_by='artist'):
    # Returns a sorted list of the top <number_of_artists> most played artists, songs or albums

    if sort_by.lower() == 'song':
        unique, counts = np.unique(alltracks[:,2], return_counts=True)
    elif sort_by.lower() == 'album':
        unique, counts = np.unique(alltracks[:,3], return_counts=True)
    else:
        unique, counts = np.unique(alltracks[:,1], return_counts=True)

    artist_plays = np.array([unique,counts],dtype=object).T
    artist_plays = artist_plays[artist_plays[:,1].argsort()[::-1]]

    if np.shape(artist_plays)[0] < top_list_length:
        return artist_plays
    else:
        return artist_plays[0:top_list_length,:]

def most_played_scaled(tracks, sort_by='artist'):
    # Uses most_played function, but scales top_list_length according to the length of tracks

    number_of_tracks = np.shape(tracks)[0]
    if number_of_tracks < 100:
        return most_played(tracks, 3)
    else:
        return most_played(tracks, 6)

def create_plot(alltracks, show=True):

    # Set plot type
    create_smoothed_plot = False
    add_edge_data = True

    # Arange track data
    tracks_grouped_by_month = group_plays(alltracks)
    monthly_time = tracks_grouped_by_month[:,1]
    monthly_tracks = tracks_grouped_by_month[:,0]
    monthly_tracks = [most_played_scaled(tracks) for tracks in monthly_tracks] # Fetches most played artists, but possible to change in function argument

    number_of_months = len(monthly_tracks)

    # Create artists list consisting of all artists from top played list
    artists = []
    for group in monthly_tracks:
        for artist in group:
            artist = artist[0]
            if artist not in artists:
                artists.append(artist)

    number_of_artists = len(artists)
    total_stats = np.zeros((number_of_artists, number_of_months), dtype=int)

    # Arange statistics of number of plays pr artist pr month
    for month, group in enumerate(monthly_tracks):
        monthly_stats = np.zeros(number_of_artists, dtype=int)
        for artist_stat in group:
            monthly_stats[artists.index(artist_stat[0])] = artist_stat[1]
        total_stats[:,month] = monthly_stats

    if add_edge_data:
        # Add zeros column to total_stats
        zero_column = np.zeros(number_of_artists, dtype=int)
        total_stats = np.column_stack([zero_column, total_stats, zero_column])
        number_of_months += 2

    # Skew data
    max_column_sum = np.array([column.sum() for column in total_stats.T]).max()
    skewing_row = np.zeros(number_of_months, dtype=int)
    for month, column in enumerate(total_stats.T):
        column_sum = column.sum()
        if column_sum < max_column_sum:
            skewing_row[month] = (max_column_sum - column_sum)/2
    total_stats = np.vstack([skewing_row, total_stats])

    time = np.arange(number_of_months)

    if create_smoothed_plot:
        # Give the data plot smoothed curves

        interpolation_points = 300
        time_smoothed = np.linspace(time.min(),time.max(), interpolation_points)
        total_stats_smoothed = np.zeros((number_of_artists, interpolation_points))

        for i in range(number_of_artists):
            total_stats_smoothed[i,:] = spline(time, total_stats[i,:], time_smoothed)

        total_stats = total_stats_smoothed
        time = time_smoothed


    # Create a fig with a subplot
    fig, ax = plt.subplots(figsize=(20, 10))

    # Set colormap
    cm = plt.get_cmap('Paired')
    color_cycle = [cm(1.*i/number_of_artists) for i in range(number_of_artists)]
    color_cycle.insert(0, (1.0, 1.0, 1.0))
    ax.set_color_cycle(color_cycle)

    # Plot data
    ax.stackplot(time, total_stats[:,::-1]) # Plot with reverse order, i.e. chronologically, on x-axis

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis

    ## QUICKFIX: removing non-ascii chars due to unicode problem in mpl
    artists = [ ''.join([i if ord(i) < 128 else '_' for i in text]) for text in artists ]

    artists.insert(0,'Skewing plot') # Insert a legend entry for the skewing plot
    ax.legend(artists, loc='center left', bbox_to_anchor=(1, 0.5))

    # Modify x-axis
    plt.xticks(np.arange(min(time), max(time)+1, 1.0))
    ax.set_xticklabels(monthly_time[::-1]) # Set x-axis time label in reversed order as the plot order also is reversed

    if show:
        plt.show()
    else:
        return fig

def plot_flask(user):

    csv_file = 'alltracks_' + user + '.csv'
    alltracks = read_csv(csv_file)
    alltracks = np.array(alltracks, dtype=object)

    return create_plot(alltracks, show = False)


