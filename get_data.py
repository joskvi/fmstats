
import sys
import datetime
import time

import xml.etree.cElementTree as ETree
import requests

from db import Database


def get_recent_tracks_from_lastfm(username, api_key, page=1, page_size_limit=200):
    ''' Calls last.fm api and returns xml string '''
    
    api_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&page={page}&limit={limit}'
    api_url = api_url.format(username=username, api_key=api_key, page=page, limit=page_size_limit)
    
    response = requests.get(api_url)

    return response.text.encode('utf-8')

def get_number_of_track_pages(username, api_key, page_size_limit=200):
    ''' Calls last.fm api and return number of track pages available at a given page size '''

    tree = ETree.fromstring(get_recent_tracks_from_lastfm(username, api_key, page=1, page_size_limit=page_size_limit))
    recent_tracks = tree.getchildren()[0]

    return int(recent_tracks.attrib['totalPages'])

def tracks_xml_to_list(xml_track_list):
    ''' Takes track list from last.fm in xml format into a list of tuples '''

    tree = ETree.fromstring(xml_track_list)
    recent_tracks = tree.getchildren()[0]
    
    output_track_list = []

    for i, track in enumerate(recent_tracks.getchildren()):

        # Get song data
        try:
            play_time = track.find('date').text
        except AttributeError:
            # Song probably playing atm
            continue

        playtime = datetime.datetime.strptime(play_time, '%d %b %Y, %H:%M')
        track_name = track.find('name').text
        album_name = track.find('album').text
        artist_name = track.find('artist').text

        output_track_list.append((playtime, track_name, album_name, artist_name))

    return output_track_list


def insert_listens_to_db(listens):
    ''' Takes a list of tuples and inserts into db '''

    with Database('database.db') as db:
        for listen in listens:
            db.execute('INSERT INTO listens (ts, artist, album, track) VALUES (?, ?, ?, ?)', listen)
        

def load_all_tracks_into_db(username, api_key):
    ''' Takes a username and loads all tracks logged in last.fm to the db '''

    def report_progress(page, num_pages):
        progress_report = 'Processing page {} of {} ({}%) ...'
        progress_report = '\r' + progress_report.format(str(page), str(num_pages), str(round(float(page)/num_pages*100, 1)))
        sys.stderr.write(progress_report)
        sys.stderr.flush()
    
    page_limit = 200
    number_of_pages = get_number_of_track_pages(username, api_key, page_size_limit=page_limit)
    
    for page in range(1, number_of_pages + 1):
        
        report_progress(page, number_of_pages)
        
        track_list = tracks_xml_to_list(get_recent_tracks_from_lastfm(username, api_key, page=page, page_size_limit=page_limit))
        insert_listens_to_db(track_list)

        time.sleep(30)

    print('')


if __name__ == "__main__":

    import locale
    if locale.getlocale() != ('en_US', 'UTF-8'):
        print('Locale should be set to en_US, not {}.'.format(locale.getlocale()))

    import secrets
    username = secrets.LASTFM_USR
    api_key = secrets.LASTFM_API_KEY

    load_all_tracks_into_db(username, api_key)
