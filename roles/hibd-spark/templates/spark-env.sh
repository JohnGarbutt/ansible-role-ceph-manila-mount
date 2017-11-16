export SPARK_CONF_DIR=/opt/spark/conf
export SPARK_MASTER_HOST={{ groups['hibd-spark-master'][0] }}
export SPARK_LOCAL_IP=`hostname -s`

export SPARK_WORKER_MEMORY=96g
export SPARK_WORKER_CORES=120
export SPARK_DAEMON_MEMORY=90g

export PYSPARK_DRIVER_PYTHON={{ hibd_spark_py3_venv }}/bin/python3
export PYSPARK_PYTHON={{ hibd_spark_py3_venv }}/bin/python3
