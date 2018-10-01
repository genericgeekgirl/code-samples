#!flask/bin/python
from flask import Flask, jsonify

import csv
import json
from collections import OrderedDict
import time
import requests

app = Flask(__name__)


@app.route('/package/releases/<string:packagename>', methods=['GET'])

def releases(packagename):

    r = requests.get("https://registry.npmjs.org/"+packagename)

    response = r.status_code
    if (response == 404):
        return jsonify("Invalid package name")

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

    return jsonify(output)



@app.route('/package/health/<string:packagename>/<string:version>', methods=['GET'])

def health(packagename, version):

    licenses_file = csv.reader(open('licenses.csv', "rb"), delimiter=",", skipinitialspace=True)

    license_ = ""

    for row in licenses_file:
        if packagename == row[0]:
            license_ = row[1]

    if not license_:
        return jsonify("Invalid package name")

    vulnerabilities_file = csv.reader(open('vulnerabilities.csv', "rb"), delimiter=",")

    vulnerabilities = []

    for row in vulnerabilities_file:
        if packagename == row[1] and version == row[2]:
            vulnerabilities.append(row)

    json_vulnerabilities = []

    for vulnerability in vulnerabilities:
        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(vulnerability[4])))
        json_vulnerabilities.append({"id": vulnerability[0], "description": vulnerability[3], "created": created})

    output = OrderedDict([("name", packagename), ("version", version), ("license", license_), ("vulnerabilities", json_vulnerabilities)])

    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
    
