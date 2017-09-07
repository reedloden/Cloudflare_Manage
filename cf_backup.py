import requests
import json
import os.path
import os
import time
import sys
import argparse
import itertools
import logging
import compare_zones2
import cf_restore

logging.basicConfig(level=logging.DEBUG)

# Take in commandline arguments
parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('-u', dest='userEmail', help='Store userEmail',
                    required=True)
parser.add_argument('-T', dest='apiToken', help='Store API Token',
                    required=True)
parser.add_argument('--all', action='store_true', dest='all',
                    default=False, help='If True will backup all endpoints.')
parser.add_argument('--dns', action='store_true', dest='dns',
                    default=False, help='If True will backup DNS.')
parser.add_argument('--pagerules', action='store_true', dest='pagerules',
                    default=False, help='If True will backup Page Rules')
parser.add_argument('--settings', action='store_true',
                    dest='settings', default=False,
                    help='If True will backup global zone settings')
parser.add_argument('--zoneId', dest='fromZoneId', default=False,
                    help='Zone you want to Backup')
parser.add_argument('--zoneName', dest='fromZoneName', default=False,
                    help='Zone you want to Backup.')
parser.add_argument('--db', dest='db', action='store_true',
                    default=False, help='Backup to local db')
parser.add_argument('--firewall', dest='firewall', action='store_true',
                    default=False, help='If True will backup firewall settings')
parser.add_argument('--printzones', dest='printzones', action='store_true',
                    default=False, help='If True will print zone names and ids to a file.')
parser.add_argument('--write_csv', dest='write_csv', action='store_true',
                    default=False, help='Will export endpoint values to csv.')
parser.add_argument('--file', dest='backup_file', default=False, help='File to use to restore enpoint.')
parser.add_argument('--restore', dest='restore', action='store_true', default=False,
                    help='Will restore a particular endpoint & zone you declare.')
parser.add_argument('--backup', dest='backup', action='store_true', default=False,
                    help='Will backup particular endpoint(s) & zone(s) you declare.')


# get parsed arguments
args = parser.parse_args()
arg_map = vars(args)

# setting session for requests
s = requests.Session()
s.headers.update({"X-Auth-Email": "%s" % args.userEmail,
            "X-Auth-Key": "%s" % args.apiToken,
            "Content-Type": "application/json"})

# define urls
cloudflare_v4 = "https://api.cloudflare.com/client/v4"

# endpoints that are backed up with --backup all argument configurable.
endPoints = ['dns_records', 'pagerules', 'settings', 'firewall']

ep_args_mapping = {
    'dns': 'dns_records',
    'pagerules': 'pagerules',
    'settings': 'settings',
    'firewall': 'firewall'
}

# backup time set for when the script is ran.
backup_time = time.strftime("%Y-%m-%d_%H:%M:%S")

# check and create or raise error on directories being created
def checkPathExists(directory):
    try:
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise

# to write the backup of modified response
def writeBackupConfig(content, path, filename):
    checkPathExists(path)
    with open(path + '/' + filename, 'w') as backupfile:
        json.dump(content, backupfile, sort_keys=True, indent=4)

    backupfile.close()

def numberOfPages():
    r_getZones = s.get("%s/zones/?per_page=50" % cloudflare_v4)
    json_data = json.loads(r_getZones.content)
    pages = json_data['result_info']['total_pages']
    print pages

    return pages

# get all zone names and ids and put them in an array
def getZones(**kwargs):
    allZones = {}
    # if zoneId or zoneName were passed sets the allzones dic accordingly
    zone_id = kwargs.pop('fromZoneId', None)
    zone_name = kwargs.pop('fromZoneName', None)

    if zone_id:
        r_getZones = s.get("%s/zones/%s" % (cloudflare_v4, zone_id))
        json_data = json.loads(r_getZones.content)
        json_data = json_data['result']
        allZones[json_data['name']] = json_data['id']
            # api for zonename returns results as an array
        return allZones
    if zone_name:
        r_getZones = s.get("%s/zones?name=%s" % (cloudflare_v4, zone_name))
        return map_zone_name_id(r_getZones)
    # If you did not declare the zoneName or ZoneId
    else:
        page = numberOfPages()
        zone_map = {}
        while page != 0:
            r_getZones = s.get("%s/zones/?page=%s&per_page=50" % (cloudflare_v4, page))
            json_data = json.loads(r_getZones.content)
            for i in json_data['result']:
                zone_map.update({i['name']:i['id']})
                #prints all zones and ids and exits
                if page == 1 and args.printzones:
                    f = open('ListOfZones.json', 'w')
                    strinify = str(zone_map)
                    f.write(strinify)
                    f.close()
                    sys.exit()

            page -= 1
        return zone_map

def map_zone_name_id(zones):
    zone_map = {}
    json_data = json.loads(zones.content)
    for i in json_data['result']:
        zone_map[i['name']] = i['id']
    return zone_map


# takes response and modfies it to be used for future updates to the endpoint
def modifyResponse(response):
    results= {}
    response = json.loads(response)
    results['items'] = response['result']
    return results


# logic to get result and backup
def backupZoneSettings(allZones, end_points):
    for ep in end_points:
        for zoneName, zoneId in allZones.items():
            if ep is 'pagerules' or 'settings':
                r_allZoneSetting = s.get("%s/zones/%s/%s" %
                                        (cloudflare_v4, zoneId, ep))
            if ep == 'firewall':
                r_allZoneSetting = s.get("%s/zones/%s/%s/waf/packages/" %
                                    (cloudflare_v4, zoneId, ep))
                packageIds = modifyResponse(r_allZoneSetting)
                r_allZoneSetting = s.get("%s/zones/%s/%s/waf/packages/%s/groups" %
                                    (cloudflare_v4, zoneId, ep, package_id))
            if ep == 'dns_records':
                r_allZoneSetting = s.get("%s/zones/%s/%s?per_page=100" %
                                        (cloudflare_v4, zoneId, ep))

            zoneSettings = r_allZoneSetting.content

            zoneSettings = modifyResponse(zoneSettings)

            if arg_map['db']:
                compare_zones2.main(zoneSettings, zoneName, zoneId, ep, arg_map)

            if not arg_map['write_csv']:
                path = os.path.join(backup_time, zoneName)
                filename = ep + '.json'
                writeBackupConfig(zoneSettings, path, filename)

            if arg_map['restore'] and (arg_map['dns'] or arg_map['settings'] or arg_map['pagerules']) and arg_map['backup_file']:
                with open(arg_map['backup_file']) as data_file:
                    data = json.load(data_file)

                cf_restore.main(data, zoneName, zoneId, ep, arg_map, s)

    if arg_map['write_csv']:
        compare_zones2.destory_db()

# matching zoneIds with zoneNames
def alignZone():
    if args.fromZoneId:
        passAlong = getZones(fromZoneId=args.fromZoneId)
    elif args.fromZoneName:
        passAlong = getZones(fromZoneName=args.fromZoneName)
    else:
        passAlong = getZones()

    # returns {zoneName : zoneId}
    return passAlong


def args_to_backups():
    backups = []
    if arg_map['all']:
        backups = endPoints
    else:
        for arg, ep in ep_args_mapping.iteritems():
            if arg_map[arg]:
                backups.append(ep)
    return backups

def main():
    passAlong = alignZone()
    backups = args_to_backups()

    if backups:
        backupZoneSettings(passAlong, backups)

    else:
        print 'Please provide an option.'

main()
