#!/usr/bin/env python3

import requests
import json
from urllib.parse import urlparse

import argparse
import logging
import getpass

import subprocess
import sys

INFO_PATH = '/rest/public/1.0/links/info/'

parser = argparse.ArgumentParser(description='Fetch file from Egnyte link')
parser.add_argument('url', help='Egnyte URL')
parser.add_argument('-i', '--info',  action='store_true', default = False,
    help='print info for the link')
parser.add_argument('-d', '--dry-run',  action='store_true', default = False, 
    help='no download, print wget command')

args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

o = urlparse(args.url)
url = o.scheme + '://' + o.netloc
eid = o.path.split('/')[-1]

passwd = getpass.getpass()
jpasswd = {'password': passwd} 

s = requests.Session()
r = s.post(url + INFO_PATH + eid, json = jpasswd)

if r.status_code != 200:
    log.critical('info request status code: ' + str(r.status_code))
    print(r.text)
    sys.exit(1)

info = r.json()
if args.info:
    print(json.dumps(info, indent=4))

link = info['downloadLink']
file = info['filename']

cmd = ['wget', '-O', file, url+link]

if args.dry_run:
    print(' '.join(cmd))
else:
    r = subprocess.run(cmd)
