
# import libraries
import os
import sys
import subprocess
from string import punctuation
import unicodedata

import pandas as pd
import numpy as np

import time
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from numerize.numerize import numerize
from scipy import stats

import requests

import json
import multiprocessing
import re
from unidecode import unidecode
from operator import add

from functools import reduce
from itertools import chain

from pyarrow import fs
import pyarrow.parquet as pq

import warnings
warnings.filterwarnings('ignore')

os.environ['HTTP_PROXY'] = "http://proxy.hcm.fpt.vn:80"
os.environ['HTTPS_PROXY'] = "http://proxy.hcm.fpt.vn:80"

os.environ['HADOOP_CONF_DIR'] = "/etc/hadoop/conf/"
os.environ['JAVA_HOME'] = "/usr/jdk64/jdk1.8.0_112"
os.environ['HADOOP_HOME'] = "/usr/hdp/3.1.0.0-78/hadoop"
os.environ['ARROW_LIBHDFS_DIR'] = "/usr/hdp/3.1.0.0-78/usr/lib/"
os.environ['CLASSPATH'] = subprocess.check_output("$HADOOP_HOME/bin/hadoop classpath --glob", shell=True).decode('utf-8')

hdfs = fs.HadoopFileSystem(host="hdfs://hdfs-cluster.datalake.bigdata.local", port=8020)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)

# import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession

from pyspark.sql import functions as F

from pyspark.sql import DataFrame
from typing import Iterable

from pyspark.sql.window import Window

def initial_spark(spark_name='demo', mode='local[16]', driver_memory='20g', max_worker=1):
    
    # for yarn support
    os.environ['SPARK_HOME']="/opt/spark/spark-3.0.2-bin-hadoop2.7/"
    # os.environ[
    #     "SPARK_HOME"
    # ] = "/opt/spark/spark-3.0.2-bin-hadoop2.7-lineage/"  # Change SPARK_HOME to lineage
    os.environ['JAVA_HOME']="/usr/jdk64/jdk1.8.0_112/"
    os.environ['SPARK_CONF_DIR']= ''
    
    conf = SparkConf()
    
    # config spark application name
    conf.setAppName(spark_name)

    # config location for spark finding metadata from hive metadata server
    conf.set("hive.metastore.uris", "thrift://master01-dc9c14u40.bigdata.local:9083,thrift://master02-dc9c14u41.bigdata.local:9083")
    conf.set("spark.sql.hive.metastore.jars", "/opt/spark/spark-3.0.2-bin-hadoop2.7/*")

    # config in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes
    conf.set("spark.kryoserializer.buffer.max", "2000")
    conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    conf.set("spark.sql.execution.arrow.enabled", "true")
    conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "10000")

    # config spark driver memory
    conf.set("spark.driver.memory", driver_memory)
    conf.set('spark.driver.maxResultSize', driver_memory)

    #set metastore.client.capability.check to false
    conf.set("hive.metastore.client.capability.check", "false")
    conf.set("spark.port.maxRetries", 100)
    conf.set("spark.jars","hdfs:///shared/jars/hotpot_2.12-0.0.3.jar")
    conf.set("spark.sql.redaction.string.regex",".{22}==")
    
    # config timezone
    conf.get('spark.sql.session.timeZone')
    conf.get("hive.metastore.uris")
    
    # config show pandas dataframe format on notebook
    conf.set("spark.sql.repl.eagerEval.enabled",True)
    conf.set("spark.sql.repl.eagerEval.truncate",200)
    conf.get("hive.metastore.uris")
    
    # config calendar
    conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead", "LEGACY")
    conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite", "LEGACY")

    # config yarn
    if mode == 'yarn':
        conf.set("spark.executor.memory", "12g")
        conf.set("spark.executor.cores", "4")
        conf.set("spark.dynamicAllocation.enabled", True)
        conf.set("spark.dynamicAllocation.initialExecutors", 1)
        conf.set("spark.dynamicAllocation.shuffleTracking.enabled", True)
        conf.set("spark.dynamicAllocation.minExecutors", 1)
        conf.set("spark.dynamicAllocation.maxExecutors", max_worker)
        conf.set("spark.dynamicAllocation.shuffleTracking.timeout", "3m")
        os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'
        os.environ['PYSPARK_PYTHON'] = './environment/bin/python'
        conf.set("spark.yarn.dist.archives", "hdfs:/shared/envs/trinhlk2-python37_env.tar.gz#environment")
        
    # config checkpoint
    conf.set("spark.cleaner.referenceTracking.cleanCheckpoints", "true")
    
    # config maxSize
    conf.set("spark.rpc.message.maxSize", 512)
    
    # initial spark
    spark = SparkSession.builder.config(conf=conf).master(mode).enableHiveSupport().getOrCreate()
    
    # decrypt
    spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fdecrypt","fdecrypt")
    spark.sql("use ftel_dwh_isc")
    
    # set checkpoint dir
    spark.sparkContext.setCheckpointDir('/data/fpt/ftel/cads/dep_solution/sa/dev/checkpoint')
    
    # set log level
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark

def rename_columns(df, columns):
    if isinstance(columns, dict):
        return df.select(*[F.col(col_name).alias(columns.get(col_name, col_name)) for col_name in df.columns])
    else:
        raise ValueError("'columns' should be a dict")
