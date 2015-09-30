#!/usr/bin/env python3

import pycurl
import json
import os
import copy
import argparse
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('nightlydownload')
log.propagate = False

try:
    from systemd import journal
    log.addHandler(journal.JournalHandler())
except ImportError:
    from logging.handlers import SysLogHandler
    log.addHandler(SysLogHandler())

parser = argparse.ArgumentParser()
parser.add_argument("filelistpath", type=str, help="json list of urls")
parser.add_argument("outpath", type=str, help="output folder for files")
args = parser.parse_args()


log.info('Starting nightly download')

files = []
with open(args.filelistpath) as filelist:
    files = json.load(filelist)

# used to write out the files not downloaded
files_left = copy.copy(files)

for item in files:
    p = urlparse(item['url'])
    filename = p.path.split("/")[-1]  # assume the last substr is the filename
    if 'filename' in item:
        filename = item['filename']

    path = os.path.join(args.outpath, filename)
    success = True

    # Resume support
    resume = False
    open_mode = "wb"
    # if os.path.exists(path):
    #     open_mode = "ab"
    #     resume = True

    with open(path, open_mode) as fp:
        try:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, item['url'])
            curl.setopt(pycurl.WRITEDATA, fp)
            curl.setopt(pycurl.NOSIGNAL, 1)

            # if resume:
            #     curl.setopt(pycurl.RESUME_FROM, os.path.getsize(filename))

            curl.perform()
            if curl.getinfo(pycurl.HTTP_CODE) != 200:
                log.warn("Failed to download %s" % item['url'])
                success = False
        except pycurl.error as error:
            log.warn(str(error))
        # except Exception as e:
        #     log.error(str(e))
        finally:
            curl.close()

    if success:
        del(files_left[0])

        with open(args.filelistpath, "w") as filelist:
            json.dump(files_left, filelist)


log.info('Finished nightly download')
