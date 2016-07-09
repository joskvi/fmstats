import requests
import re
import time
import xml.etree.cElementTree as ET
import sys
import datefunc

# Import config file
try:
    import config_local as config
except ImportError:
    try:
        import config
    except ImportError:
        raise ImportError('Cannot find a config file.')

def fetch_all_user_data(username):
    # Returns LastFM listening data on specified user.
    # Should do some checking on wether user exists.

    filename_xml_dump = 'lastfm_data/' + username + '.xml'
    filename_csv_dump = 'lastfm_data/' + username + '.csv'
    baseurl = ''.join(['http://ws.audioscrobbler.com/2.0/',
                   '?method=user.getrecenttracks',
                   '&user=', username,
                   '&api_key=', config.API_KEY,
                   '&limit=200'])

    def clean_xml(xml_tree):
        xml_data = re.split('<track', xml_tree, maxsplit=2)[2]
        xml_data = re.split('</recenttracks>', xml_data)[0]
        return '<track' + xml_data
        #return '\n'.join(xml_tree.split('\n')[12:-3])

    def report_progress(page, num_pages, width=50):
        '''
        filled = '=' * int(ratio*width)
        rest = '-' * (width - int(ratio*width))
        sys.stderr.write('\r|' + filled + rest + '|')
        '''
        progress = 'Currently on page {}/{} ... {}%'
        sys.stderr.write('\r' + progress.format(str(page), str(num_pages), str(round(float(page)/num_pages*100, 1))) )
        sys.stderr.flush()

    # Fetch first page with info
    response = requests.get(baseurl+'&page=1')
    tree = ET.fromstring(response.text.encode('utf-8'))
    num_pages = int(tree[0].attrib['totalPages'])

    # File to save results, overwrites old file
    fh = open(filename_xml_dump, 'w+')
    fh.write('<alltracks>')

    print 'Initating user data request.'

    # Send request and clean each response
    for page in range(1, num_pages+1):
        time.sleep(2)
        report_progress(page, num_pages)
        response = requests.get(baseurl+'&page='+str(page))
        xml_tree = clean_xml(response.text)
        fh.write(xml_tree.encode('utf-8'))

    fh.write('</alltracks>')
    fh.close()

    print '\nUser data download complete.'
    create_csv_file(filename_xml_dump, filename_csv_dump)
    print 'XML and CSV files created.'

def create_csv_file(xml_file, csv_file):

    alltracks = ET.parse(xml_file).getroot()
    f = open(csv_file, 'w+')

    for track in alltracks:

        artist = track.find('artist').text
        name = track.find('name').text
        album = track.find('album').text

        date = track.find('date')

        # Check if track has date attribute. Skip element if not.
        if date is None:
            continue

        # Change date formatting from DD Month YYYY to YYYYMMDD
        date = re.split(r'[, ]+', date.text)[0:3]
        date = ''.join([date[2], datefunc.month2num(date[1]), date[0]])

        csvline = '{}\t{}\t{}\t{}\n'.format(date, artist.encode('utf-8'), name.encode('utf-8'), album.encode('utf-8'))
        f.write(csvline)

    f.close()
