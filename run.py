#!flask/bin/python
import sys
import getopt
import numpy as np

import analysis
import fetch
from app import app

# Set constants. Move this to separate file
username = 'joskvi'
xml_file = 'all_tracks_' + username + '.xml'
csv_file = 'all_tracks_' + username + '.csv'
# SPECIFY APIKEY ALSO

def usage():
    print '''How to use fmstats:
          -o specifies output file name.
          -i specifies input file name. Must be .csv file, using ; as separator.
          --plot to plot data
          --fetch to download data. Use with argument csv or xml, to specify output filetype. Use with -o
          --flask to start flask server hosting a simple application for showing user plots
          '''

def main(argv):

    try:
        options, remainders = getopt.getopt(argv, 'hi:o:', ['help','plot','fetch','flask'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '-o':
            output_filename = arg
        elif opt == '-i':
            input_filename = arg
        elif opt == '--plot':
            alltracks = analysis.read_csv(csv_file)
            alltracks = np.array(alltracks, dtype=object)
            analysis.create_plot(alltracks)
        elif opt == '--fetch':
            fetch.fetch_all_user_data(username, xml_file)
        elif opt == '--flask':
            app.debug = True
            app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main(sys.argv[1:])
