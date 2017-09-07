import requests
import json
import os.path
import os
import time
import sys
import argparse
import itertools
import logging

logging.basicConfig(level=logging.DEBUG)

# Take in commandline arguments
parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('-u', dest='userEmail', help='Store userEmail',
                    required=True)
parser.add_argument('-T', dest='apiToken', help='Store API Token',
                    required=True)
parser.add_argument('--zoneId', dest='zone_id', default=False,
                    help='Zone you want logs for')
parser.add_argument('--zoneName', dest='zone_name', default=False,
                    help='Zone you want logs for')

# get parsed arguments
args = parser.parse_args()
arg_map = vars(args)

# setting session for requests
s = requests.Session()
s.headers.update({"X-Auth-Email": "%s" % args.userEmail,
            "X-Auth-Key": "%s" % args.apiToken,
            "Content-Type": "application/json"})

# define urls
cloudflare_v4 = "https://api.cloudflare.com/client/v4/zones"

# get zone id/name
def setZoneId():
#    if zone_id:

    if zone_name:
        r_getZoneId = s.get("%s/zones?name=%s" % (cloudflare_v4, zone_name))


def main():
    r_getLogs = s.get("%s/%s/logs/requests?start=1494376045" % (cloudflare_v4, args.zone_id))
    localfile = 'mydick2.txt'
    with open(localfile, 'wb') as f:
        for chunk in r_getLogs.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return localfile

main()
