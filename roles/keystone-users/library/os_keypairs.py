#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

import os_client_config


ANSIBLE_METADATA = {'metadata_version': '1.0'}


def get_users(identity_client):
    response = identity_client.get("/v3/users").json()
    raw_users = response['users']
    return [{'name':u['name'], 'user_id':u['id']} for u in raw_users]


def get_keypairs(compute_client, user_id):
    response = compute_client.get(
        "/os-keypairs?user_id=%s" % user_id, microversion="2.15").json()
    raw_keypairs = response['keypairs']
    return [k['public_key'] for k in raw_keypairs]


def main():
    module = AnsibleModule(
        argument_spec = dict(
            all=dict(required=True, type='bool'),
        ),
        supports_check_mode=False
    )

    try:
        cloud_config = os_client_config.get_config()
        identity_client = cloud_config.get_session_client("identity")
        compute_client = cloud_config.get_session_client("compute")
    except Exception, e:
        module.fail_json(msg="Unable to initialise OpenStack client: %s" % e)

    if not identity_client or not compute_client:
        module.fail_json(msg="Please check your OpenStack credentials.")

    users = get_users(identity_client)
    for user in users:
        user['keypairs'] = get_keypairs(compute_client, user['user_id'])

    module.exit_json(changed=True, users=users)

if __name__ == '__main__':
    main()
