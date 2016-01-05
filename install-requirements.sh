
#!/bin/bash

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py 
python2.7 ez_setup.py
easy_install-2.7 pip

yum -y install geos build-essential python27-devel libatlas-dev libatlas3gf-base
pip2.7 install -r ~/eg_twitter/requirements.txt

echo "PYSPARK_PYTHON=/usr/bin/python2.7" >> ~/spark/conf/spark-env.sh
echo "PYSPARK_DRIVER_PYTHON=python2.7" >> ~/spark/conf/spark-env.sh

yum -y install java-1.8.0
rm /usr/lib/jvm/java
ln -s /etc/alternatives/jre_1.8.0 /usr/lib/jvm/java

