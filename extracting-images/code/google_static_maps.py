"""
Google Static Maps API

Read input file of latitude and longitude coordinates
Writes output file with: ID, latitude, longitude, Static_maps_URL
"""

import argparse
import csv
import os
import requests
import time
import urllib.parse


# Set url parameters
# base URL="https://maps.googleapis.com/maps/api/staticmap?[parameters]"
# parameters specified are: center=13.0628505,80.2764982&zoom=19&size=1024x1024&scale=2&maptype=satellite&key=


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Google Static Maps URL Writer')
    parser.add_argument(
        '--input_file', help='Full path to input file (.csv of x,y)', required=True)
    parser.add_argument(
        '--output_file', help='Full path to output file (.csv)', required=True)
    parser.add_argument(
        '--zoom', default=19, help='Zoom level int 0-21+')
    parser.add_argument(
        '--size', default='1280x1280', help='WxH image size in pixels 512x512 to 2048x2048.')
    parser.add_argument(
        '--scale', default='2', help='Scale image resolution, 1, 2 or 4')
    parser.add_argument(
        '--maptype', default='satellite', help='Google map image type: satellite, terrain')
    return parser.parse_args()


def main():
    """Main function to run Static Maps URL Writer"""
    args = get_args()
    print(args.input_file)

    # Set google url and service key
    google_url = "http://maps.googleapis.com"
    api_service = "/maps/api/staticmap?"
    #clientID and privatekey from Google API for Work
    # client = "gme-harvarduniversity1"
    privateKey = os.getenv('GOOGLE_STATIC_MAPS_API')
    channel = ""

    # store starting date and time of batch and display to user
    process_start_dtime = time.asctime(time.localtime(time.time()))
    print("Process Start: %s \n\n" % process_start_dtime)

    # print parameters for user to see
    print("Using Static Map parameters...\nZoom: %s, Size: %s, Scale: %s, Map type: %s\n" %
          (args.zoom, args.size, args.scale, args.maptype))

    # Open the coords .csv (x,y)
    f_in = open(args.input_file, 'r')
    f_out = open(args.output_file, 'w')

    # Need to put this inside the below for loop.
    f_image = open('/Users/VincentLa/git/india-slum-classification/extracting-images/output/static.png','wb')
    file_read = csv.reader(f_in)

    # Set row number and wait increment to initial values
    file_num = 1

    # read each row of coordinate pairs
    for row in file_read:

        # concatenate elements of row, separating with comma (x,y)
        line = ",".join(entry for entry in row)
        print('Image: %d, X,Y: %s' % (file_num, line))

        # Set full URL path by reading each row in the coords.csv (x,y) + parameters + signature

        # Generate valid signature
        encodedParams = urllib.parse.urlencode({
            'center': line,
            'zoom': args.zoom,
            'size': args.size,
            'scale': args.scale,
            'maptype': args.maptype,
            # 'client': client,
            'sensor': "false"
        })
        signed_url = google_url + api_service + encodedParams + "&key=" + privateKey
        # print final URL used
        print('%s\n' % signed_url)

        # write row number, coordinates and unique key encoded URL to output file
        f_out.write("%d,%s,%s\n" % (file_num, line, signed_url))
        f_image.write(requests.get(signed_url).content)
        f_image.close()

        # increment file count after reading each row
        file_num += 1

    # print number of rows read (- last increment)
    total = file_num - 1
    print('Finished! Processed %d total URL requests' % total)
    print('Process End: %s\n' % time.asctime(time.localtime(time.time())))
    print('Wrote map URLs to output file %s' % args.output_file)

    # close both .csvs after reading last line
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    main()
