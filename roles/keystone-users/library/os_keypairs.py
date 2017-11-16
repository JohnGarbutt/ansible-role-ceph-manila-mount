#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

import os_client_config


ANSIBLE_METADATA = {'metadata_version': '1.0'}


def get_users(identity_client, project_name):
    # TODO - filter by project
    proj_response = identity_client.get(
            "/v3/projects?name=%s" % project_name).json()
    raw_projects = proj_response["projects"]
    if len(raw_projects) != 1:
        raise Exception("Invalid project_name")
    project_id = raw_projects[0]["id"]

    assign_response = identity_client.get(
        "/v3/role_assignments?include_names=1"
        "&scope.project.id=%s" % project_id,
        microversion="3.6").json()
    # TODO - check paging
    raw_assignments = assign_response["role_assignments"]
    users = [(a['user']['id'], a['user']['name']) for a in raw_assignments]
    users = set(users)
    return [{'name':u[1], 'user_id':u[0]} for u in users]


def get_keypairs(compute_client, user_id):
    response = compute_client.get(
        "/os-keypairs?user_id=%s" % user_id, microversion="2.15").json()
    raw_keypairs = response['keypairs']
    return [k['keypair']['public_key'] for k in raw_keypairs]


def main():
    module = AnsibleModule(
        argument_spec = dict(
            project_name=dict(required=True, type='str'),
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

    users = get_users(identity_client, module.params['project_name'])

    authorized_keys = {}
    for user in users:
        keypairs = get_keypairs(compute_client, user['user_id'])
        if keypairs:
            authorized_keys[user['name']] = "\n".join(keypairs)

    if authorized_keys:
        module.exit_json(changed=False, authorized_keys=authorized_keys)

if __name__ == '__main__':
    main()
