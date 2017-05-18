"""
Google Static Maps API

Read input file of latitude and longitude coordinates
Writes output file with: ID, latitude, longitude, Static_maps_URL
"""

from optparse import OptionParser

import base64
import csv
import hashlib
import hmac
import json
import os
import pdb
import sys
import time
import urllib
import urllib2

# Command line options to specify input output files
parser = OptionParser()

# Input file is a .csv file with x,y coordinates
# Output fle is a .csv file that writes: ID (row number),latitude,longitude,custom URL
parser.add_option("-i", "--input-file", dest="input_file",
                  help="full path to input file (.csv of x,y)", metavar='"C:\\Users\\uname\\Documents\\Input_coords.csv"')

parser.add_option("-o", "--output-file", dest="output_file",
                  help="full path to output file (.csv)", metavar='"C:\\Users\\uname\\Documents\\Output_coords.csv"')

# Options for URL parameters that can be specified: zoom, size, scale, maptype
# Zoom is an integer 0-21, size is WIDTHxHEIGHT, scale is 1, 2 or 4, maptype is satellite, terrain
parser.add_option("-z", "--zoom", dest="zoom",
                  help="zoom level 0-21+", metavar='"19"')

parser.add_option("-s", "--size", dest="size",
                  help="WxH image size in pixels 512x512 to 2048x2048", metavar='"1280x1280"')

parser.add_option("-c", "--scale", dest="scale",
                  help="scale image resolution, 1, 2 or 4", metavar='"2"')

parser.add_option("-t", "--maptype", dest="maptype",
                  help="Google map image type: satellite, terrain", metavar='"satellite"')

# load command line args into parser
(options, args) = parser.parse_args()

# make input file, output folder and username required arguments

# Set path for .csv with coordinates (x,y)
if options.input_file:
    input_file = os.path.expanduser(options.input_file)
else:
    print "MUST SPECIFY INPUT FILE WITH -i"
    sys.exit()
# Set output file path to write URLs
if options.output_file:
    output_file = os.path.expanduser(options.output_file)
else:
    print "MUST SPECIFY OUTPUT PATH TO SAVE SCREENSHOTS WITH -o"
    sys.exit()

# Set url parameters
# base URL="https://maps.googleapis.com/maps/api/staticmap?[parameters]"
# parameters specified are: center=13.0628505,80.2764982&zoom=19&size=1024x1024&scale=2&maptype=satellite&key=

# Optional parameters: URL parameters zoom, size, scale, maptype
# Set to default if not specified
if options.zoom: zoom = options.zoom
else: zoom = '19'
if options.size: size = options.size
else: size = '1280x1280'
if options.scale: scale = options.scale
else: scale = '2'
if options.maptype: maptype = options.maptype
else: maptype = 'satellite'

## MAIN CODE ##

# Set google url and service key
google_url = "http://maps.googleapis.com"
api_service = "/maps/api/staticmap?"
#clientID and privatekey from Google API for Work
client = "gme-harvarduniversity1"
privateKey = "fFINx5hoJ_ThkdXadWeIVbMD3d4="
channel = ""

# store starting date and time of batch and display to user
process_start_dtime = time.asctime( time.localtime(time.time()) )
print "Process Start: %s \n\n" % process_start_dtime

# print parameters for user to see
print "Using Static Map parameters...\nZoom: %s, Size: %s, Scale: %s, Map type: %s\n" % (zoom, size, scale, maptype)

# Open the coords .csv (x,y)
f_in = open(input_file, 'r')
f_out = open(output_file, 'w')
file_read = csv.reader(f_in)

# Set row number and wait increment to initial values
file_num = 1
i = 0

# read each row of coordinate pairs
for row in file_read:

    # concatenate elements of row, separating with comma (x,y)
    line = "".join(entry for entry in row)
    print "Image: %d, X,Y: %s" % (file_num, line)

    # Set full URL path by reading each row in the coords.csv (x,y) + parameters + signature

    # Generate valid signature
    encodedParams = urllib.urlencode({"center":line,"zoom":zoom,"size":size,"scale":scale,"maptype":maptype,"client":client,"sensor":"false"});
    # encdodedParams = urllib.urlencode("center=13.0628505,80.2764982&zoom=19&size=1024x1024&scale=2&maptype=satellite&key=
    # decode the private key into its binary format
    decodeKey = base64.urlsafe_b64decode(privateKey)
    urltosign = api_service + encodedParams
    # create a signature using the private key and the url encoded, string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decodeKey, urltosign, hashlib.sha1)
    # encode the binary signature into base64 for use within a URL
    encodedsignature = base64.urlsafe_b64encode(signature.digest())
    # Combine coordinates, parameters and signature into full url_path
    signed_url = google_url + api_service + encodedParams + "&signature=" + encodedsignature
    # print final URL used
    print "%s\n" % signed_url

    # write row number, coordinates and unique key encoded URL to output file
    f_out.write("%d,%s,%s\n" % (file_num, line, signed_url))

    # increment file count after reading each row
    file_num += 1

# print number of rows read (- last increment)
total = file_num - 1
print "Finished! Processed %d total URL requests" % total
print "Process End: %s\n" % time.asctime( time.localtime(time.time()) )
print "Wrote map URLs to output file %s" % output_file

# close both .csvs after reading last line
f_in.close()
f_out.close()
