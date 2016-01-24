from pyspark import SparkContext, SparkConf
import pymongo_spark
import os

APP_NAME = 'EG_twitter'
FILESYSTEM = 'file'
APP_HOME = os.environ['HOME'] + '/eg_twitter2'

ENV_VARS = {'PYSPARK_PYTHON': "/usr/bin/python2.7", 'PYSPARK_DRIVER_PYTHON': "/usr/bin/python2.7"}
PY_FILES = ['settings.py', 'stanford_segmenter.py', 'pos_tag.py', 'logger.py', 'pymongo_spark.py']
FILES = ['NER.model']
CONF = {'spark.driver.extraClassPath':
        os.environ['HOME'] + 'mongo-hadoop/spark/build/libs/mongo-hadoop-spark.jar'}

STANFORD_SEGMENTER = APP_HOME + '/stanford_segmenter'
STANFORD_POSTAGGER = APP_HOME + '/stanford-postagger'
STANFORD_MODELS = STANFORD_POSTAGGER + '/models'

LOG_DIR = 'log'

MONGO_SERVER = 'localhost'
MONGO_PORT = 27017
DB = 'tweets_data'

### Prepare SparkContext ###
conf = SparkConf().setAppName(APP_NAME)

for prop, val in CONF.items():          #set configuration properties
    conf.set(prop, val)         

sc = SparkContext(conf=conf, environment=ENV_VARS)

for f in PY_FILES:          #add dependencies
    sc.addPyFile('%s://%s/%s' %(FILESYSTEM, APP_HOME, f))

for f in FILES:          #add required files
    sc.addFile('%s://%s/%s' %(FILESYSTEM, APP_HOME, f))
    
pymongo_spark.activate()
