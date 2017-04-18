import json
import sqlite3 as lite
import sys
import collections
import requests
import csv
import os

#setting_ids = json.load(open('path/file.json'))

#s = requests.Session()
#s.headers.update({"X-Auth-Email": "<email>",
#            "X-Auth-Key": "<api_token>",
#            "Content-Type": "application/json"})

#with open('path/file.json') as data_file:
#    data = json.load(data_file)
#def create_columnsandvalues(i, columns, values):

#    for k, v in i.iteritems():
#        columns.append(k)
#        values.append(v)

#    columns = (', '.join("'" + str(column) + "'" for column in columns))
#    values = (', '.join("'" + str(value) + "'" for value in values))
#    return columns, values

db_name = 'Cloudflare.db'


def pagerules_insert(data, zone_name, zone_id):
    db = lite.connect(db_name)

    with db:
        db.row_factory = lite.Row
        c = db.cursor()
        # c.execute("DROP TABLE IF EXISTS PAGERULE_SETTINGS;")
        c.execute("CREATE TABLE IF NOT EXISTS PAGERULE_SETTINGS( \
        row_id INTEGER PRIMARY KEY, actions BLOB, created_on TEXT, id TEXT, \
        modified_on TEXT, priority TEXT, status TEXT, targets BLOB, zone_name text, \
        zone_id text)")

        for i in data['items']:
            if i['actions']:
                i['actions'] = json.dumps(i['actions'])
            if i['targets']:
                i['targets'] = json.dumps(i['targets'])

            columns = ['zone_name', 'zone_id']
            values = [zone_name, zone_id]
            for k, v in i.iteritems():
                columns.append(k)
                values.append(v)

            columns = (', '.join("'" + str(column) + "'" for column in columns))
            values = (', '.join("'" + str(value) + "'" for value in values))
            print columns, values
            query = "INSERT INTO PAGERULE_SETTINGS (%s) VALUES (%s);" % (columns , values)
            print query
            c.execute(query)


def dns_insert(data):
    db = lite.connect(db_name)

    with db:
        db.row_factory = lite.Row
        c = db.cursor()
        # c.execute("DROP TABLE IF EXISTS DNS_SETTINGS;")
        c.execute("CREATE TABLE IF NOT exists DNS_SETTINGS( \
        row_id INTEGER PRIMARY KEY, content TEXT, created_on TEXT, id TEXT, \
        locked TEXT, meta BLOB, modified_on TEXT, name TEXT, proxiable TEXT, \
        proxied TEXT, priority TEXT, ttl INT, type TEXT, zone_id TEXT, zone_name TEXT)")

        for i in data['items']:
            if i['meta']:
                i['meta'] = json.dumps(i['meta'])
            columns = []
            values = []
            for k, v in i.iteritems():
                columns.append(k)
                values.append(v)

            columns = (', '.join("'" + str(column) + "'" for column in columns))
            values = (', '.join("'" + str(value) + "'" for value in values))
# delete            #print columns
# delete            #print values

            query = "INSERT INTO DNS_SETTINGS (%s) VALUES (%s);" % (columns , values)
# delete            print query
            c.execute(query)

def settings_insert(data, zone_name, zone_id, arg_map):
    db = lite.connect(db_name)

    with db:
        db.row_factory = lite.Row
        c = db.cursor()

        # c.execute("DROP TABLE IF EXISTS ZONE_SETTINGS;")
        c.execute("CREATE TABLE IF NOT exists ZONE_SETTINGS(row_id INTEGER PRIMARY KEY, \
                modified_on text, editable text, id text,value BLOB, time_remaining INTEGER, \
                certificate_status text, zone_name text, zone_id text)")

        for i in data['items']:
            if i['id'] == 'minify':
# delete                print json.dumps(i['value'])
                i['value'] = json.dumps(i['value'])
            if i['id'] == 'mobile_redirect':
                i['value'] = json.dumps(i['value'])
            if i['id'] == 'security_header':
                i['value'] = json.dumps(i['value'])

            columns = ['zone_name', 'zone_id']
            values = [zone_name, zone_id]
            for k, v in i.iteritems():
                columns.append(k)
                values.append(v)


            columns = (', '.join("'" + str(column) + "'" for column in columns))
            values = (', '.join("'" + str(value) + "'" for value in values))
# delete            print columns, values
            query = "INSERT INTO ZONE_SETTINGS (%s) VALUES (%s);" % (columns , values)
# delete            print query
            c.execute(query)
# delete            print query
        if arg_map['write_csv']:
            #c.connect(".headers on")
            #c.execute(".mode csv")
            #c.execute(".once customer.csv")
            c.execute("SELECT * from ZONE_SETTINGS ORDER BY ID ASC")
            #c.execute(".system customer.csv")
            #data = c.fetchall()

            with open('output.csv', 'wb') as f:
                writer = csv.writer(f)
                writer.writerow([ i[0] for i in c.description ])
                writer.writerows(c.fetchall())

def destory_db():
    os.remove(db_name)



def main(data, zone_name, zone_id, end_point, arg_map):
    if end_point == 'settings':
        settings_insert(data, zone_name, zone_id, arg_map)
    if end_point == 'dns_records':
        dns_insert(data)
    if end_point == 'pagerules':
        pagerules_insert(data, zone_name, zone_id)
#    if end_point == 'firewall':
#        firewall_insert(data, zone_name, zone_id)
