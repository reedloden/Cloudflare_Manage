import json
import sys
import collections
import requests
import csv
import os
import urllib

# define urls
cloudflare_v4 = "https://api.cloudflare.com/client/v4"

# write DNS to a Zone
def write_dns(data, zone_id, arg_map, s):
    for i in data['items']:
        dns_entries = {}
        for k, v in i.iteritems():
            if k in ('type','name','content','ttl','proxied'):
                dns_entries[k]= i[k]
        new_dns = s.post('{api}/zones/{zone}/dns_records'.format(api=cloudflare_v4, zone=zone_id), data=json.dumps(dns_entries))
        print new_dns.content

# write Global settings to a Zone
def write_settings(data, zone_id, arg_map, s):
    for i in data['items']:
        zone_settings = {}
        for k, v in i.iteritems():
            if i['modified_on'] == None:
                break
            else:
                payload = "{\"value\":\"%s\"}" % i['value']
                response = s.patch('{api}/zones/{zone}/settings/{endpoint}'.format(api=cloudflare_v4, zone=zone_id, endpoint=i['id']), data=payload)
                print(response.text)
                break

# restore Pagerules
def write_pagerules(data, zone_id, arg_map, s):
    for i in reversed(data['items']):
        for x in i.iteritems():
            payload = {
                    'targets':i['targets'],
                    'actions':i['actions'],
                    'priority': i['priority'],
                    'status': i['status']
                    }
            print json.dumps(payload)

            break

def main(data, zone_name, zone_id, end_point, arg_map, s):
    print end_point
    if end_point == 'dns_records':
        write_dns(data, zone_id, arg_map, s)
    if end_point == 'settings':
        write_settings(data, zone_id, arg_map, s)
    if end_point == 'pagerules':
        write_pagerules(data, zone_id, arg_map, s)
