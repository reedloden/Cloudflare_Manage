This script has morphed into a mirage of things. You can currently take a backup
of your DNS, Pagerules, and Global Settings (excludes Firewall settings).

Format to run python script:
`python cf_backup.py -u <User_email> -T <api_token> --<argument_action> --<argument_optional>`

Example:
`python cf_backup.py -u user@domain.com -T XXXXXYYYYAAAABBBB --settings`
^^Exports all zone settings into a json format ready to be applied to any zone

Argument Endpoints Supported:
--all
--dns
--pagerules
--settings

Additional Arguments Supported:
--zoneId (Takes in 1 zoneId to backup)
--zoneName (Takes in 1 zoneName to backup)
--db (Will export to a SQLlite DB)
--printzones (Will print out a list of your zoneNames and zoneIds)
--write_csv (Currently only works for exporting settings)


Backup Management Wish List:
1. take in arguments via config or commandline
    email - Done
    apiToken - Done
    zone(s) - Done
    interactive vs non-interactive - ????
    firewall settings -  ????
2. Prepare response data for later use
    Zone Settings - Done
    DNS Records - Done
    Page Rules - Done
3. Endpoints to Backup
    ZonesSettings - Done
    DNS - Done
    Page Rules -Done
    Firewall (Waf Rules) - ????
    Rate Limiting -
    Load Balancing  
    ....
4. Advanced Error Handling
    Argument check
    Allow user to correct miss guided arguments before exit
5. "Super User Mode" / SUDO
6. Add in Dev/Stagging argument for forward compatibility of API v5

Restore Management Wish List:
1. Restore endpoints from previous backup
    Zone Settings -
    DNS Records -
    Page Rules -
    Firewall -
2. allow for ability to change/modify configuration being applied prior to
3. prompt user on diff of configuration being applied
4. interactive vs. non-interactive -
