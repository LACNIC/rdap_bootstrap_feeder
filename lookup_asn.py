import json
from libs.libs import AutnumRange
import sys

asn = sys.argv[1]
f = open('resources/final.asn.json', mode='r')
objects = json.loads(f.read())
f.close()

for service in objects['services']:
    resources = service[0]
    endpoints = service[1]

    for resource in resources:
        if AutnumRange(string=asn).is_within(AutnumRange(string=resource)):
            print resource, endpoints[0]
