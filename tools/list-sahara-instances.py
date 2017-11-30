#!/bin/python2

import argparse

import os_client_config


def get_sahara_client():
    cloud_config = os_client_config.get_config()
    return cloud_config.get_session_client("data_processing")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cluster_name', type=str,
                        help='Name of cluster')
    args = parser.parse_args()

    client = get_sahara_client()

    url = "/clusters/%s" % args.cluster_name
    import pprint
    pprint.pprint(client.get(url))

if __name__ == '__main__':
    main()
