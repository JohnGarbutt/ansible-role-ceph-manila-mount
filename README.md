# ansible-role-ceph-manila-mount
Automate the mounting of manila provided Ceph FS share.

You can use manila to create a CephFS share in a way similar to this:

	source openrc

	export SHARE_NAME=quicktest
	export SHARE_SIZE_GB=10
	export USER_NAME=testuser

	manila create --share-type cephfsnativetype --name $SHARE_NAME cephfs $SHARE_SIZE_GB
	manila access-allow $SHARE_NAME cephx $USER_NAME

	manila share-export-location-list $SHARE_NAME --columns path
	+-------------------------------------------------------------------------+
	| Path                                                                    |
	+-------------------------------------------------------------------------+
	| 10.0.10.101:6789:/volumes/_nogroup/2c6b0b4a-5fe5-48ea-a67c-90dd77a0b2b0 |
	+-------------------------------------------------------------------------+

	manila access-list $SHARE_NAME --columns access_to,access_key
	+-----------+------------------------------------------+
	| Access_To | Access_Key                               |
	+-----------+------------------------------------------+
	| quicktest | ABCBuPFZ7wNLExAAuWmBG7cvpbwD/4/XU/sU8g== |
	+-----------+------------------------------------------+

Then you should use the above to fill out roles/ceph-mount/vars/main.yml:

	ceph_mount_ceph_mon_host: 10.0.10.101
	ceph_mount_ceph_access_user: quicktest
	ceph_mount_ceph_access_key: ABCBuPFZ7wNLExAAuWmBG7cvpbwD/4/XU/sU8g==
	ceph_mount_ceph_share_id: 2c6b0b4a-5fe5-48ea-a67c-90dd77a0b2b0

If you need to install ansible, you could do this:

	virtualenv .venv
	. .venv/bin/activate
	pip install -U pip
	pip install ansible

You can run the playbook like this to mount the filesystem:

	ansible-playbook -i hosts site.yml --skip-tags unmount

You can run the playbook like this to unmount the filesystem:

	ansible-playbook -i hosts site.yml --skip-tags mount

Please let us know how it goes. Pull requests are very welcome.
