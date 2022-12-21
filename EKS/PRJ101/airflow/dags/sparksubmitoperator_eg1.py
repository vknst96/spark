import airflow
from airflow import DAG
from airflow.configuration import conf
from datetime import datetime, timedelta
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

default_args = {
   'owner': 'airflow',
   'depends_on_past': False,
   'retry_delay': timedelta(minutes=5),
   'start_date': datetime(2021, 2, 20),
   'provide_context': True
}

dag_path = '/home/ubuntu/airflow/dags/'

aws_region = 'us-east-1'

k8s_ca_crt_path = '/home/ubuntu/caCertfile'
k8s_sa_token_path = '/home/ubuntu/secToken'


with DAG(
        dag_id='sparkSubmitOperator_dag',
        default_args=default_args,
        schedule_interval='@once'
) as dag:
    podRun = SparkSubmitOperator(
        task_id='sparkSubmitOperator_tsk',
        conn_id='spark-eks', # Set connection details in the airflow connections.
        application='local:///opt/spark/work-dir/main.py',
        py_files='local:///opt/spark/work-dir/functions.py',
        name='spark-on-eks-example',
        conf={
            'spark.driver.memory': '2G',
            'spark.executor.memory': '2G',
            'spark.executor.cores': '1',
            'spark.sql.shuffle.partitions': '20',
            'spark.kubernetes.allocation.batch.size': '10',
            'spark.kubernetes.container.image': 'vknstudy96/pyspark-app:v1',
            'spark.kubernetes.container.image.pullPolicy': 'Always',
            'spark.kubernetes.authenticate.driver.serviceAccountName': 'spark',
            'spark.kubernetes.namespace': 'spark',
            'spark.kubernetes.driver.label.spark/app': 'spark-eks',
            'spark.kubernetes.executor.label.spark/app': 'spark-eks',
            'spark.kubernetes.driver.label.spark/component': 'driver',
            'spark.kubernetes.executor.label.spark/component': 'executor',
            'spark.kubernetes.node.selector.noderole': 'spark',
            'spark.hadoop.fs.s3.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
            'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
            'spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a': 'org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory',
            'spark.hadoop.fs.s3a.committer.name': 'magic',
            'spark.hadoop.fs.s3a.committer.magic.enabled': 'true',
            'spark.kubernetes.node.selector.topology.kubernetes.io/zone': '{}a'.format(aws_region),
            'spark.kubernetes.driver.podTemplateFile': '/home/ubuntu/project/driver-pod-k8s.yaml',
            'spark.kubernetes.executor.podTemplateFile': '/home/ubuntu/project/executor-pod-k8s.yaml',
            'spark.hadoop.fs.s3a.aws.credentials.provider': 'com.amazonaws.auth.WebIdentityTokenCredentialsProvider',
            'spark.kubernetes.authenticate.submission.caCertFile': k8s_ca_crt_path,
            'spark.kubernetes.authenticate.submission.oauthToken': k8s_sa_token_path,
            'spark.kubernetes.file.upload.path': 's3a://mysourcecodebkt/dynamic/'
            # 'spark.kubernetes.authenticate.submission.oauthToken': secret_token
        },
        verbose=True,
        application_args=['s3a://mysourcecodebkt/sourcedata/Restaurants_in_Wake_County.csv','s3a://mysourcecodebkt/sourcedata/Restaurants_in_Durham_County_NC.json'],
    )
