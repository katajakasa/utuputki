# -*- coding: utf-8 -*-

import config
import json
import httplib

class NetException(Exception):
    """ Exception for interwebs errors """
    pass

def get_json(path):
    """ Fetches JSON response from API """
    conn = httplib.HTTPConnection(config.UTUPUTKI_API_DOMAIN)
    conn.request("GET", path)
    ret = conn.getresponse()
    if ret.status == 200:
        return json.loads(ret.read())
    else:
        raise NetException('Unable to fetch data from server')

def req_video():
    """ Fetches next video from API """
    return get_json(config.UTUPUTKI_API_PATH + '/next/')

def req_skips(id):
    """ Fetches skipping information from API """
    return get_json(config.UTUPUTKI_API_PATH + '/checkskip/?video_id=' + str(id))

