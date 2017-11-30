#!/bin/python2

import argparse

import os_client_config


def get_sahara_client():
    cloud_config = os_client_config.get_config()
    return cloud_config.get_session_client("data_processing")


def get_id(client, cluster_name):
    url = "/clusters"
    raw_clusters = client.get(url)['clusters'].json()

    matches = [cluster['id'] for cluster in raw_clusters
                             if cluster['name'] == cluster_name]
    if len(matches) == 1:
        return matches[0]
    raise Exception("Can't find %s" % cluster_name)


def get_cluster(client, client_id):
    url = "/clusters/%s" % cluster_id
    return client.get(url).json()['cluster']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cluster_name', type=str,
                        help='Name of cluster')
    args = parser.parse_args()

    client = get_sahara_client()

    cluster_id = get_id(client, args.cluster_name)
    raw_cluster = get_cluster(client, cluster_id)

    raw_node_groups = raw_cluster['node_groups']
    groups = {group['name']: group['instances'] for group in raw_node_groups}

    import pprint
    pprint.pprint(groups)


if __name__ == '__main__':
    main()
