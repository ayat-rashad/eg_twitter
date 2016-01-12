
#!/bin/bash

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py 
python2.7 ez_setup.py
easy_install-2.7 pip

yum -y install geos build-essential python27-devel libatlas-dev libatlas3gf-base
pip2.7 install -r ~/eg_twitter/requirements.txt

echo "export PYSPARK_PYTHON=/usr/bin/python2.7" >> ~/spark/conf/spark-env.sh
echo "export PYSPARK_DRIVER_PYTHON=python2.7" >> ~/spark/conf/spark-env.sh

#install Java 8
yum -y install java-1.8.0-openjdk*
rm /usr/lib/jvm/java
ln -s /etc/alternatives/jre_1.8.0 /usr/lib/jvm/java


#install MongoDB
echo "[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.2/x86_64/
gpgcheck=0
enabled=1" > /etc/yum.repos.d/mongodb-org-3.2.repo

yum install -y mongodb-org

service mongod start

#install mongo-hadoop
git clone https://github.com/mongodb/mongo-hadoop.git
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
cd mongo-hadoop
./gradlew jar

cd spark/src/main/python
python2.7 setup.py install