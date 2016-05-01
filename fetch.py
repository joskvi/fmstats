import requests
import time
import xml.etree.cElementTree as ET


filename_dump = 'all_tracks.xml'

baseurl = ''.join(['http://ws.audioscrobbler.com/2.0/',
                   '?method=user.getrecenttracks',
                   '&user=joskvi&api_key=fa26698d2bf6b5523524675364fe1003&limit=200'])

# Cleans up xml response
def clean_xml(the_xml):
    return "\n".join(the_xml.split("\n")[12:-3])
    """
    lines = the_xml.split('\n')[1:-3]
    first_line = lines[0].split('><')[-2:]
    first_line = '<'+first_line[0]+'>\n<'+first_line[1]+'>'
    lines[0] = first_line
    return '\n'.join(lines)
    """


# Fetch first page with info
response = requests.get(baseurl+'&page=1')
tree = ET.fromstring(response.text.encode('utf-8'))
num_pages = int(tree[0].attrib['totalPages'])



# File to save results, overwrites old file
fh = open(filename_dump, 'w+')

for page in xrange(1, num_pages+1):
    time.sleep(2)
    progress = 'On page {} of {}...........  {}%'
    print progress.format(str(page),
                          str(num_pages),
                          str(round(float(page)/num_pages*100, 1)))
    response = requests.get(baseurl+'&page='+str(page))
    the_xml = clean_xml(response.text)
    fh.write(the_xml.encode('utf-8'))
fh.close()
