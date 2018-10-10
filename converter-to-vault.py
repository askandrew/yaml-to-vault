#!/usr/bin/env python
import argparse, yaml
import hvac

parser = argparse.ArgumentParser(description='Params for vault')
parser.add_argument('file', metavar='file', type=str, help='Yaml file path')
parser.add_argument('service_name', metavar='service_name', type=str, help='test_andrew')
parser.add_argument('host', metavar='host', type=str, nargs='?', help='Vault host name', default='localhost')
parser.add_argument('token', metavar='token', type=str, nargs='?', help='Vault token', default="-")
args = parser.parse_args()

from_file = {}
client = hvac.Client(url=args.host, token=args.token)


def process_data(rest):
    ss = {}
    for k in list(rest):
        ss[k] = rest[k]
        
    client.write('secret/'+args.service_name, **ss)


def parse_data(d, key):
    for k, v in d.iteritems():
        if key != "":
            newkey = str(key) + "/" + str(k)
        else:
            newkey = str(key) + str(k)

        if isinstance(v, dict):
            parse_data(v, newkey)
        else:
            val = str(v)
            newkey = newkey.replace("/", "_")
            from_file[newkey] = val


with open(args.file, 'r') as stream:
    try:
        data = yaml.load(stream)
        parse_data(data, "")
        process_data(from_file)

    except yaml.YAMLError as exc:
        print(exc)
