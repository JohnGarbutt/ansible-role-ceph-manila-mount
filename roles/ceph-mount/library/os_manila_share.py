#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

import os_client_config


ANSIBLE_METADATA = {'metadata_version': '1.0'}


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            type=dict(required=False, type='str'),
            protocol=dict(required=False, type='str'),
            size_gb=dict(required=False, type='int'),
        ),
        supports_check_mode=False
    )

    try:
        cloud_config = os_client_config.get_config()
        share_client = cloud_config.get_session_client("sharev2")
    except Exception, e:
        module.fail_json(msg="Unable to initialise OpenStack client: %s" % e)

    if not share_client:
        module.fail_json(msg="Please check your OpenStack credentials.")

    raw_shares = share_client.get(
        "/shares/detail?name=%s" % "jmfg2-spark-test").json()['shares']
    if not raw_shares:
        raise Exception("Invalid share name")

    raw_share = raw_shares[0]

    # TODO if size doesn't match, should expand the share
    share = {
        "id": raw_share['id'],
        "size" : raw_share['size'],
    }

    # TODO - some drivers have a preferred export.
    exports = raw_share['export_locations']
    if exports:
        share['export'] = exports[0]

    headers={"X-Openstack-Manila-Api-Version": "2.40"}
    payload = {"access_list": None}
    raw_access = share_client.post(
            "/shares/%s/action" % share['id'],
            json=payload, headers=headers).json()['access_list']
    access_key = None
    for access in raw_access:
        if access['access_to'] == "spark":
            access_key = access['access_key']
            break

    # TODO - get access if this user doesn't have access
    share['access_key'] = access_key

    module.exit_json(changed=False, details=share)

if __name__ == '__main__':
    main()
