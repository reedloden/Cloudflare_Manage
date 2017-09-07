import requests
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('-u', dest='userEmail', help='Store userEmail',
                    required=True)
parser.add_argument('-T', dest='apiToken', help='Store API Token',
                    required=True)
parser.add_argument('--file', dest='backup_file', default=False,
                    help='File to use to restore DNS.', required=True)
parser.add_argument('--zoneId', dest='fromZoneId', default=False,
                    help='Zone you want to import dns to', required=True)

args = parser.parse_args()

s = requests.Session()
s.headers.update({"X-Auth-Email": "%s" % args.userEmail,
            "X-Auth-Key": "%s" % args.apiToken})

cloudflare_v4 = "https://api.cloudflare.com/client/v4"

location = args.backup_file
zone_id = args.fromZoneId

files = {'file': open(location, 'rb')}
s.post('%s/zones/%s/dns_records/import' % (cloudflare_v4, zone_id), files=files)
