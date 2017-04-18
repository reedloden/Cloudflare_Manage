#!/bin/bash

mkdir compareSettings

curl -sSL https://github.com/sschemel/Cloudflare_Manage/archive/master.zip --output compareSettings/compareSettings.zip

echo "unziping files"
unzip -o compareSettings/compareSettings.zip -d compareSettings/

echo "Getting Zone Settings for user: $1"
python compareSettings/Cloudflare_Manage-master/cf_backup.py -u $1 -T $2 --settings --db --write_csv

rm -rf compareSettings
