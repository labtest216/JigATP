
# Manual install:
# 1. Install python.
# 2. Install mongodb server: https://www.mongodb.com/download-center/community?initial=true
# 3. Install AVbin10-win64 for microphone test
# 4. Install ActiveTcl: https://www.activestate.com/products/activetcl/downloads/
# 4. Start mongo server on command line: mongod.
# 5.
# 6.


# Auto install:
import pymongo
import os
import time

from Setup.cfg_setup import *


def set_environment_var():
    os.system('PATH %PATH%;' + mongo_env)
    time.sleep(1)
    os.system('PATH %PATH%;' + python_env)


# Install pip.
def install_pip():
    os.system("python D:\\Projects\\JigATP\\Jig\\Setup\\pipinstall.py")
y

# Install python project packages.
class InstallPythonPackages:
    password = ' '

    py_packages = ['pip install pymongo',
                   'pip install schedule',
                   'pip install pyserial',
                   'pip install pyglet',
                   'pip install -U matplotlib'
                   'pip install panda',
                   'pip install swampy',
                   'pip install PyDAQmx',
                   'pip install PyBluez-win10']

    od_packages = ['sudo apt-get install device-tree-compiler i2c-tools',
                    'sudo apt-get install python-smbus',
                    'sudo apt-get install -y i2c-tools',
                   'sudo -H pip install esptool',
                   'sudo apt-get install python3-pip',
                   'sudo apt-get install python-pip'
                   ]

    def start(self, packages):
        for pack in packages:
            print('Out put for ' + str(pack) + ':')
            debug = os.system(pack)
            time.sleep(2)
            print('return=' + str(debug))
            print('\n\n\n')


def config_mongo_db():

    # Create \C:\data\db folders.
    if not os.path.isdir("C:\\data"):
        os.mkdir("C:\\data")
        os.mkdir("C:\\data\\db")
    # Create connection with mongo client.
    ATP_DB = pymongo.MongoClient("mongodb://localhost:27017/")
    # Create db.
    report = ATP_DB["test_reports"]
    # Print db and collections
    dblist = ATP_DB.list_database_names()
    collist = report.list_collection_names()
    print(dblist)
    print(collist)


# Start install:
set_environment_var()
install_pip()
InstallPythonPackages().start()
