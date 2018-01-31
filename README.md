# ansible-role-ceph-manila-mount

This repository is being used to automate the customization of various clusters
and includes roles for:

* Adds OpenStack clouds.yaml file (role: `openstack-conf`)
* Adds specific keystone users, password from keystone-pam, ssh keys from Nova
  (role: `keystone-users`)
* Add CephFS mount (using fuse), pulls connection info from Manila
  (role: `ceph-mount`)
* TODO: add GlusterFS mount, using connection info from Manila
* Installs Docker-ce (role: `docker`)
* Adds cAdvisor and Prometheus Node exporter (role: `prometheus-docker-node`)
* Adds cAdvisor and Prometheus Node exporter (role: `prometheus-docker-node`)
* Configures Prometheus and Grafana (role: `prometheus-server`)
* Configures spark to use a Python34 virtualenv, restarts Spark, adds some
  ssh keys to hadoop and centos users (role: `hibd-spark`)
* Installs, configures and runs spark-bench and HiBD's spark microbenchmarks
  (role: `hibd-bench` and role: `spark-bench`)

If you need to install ansible, you could do this:

	virtualenv .venv
	. .venv/bin/activate
	pip install -U pip
	pip install ansible

    ansible-galaxy install stackhpc.os-config stackhpc.os-keypair-login \
                           stackhpc.os-keystone-pam stackhpc.os-manila-mount \
                           stackhpc.monasca-agent

To access the vault protected passwords in the groupvars, we need to give
ansible access to the vault password, such as telling it where your password
file lives:

    export ANSIBLE_VAULT_PASSWORD_FILE=.vaultpass

To access OpenStack APIs for getting ssh keys we need admin credentials:

    source openrc

Or if you have a clouds.yaml file configured:

    export OS_CLOUD=alaska

To run all the playbooks (except benchmarks), you can do:

    ansible-playbook master.yml

If you want to run the benchmarks you can do this:

    ansible-playbook playbooks/bench.yml

Currently there are the following cluster inventories:

* (default) `alt-1-spark` RDMA enabled Spark running on alaksa alt-1

Please let us know how it goes. Pull requests are very welcome.

## Notes on Manila

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

Then you should use the above to fill out ``roles/ceph-mount/vars/main.yml``:

	ceph_mount_ceph_mon_host: 10.0.10.101
	ceph_mount_ceph_access_user: quicktest
	ceph_mount_ceph_access_key: ABCBuPFZ7wNLExAAuWmBG7cvpbwD/4/XU/sU8g==
	ceph_mount_ceph_share_id: 2c6b0b4a-5fe5-48ea-a67c-90dd77a0b2b0

After the above, update the ``hosts`` file to list the hostnames (or IPs)
for all the servers you wish mount the ceph filesystem on. In the future
we hope to provide tools to generate that information from a magnum
cluster or similar.
