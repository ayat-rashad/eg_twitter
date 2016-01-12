import os

APP_NAME = 'EG_twitter'
FILESYSTEM = 'file'
APP_HOME = os.environ['HOME'] + '/eg_twitter'

ENV_VARS = {'PYSPARK_PYTHON': "/usr/bin/python2.7", 'PYSPARK_DRIVER_PYTHON': "/usr/bin/python2.7"}
PY_FILES = ['settings.py', 'stanford_segmenter.py', 'pos_tag.py', 'logger.py']
CONF = {'spark.driver.extraClassPath',
        os.environ['HOME'] + 'mongo-hadoop/spark/build/libs/mongo-hadoop-spark.jar'}

STANFORD_SEGMENTER = APP_HOME + '/stanford_segmenter'
STANFORD_POSTAGGER = APP_HOME + '/stanford-postagger'
STANFORD_MODELS = STANFORD_POSTAGGER + '/models'

LOG_DIR = 'log'

MONGO_SERVER = 'localhost'
MONGO_PORT = '27017'
DB = 'tweets_data'
 
