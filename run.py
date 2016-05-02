#!/usr/bin/python
import sys
import getopt
import numpy as np

import analysis

xml_file = 'all_tracks.xml'
csv_file = 'all_tracks.csv'

def usage():
    print '''How to use fmstats:
          -i to specify input file. Must be .csv or .xml file. Required.
          -o to output path of output image
          '''

def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['help', 'type'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    alltracks = analysis.read_csv(csv_file)
    alltracks = np.array(alltracks, dtype=object)

    analysis.create_plot(alltracks)


if __name__ == '__main__':
    main(sys.argv[1:])
