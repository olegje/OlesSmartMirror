#!/usr/bin/env python
########################################################################
# Filename    : Mirrorbuttons.py
# Description : Controlling the connection to database
# Author      : Gjengedal
# modification: 18.10.2017
########################################################################


import os
import glob
import time
import logging
import logging.config
import mysql.connector
from mysql.connector import errorcode

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('rotatingLogger')

class Tempratures():
    def __init__(self):
        logger.debug('Tempratures initialized')

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.temp = 22.1
        try:
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'
        except IndexError:
            logger.info("unable to read Linux-path")
    def connect_to_DB(self):
        try:
            config = {
                'user': 'PI_Mirror',
                'password': 'mirror',
                'host': '192.168.12.8',
                'database': 'Tempratures',
                'raise_on_warnings': True,
            }
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
            else:
                logger.error(err)
        else:
            #self.cnx.close()
            logger.info("Connected to database")
    def insert_to_DB(self):
        try:
            cursor = self.cnx.cursor()
            add_temprature = ("INSERT INTO Outdoor"
                              "(temprature) "
                              "VALUES (%s)" %self.temp)
            # Insert new temprature
            cursor.execute(add_temprature)
            #emp_no = cursor.lastrowid
            # Make sure data is committed to the database
            self.cnx.commit()
            cursor.close()
            logger.info('Temprature inserted')
        except:
            logger.warning("Cannot insert, no connection to database, connecting...")
            self.connect_to_DB()
            logger.info("Retrying insert in 5 minutes")
    def read_temp_raw(self):
        try:
            f = open(self.device_file, 'r')
            lines = f.readlines()
            f.close()
        except AttributeError:
            logger.info("Not able to read temperature. Mocks lines instead")
            lines = ['aa 01 4b 46 7f ff 06 10 84 : crc=84 YES', 'aa 01 4b 46 7f ff 06 10 84 t=26625']
        return lines

    def read_room_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            #time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)
            return '{:.1f}'.format( float(temp_c)/1000 )
    def get_cpu_temp(self):     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
        #tmp = open(r"/sys/class/thermal/thermal_zone0/temp")
        try:
            tmp = open('/sys/class/thermal/thermal_zone0/temp')
            cpu = tmp.read()
            tmp.close()
        except IOError:
            logger.info("INFO: Not able to open file. Mocks lines instead")
            cpu = 66666
        
        return '{:.1f}'.format( float(cpu)/1000 )
    def update(self):

        try:
            self.temp = self.read_temp()
        except NameError:
            logger.warning("Unable to read temperatures, using mock up as 22.1")
            self.temp = 22.1

if __name__ == '__main__':
    logger.info('Script started as main')
    
