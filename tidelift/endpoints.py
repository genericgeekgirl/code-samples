import csv
import json
import sys
import re
from collections import OrderedDict
import time
import requests


def health(details):

    arguments = details.split("/")

    if len(arguments) > 2:
        print "Too many arguments: supply only packagename and version"
        return

    if len(arguments) < 2:
        print "Not enough arguments: supply packagename and version"
        return

    (packagename, version) = arguments

    licenses_file = csv.reader(open('licenses.csv', "rb"), delimiter=",", skipinitialspace=True)

    license_ = "" 

    for row in licenses_file:
        if packagename == row[0]:
            license_ = row[1]

    if not license_:
        print "Invalid package name"
        return

    vulnerabilities_file = csv.reader(open('vulnerabilities.csv', "rb"), delimiter=",")

    vulnerabilities = []

    for row in vulnerabilities_file:
        if packagename == row[1] and version == row[2]:
            vulnerabilities.append(row)

    if not vulnerabilities:
        print "No vulnerabilities found: check version number"
                
    json_vulnerabilities = []

    for vulnerability in vulnerabilities:
        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(vulnerability[4])))
        json_vulnerabilities.append({"id": vulnerability[0], "description": vulnerability[3], "created": created})

    output = OrderedDict([("name", packagename), ("version", version), ("license", license_), ("vulnerabilities", json_vulnerabilities)])

    print json.dumps(output, ensure_ascii=False, indent=4)



def releases(details):

    arguments = details.split("/")

    if len(arguments) > 1:
        print "Too many arguments: supply only packagename"
        return

    packagename = details

    r = requests.get("https://registry.npmjs.org/"+packagename)

    response = r.status_code 
    if (response == 404):
        print "Invalid package name"
        return
    
    data = json.loads(r.content)

    versions_data = data["versions"]
    versions = []

    for version in versions_data:
        versions.append(version)

    created = {}
        
    time_data = data['time']
    for version in versions:
        created[version] = time_data[version]
        
    latest = sorted(created, key=created.get, reverse=True)[0]
            
    output = OrderedDict([("name", packagename), ("latest", latest), ("versions", versions)])
    
    print json.dumps(output, ensure_ascii=False, indent=4)




# main #
    
if len(sys.argv) != 2:
    exit("Please specify one argument (URI)")
    
argument = sys.argv[1]

if re.search(r'[/]$', argument):
    exit("Malformed URI: ends in '/'")

if len(argument.split("/")) < 4:
    exit("Malformed URI: too short")

if len(argument.split("/")) > 5:
    exit("Malformed URI: too long")

(blank, package, endpoint, details) = argument.split("/", 3)

if package != "package":
    exit("Valid endpoints include 'package/health' and 'package/releases'")

if endpoint == "health":
    health(details)
elif endpoint == "releases":
    releases(details)
else:
    exit("Valid endpoints include 'package/health' and 'package/releases'")


