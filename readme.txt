Currently this is only in a state to do Backups of settings and save the results
in a file structure that is ready to be used to update settings. Examples to run
the script:

python cf_backup.py -u <User_email> -T <api_token> --<argument_action> --<argument_optional>

Argument Actions Supported:
--backupSetting
--backupDNS
--backupPR
--backupAll

Arguments Optional:
--zoneId
--zoneName

* If you use --backupAll all others will be ignored. You can use any combination
of the other argument actions. ZoneId and ZoneName are optional.

Backup Management
1. take in arguments via config or commandline
    email - Done
    apiToken - Done
    zone(s) - Done
    interactive vs non-interactive - Not Implemented
    config file -  Not Implemented
2. write file structure of zones and timestamp backups - Done
    zones - Done
        backups-timestamped - Done
3. Prepare response data for later use
    Zone Settings - Done
    DNS Records - Semi Done
    Page Rules - Semi Done
4. Endpoints to Backup (please add any endpoint you want to be supported)
    ZonesSettings - Done
    DNS - Done
    Page Rules -Done
    Waf Rules - Not Implemented (requires special logic)
    ....
5. Advanced Error Handling - Not Implemented
    Argument check
    Allow user to correct miss guided arguments before exit
6. "Super User Mode" / SUDO - Not Implemented
7. Add in Dev/Stagging argument for forward compatibility of API v5

Updating / Migrating Configuration
1. backup zones previous to being written to
    a. allow for roll-back of zone
    b. allow for ability to apply previous backup
2. allow for ability to change/modify configuration being applied prior to
3. prompt user on diff of configuration being applied
4. interactive vs. non-interactive - Not Implemented
5. need to identify what can not be updated via the api
    Zone Settings
        advanced_ddos, mobile_redirect if mobile_subdomain = null, tls_1_2_only
    DNS
        Not investigated
    Page Rules
        Not investigated

Things I don't like
1. Truth List. To support both lookup via zoneId and zoneName I had to come up
    up with a way to match either of these two arguments with an action. Now
    however I can break this into if x and not y statements.
2. I always grab the Zone list. Majority of times this is needed except when you
    ask pass ZoneId. It's an extra call but I have no way of getting the zone
    name without it. If anyone knows a way of getting the ZoneName without
    getting the whole list, please share.

Things I would like to do in the nearish future
1. See this supported by a web interface
2. Make this interactive where you can pull the settings, modify a value, and
    update the setting.
