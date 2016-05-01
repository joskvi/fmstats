import xml.etree.cElementTree as ET
import datefunc
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline


xml_file = 'all_tracks.xml'
csv_file = 'all_tracks.csv'


# CLEANUP FUNCTIONS

def create_csv(xml_file, csv_file):

    alltracks = parse_xml(xml_file)
    f = open(csv_file, 'w+')

    for track in alltracks:

        artist = track.find('artist').text
        name = track.find('name').text
        album = track.find('album').text

        # Change date formatting from DD Month YYYY to YYYYMMDD
        date = re.split(r'[, ]+', track.find('date').text)[0:3]
        date = ''.join([date[2], datefunc.month2num(date[1]), date[0]])

        csvline = '{};{};{};{}\n'.format(date,artist.encode('utf-8'),name.encode('utf-8'),album.encode('utf-8'))
        f.write(csvline)

    f.close()
    return

def parse_xml(xml_file):
    return ET.parse(xml_file).getroot()

def read_csv(csv_file):

    alltracks = []
    with open(csv_file, 'rb') as csvfile:
        csv_tracks = csv.reader(csvfile, delimiter=';')
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
        return most_played(tracks, 2)
    else:
        return most_played(tracks, 3)

def create_plot(alltracks):

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


    time = np.arange(number_of_months)

    # Create smoothed data
    interpolation_points = 300
    time_smoothed = np.linspace(time.min(),time.max(), interpolation_points)
    total_stats_smoothed = np.zeros((number_of_artists, interpolation_points))

    for i in range(number_of_artists):
        total_stats_smoothed[i,:]=spline(time,total_stats[i,:],time_smoothed)

    # Create a fig with a subplot
    fig, ax = plt.subplots(figsize=(20, 10))

    # Set colormap
    cm = plt.get_cmap('Paired')
    ax.set_color_cycle([cm(1.*i/number_of_artists) for i in range(number_of_artists)])

    # Plot data
    ax.stackplot(time_smoothed, total_stats_smoothed[:,::-1]) # Plot with reverse order, i.e. chronologically, on x-axis

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(artists, loc='center left', bbox_to_anchor=(1, 0.5))


    # Modify x-axis
    plt.xticks(np.arange(min(time), max(time)+1, 1.0))
    ax.set_xticklabels(monthly_time[::-1]) # Set x-axis time label in reversed order as the plot order also is reversed

    plt.show()

# MAIN

alltracks = read_csv(csv_file)
alltracks = np.array(alltracks, dtype=object)

create_plot(alltracks)
