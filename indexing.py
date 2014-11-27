#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'binaa1@gmail.com'

import sys
import json
import requests
import logging

es_url = 'http://localhost:9200'
es_index = 'word2vec'
es_type = 'news-1'

default_api = '{es_url}/{es_index}/{es_type}'.format(
    es_url=es_url,
    es_index=es_index,
    es_type=es_type
)

schema = {
    "mappings": {
        "news-1": {
            "_source": { "enabled": False },
            "properties": {
                "word": {"type": "string", "index": "not_analyzed"},
                "x": {"type": "float"},
                "y": {"type": "float"}
            }
        }
    }
}

def args():
    if sys.version_info >= (2,7,0):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--api', dest='api', default=default_api)
        parser.add_argument('--data', dest='data')
        options = parser.parse_args()
    else:
        import optparse
        parser = optparse.OptionParser()
        parser.add_option("--api", dest="api", default=default_api)
        parser.add_option("--data", dest="data")
        (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    return options

def stream(path):
    for idx, line in enumerate(file(path)):
        item = line.strip().split(' ')
        try:
            word = item[0]
            x = float(item[-2])
            y = float(item[-1])
        except:
            continue
        yield idx, {
            'word': word,
            'x': x,
            'y': y
        }

def create_index_with_mapping(url, index, schema):
    map_api = url + '/' + index
    r = requests.put(map_api, json=json.dumps(schema))
    if r.status_code == 200:
        logging.info('mapping success {schema}'.format(schema=schema))
        logging.info(r.text)
        return True
    logging.error('mapping fail {schema}'.format(schema=schema))
    logging.error(r.text)
    return False

def put(api, id, data):
    put_api = api + '/{id}'.format(id=id)
    jdata = json.dumps(data)
    r = requests.put(put_api, data=jdata)
    if r.status_code == 200:
        logging.info('put success {id} {data}'.format(id=id, data=jdata))
        logging.info(r.text)
        return True
    logging.error('put fail {id} {data}'.format(id=id, data=jdata))
    logging.error(r.text)
    return False

def run():
    opt = args()
    #assert create_index_with_mapping(es_url, es_index, schema) == True, 'exit because fail to mapping'

    for id, doc in stream(opt.data):
        put(opt.api, id, doc)
    return 0

if __name__ == '__main__':
    logging.basicConfig(filename='neighborhood.log', level=logging.DEBUG)
    sys.exit(run())
