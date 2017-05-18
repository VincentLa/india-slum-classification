"""
Google Static Maps API (Screenshots)

Read input file of latitude and longitude coordinates and using chromedriver
Gets each URL and saves screenshot of map image
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from optparse import OptionParser
import json, pdb, csv, time, sys, urllib, urllib2, base64, hashlib, hmac, os

# Command line options to specify input output files
parser = OptionParser()

# Input file is a .csv file with x,y coordinates
# Output path is the full output path to save screenshots
# Username is simply local computer username
parser.add_option("-i", "--input-file", dest="input_file",
                  help="full path to input file (.csv of x,y)", metavar='"C:\\Users\\uname\\Documents\\Input_coords.csv"')

parser.add_option("-o", "--output-path", dest="output_path",
                  help="full path to output folder to save .png files", metavar='"C:\\Users\\uname\\Documents\\Static_Maps_Screenshots"')

parser.add_option("-u", "--username", dest="username",
                  help="FAS username to use in local Chromedriver path", metavar='"fas123"')

# (Optional) add email address to send Distance matrix status notifications
parser.add_option("-e", "--email", dest="email",
                  help="email address for status notifications", metavar='"address@gmail.com"')

# (Optional) set URL Static Map parameters
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
# Set folder path for downloads
if options.output_path:
    output_path = os.path.expanduser(options.output_path)
else:
    print "MUST SPECIFY OUTPUT PATH TO SAVE SCREENSHOTS WITH -o"
    sys.exit()
# Set username to use in local Chromedriver path
if options.username:
    username = (options.username)
else:
    print "MUST SPECIFY USERNAME WITH -u OR EDIT LOCATION OF CHROMEDRIVER PATH IN CODE"
    sys.exit()

# make email address and URL parameters optional arguments

# adding a status email address if specified
if options.email:
    email = options.email
    print "Using email address: %s for query status notifications\n" % email

# Set url parameters: zoom, size, scale, maptype
#   base URL="https://maps.googleapis.com/maps/api/staticmap?[parameters]"
#   parameters specified are: center=13.0628505,80.2764982&zoom=19&size=1024x1024&scale=2&maptype=satellite&key=
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

# Set chromedriver path
chromedriver_path = 'C:\\Users\\%s\\Desktop\\chromedriver' % username

# Use Chrome browser
chromedriver = chromedriver_path
driver = webdriver.Chrome()

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
f = open(input_file)
file_read = csv.reader(f)

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

    # add a long wait time after every 100 requests
    if file_num == int(file_num/100)*100:
        # wait an extra minute after every 100 requests
        g = int(file_num/100)+1
        time.sleep(60*g)
        # add 10 milliseconds to inter-image load times to incrementally slow down requests
        i += 0.01

    # Go to static maps url
    driver.get(signed_url)

    # Wait for image element
    driver.implicitly_wait(30)

    # save webelement, part of page (location and size)
    element = driver.find_element_by_tag_name('img')
    location = element.location
    el_size = element.size

    # wait to let image load
    time.sleep(4+i)

    # name file according to output path specified and row number
    file_name = '%s\\%d.png' % (output_path, file_num)

    # check if this file name already and break to avoid overwriting
    if os.path.exists(file_name):
        print "Trying to save to: \n %s \n" % file_name
        print "Image name already exists. Specify different output path."
        driver.quit()
        sys.exit()

    # Save screenshot of entire page
    driver.save_screenshot(file_name)

    # use PIL Python image library to open image in memory
    im = Image.open(file_name)

    # get origin and bottom right corner to define crop points
    left = location['x']
    top = location['y']
    right = location['x'] + el_size['width']
    bottom = location['y'] + el_size['height']

    # crop image according to size (0, 0, (size_w, size_h)/1 or 2 depending on scale)
    # ex. cropping 0, 0, 619, 619 (for 1280) or 450, 450 (for 900) for scale2
    #print "Total image %d, %d, %d, %d. Cropping %dx%d \n" % (left, top, right, bottom, right, bottom)
    #im = im.crop((left, top, right, bottom))
    # crop image to fixed size 880x880 (for 317m zoom comparison, slum-images specific)
    print "Total image %d, %d, %d, %d. Cropping 880x880 \n" % (left, top, right, bottom)
    im = im.crop((left, top, 880, 880))

    # re-save new cropped image over screenshot
    im.save(file_name)

    # increment file count after reading each row
    file_num += 1

# print number of rows read (- last increment)
total = file_num - 1
print "Finished! Processed %d total x,y requests \n" % total
print "Process End: %s" % time.asctime( time.localtime(time.time()) )

# close browser and .csv after reading last line
f.close()
driver.quit()
