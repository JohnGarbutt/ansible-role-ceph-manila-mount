#!/bin/bash

set -eux

pip install python-saharaclient

CLUSTER_NAME=${CLUSTER_NAME:-spark-rdma}

CLUSTER_TEMPLATE_NAME=${CLUSTER_TEMPLATE_NAME:-rdma-spark-2-1-0}
IMAGE_NAME=${IMAGE_NAME:-sahara-vanilla-2.8.0-centos7}
KEYPAIR_NAME=${KEYPAIR_NAME:-alaska-gate}
NETWORK_NAME=${NETWORK_NAME:-ilab}

# Create a cluster.
if ! openstack dataprocessing cluster show ${CLUSTER_NAME} >/dev/null 2>&1; then
    openstack dataprocessing cluster create \
        --name ${CLUSTER_NAME} \
        --cluster-template ${CLUSTER_TEMPLATE_NAME} \
        --image ${IMAGE_NAME} \
        --user-keypair ${KEYPAIR_NAME} \
        --neutron-network ${NETWORK_NAME}
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

$SCRIPTPATH/list-sahara-instances.py $CLUSTER_NAME
