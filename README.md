# ansible-role-ceph-manila-mount
Automate the mounting of manila provided Ceph FS share.

If you need to install ansible, you could do this:

    virtualenv .venv
    . .venv/bin/activate
    pip install -U pip
    pip install ansible

You can run the playbook like this:

    ansible-playbook -i hosts site.yml
