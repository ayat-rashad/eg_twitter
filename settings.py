import os

APP_NAME = 'EG_twitter'
FILESYSTEM = 'file://'
APP_HOME = os.environ['HOME'] + '/eg_twitter'
STANFORD_SEGMENTER = APP_HOME + '/stanford_segmenter'
STANFORD_POSTAGGER = APP_HOME + '/stanford-postagger'
STANFORD_MODELS = STANFORD_POSTAGGER + '/models'
LOG_DIR = 'log'
 
