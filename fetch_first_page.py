import requests
import xml.etree.cElementTree as ET


filename_dump = 'all_tracks.xml'

baseurl = ''.join(['http://ws.audioscrobbler.com/2.0/',
                   '?method=user.getrecenttracks',
                    '&user=joskvi&api_key=fa26698d2bf6b5523524675364fe1003&limit=200'])

# Fetch first page with info
response = requests.get(baseurl+'&page=1')
tree = ET.fromstring(response.text.encode('utf-8'))
print tree[0].attrib