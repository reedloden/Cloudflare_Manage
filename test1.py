import subprocess
import time

subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneId <zone_id> --backupPR", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneId <zone_id> --backupDNS", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneId <zone_id> --backupSettings", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneId <zone_id> --backupAll", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneName <zone_name> --backupPR", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneName <zone_name> --backupDNS", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneName <zone_name> --backupSettings", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneName <zone_name> --backupAll", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --backupPR", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --backupDNS", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --backupSettings", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --backupAll", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --backupSettings --backupDNS", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneName <zone_name> --backupPR --backupDNS", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN> --zoneId <zone_id> --backupPR --backupSettings", shell=True)
time.sleep(2)
subprocess.call("python cf_backup.py -u <user@email.com> -T <API_TOKEN>", shell=True)
