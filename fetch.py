import requests
import time
import xml.etree.cElementTree as ET
import sys

def fetch_all_user_data(username, filename_dump):
    # Returns LastFM listening data on specified user.
    # Should do some checking on wether user exists.

    baseurl = ''.join(['http://ws.audioscrobbler.com/2.0/',
                   '?method=user.getrecenttracks',
                   '&user=', username,
                   '&api_key=fa26698d2bf6b5523524675364fe1003&limit=200'])

    def clean_xml(xml_tree):
        return '\n'.join(xml_tree.split('\n')[13:-3])

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
    fh = open(filename_dump, 'w+')
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
