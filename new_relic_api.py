import requests
import json
import datetime, time
import pprint

# GLOBAL VARS SETTINGS
NEWRELIC_API_KEY = "<NewRelicAppLicense>"
TIMEOUT = 72

HEADERS = {"X-Api-Key": NEWRELIC_API_KEY}
FROM_TIME = datetime.datetime.today() - datetime.timedelta(hours=TIMEOUT) # setting days from expiration


# SERVERS
def get_servers():
    SERVERS_URL = "https://api.newrelic.com/v2/servers.json"
    SERVERS_KEY = "servers"
    servers = []
    page = 1

    while True:
        data = {"page":page}
        response = requests.get(SERVERS_URL, headers=HEADERS, data=data)
        
        if response.status_code != 200:
            raise Exception("could not get servers - status code is not 200")
        json_response = json.loads(response.text)
        
        if json_response.has_key(SERVERS_KEY)==False:
            raise Exception("could not get servers - bad json response")
        servers_in_this_page = json_response[SERVERS_KEY]

        if len(servers_in_this_page) == 0:
            return servers
        servers += servers_in_this_page
        page+=1


def get_servers_to_delete(servers, last_reported):
    servers_to_delete = []
    for server in servers:
        server_last_reported = time.strptime(server["last_reported_at"], "%Y-%m-%dT%H:%M:%S+00:00")
        server_last_reported_datetime = datetime.datetime.fromtimestamp(time.mktime(server_last_reported))
        if server_last_reported_datetime < last_reported and server["reporting"]==False:
            servers_to_delete.append(server)
    return servers_to_delete


def delete_servers(servers_to_delete):
    DELETE_SERVERS_URL = "https://api.newrelic.com/v2/servers/%s.json"

    for server_to_delete in servers_to_delete:
        server_id_to_delete = server_to_delete["id"]
        print "about to delete %(server_to_delete)s" % vars()
        response = requests.delete(DELETE_SERVERS_URL % server_id_to_delete, headers=HEADERS)
        if response.status_code != 200:
            raise Exception("could not delete server - status code is not 200")


# APPLICATIONS

# get all application, return objects
def get_apps():
    APPLICATIONS_URL = "https://api.newrelic.com/v2/applications.json"
    APPLICATIONS_KEY = "applications"
    apps = []
    page = 1

    while True:
        data = {"page":page}
        res = requests.get(APPLICATIONS_URL, headers=HEADERS, data=data)
        if res.status_code != 200:
            raise Exception("could not get applications - status code is not 200")
        json_res = json.loads(res.text)
        if json_res.has_key(APPLICATIONS_KEY)==False:
            raise Exception("could not get applications - bad json response")
        apps_in_this_page = json_res[APPLICATIONS_KEY]
        if len(apps_in_this_page) == 0:
            return apps
        apps += apps_in_this_page
        page+=1

# get expired apps, takes (object, time) and return objects
def get_expired_apps(apps, last_reported):
    
    expired_apps = []
    
    for app in apps:
        if not "last_reported_at" in app :
            expired_apps.append(app)
            continue
        
        app_last_reported = time.strptime(app["last_reported_at"], "%Y-%m-%dT%H:%M:%S+00:00")
        app_last_reported_datetime = datetime.datetime.fromtimestamp(time.mktime(app_last_reported))
        if app_last_reported_datetime < last_reported and app["reporting"]==False:
            expired_apps.append(app)

    return expired_apps


# delete apps, takes objects
def delete_apps(apps_to_delete):
    DELETE_APPS_URL = "https://api.newrelic.com/v2/applications/%s.json"
    
    for a in apps_to_delete:
        a_name = a['name']
        print "about to delete %(a_name)s" % vars()
        response = requests.delete(DELETE_APPS_URL % a['id'], headers=HEADERS)
        if response.status_code != 200:
            raise Exception("could not delete app - status code is not 200")


# PRINT  (modify format if needed)
def print_names(objects):
    print "**********  There are %s applications  **********" % len(objects)
    for object in objects :
        print " -- NAME: %-28s -- ID: %-10s -- ACTIVE: %-5s" % (object['name'], object['id'], object['reporting'])


# MAIN
if __name__ == "__main__":

    _to_delete = get_expired_apps(get_apps(),FROM_TIME)
    print_names(_to_delete)
    delete_apps(_to_delete)

