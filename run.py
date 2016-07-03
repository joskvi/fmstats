#!flask/bin/python
import sys
import getopt
import numpy as np

import analysis
import get_user_data
from app import app

try:
    import config_local as config
except ImportError:
    try:
        import config
    except ImportError:
        raise ImportError('Cannot find a config file.')

# Set constants. Move this to separate file
username = config.USERS[0]
xml_file = 'alltracks_' + username + '.xml'
csv_file = 'alltracks_' + username + '.csv'

def usage():
    print '''\nFMstats\n
--plot\t\tPlot data.
--fetch\t\tDownload data.
--flask\t\tStart flask server hosting a web application for showing user plots.
'''

def main(argv):

    try:
        options, remainders = getopt.getopt(argv, 'h', ['help','plot','fetch','flask'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '--plot':
            alltracks = analysis.read_csv(csv_file)
            alltracks = np.array(alltracks, dtype=object)
            analysis.create_plot(alltracks)
        elif opt == '--fetch':
            get_user_data.fetch_all_user_data(username)
        elif opt == '--flask':
            app.debug = True
            app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main(sys.argv[1:])
