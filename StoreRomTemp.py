#!/usr/bin/python3

########################################################################
# Filename    : StoreRomTemp.py
# Description : Script to store the rom temp to remote database
# Author      : Gjengedal
# modification: 07.06.2017
########################################################################

import os
import glob
import time
import mysql.connector
from mysql.connector import errorcode

class Tempratures():
    def __init__(self):

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.temp = 22.1
        try:
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'
        except IndexError:
            print("INFO: unable to read Linux-path")
    def connect_to_DB(self):
        try:
            config = {
                'user': 'smart_mirror',
                'password': 'legobil',
                'host': '192.168.11.8',
                'database': 'Tempratures',
                'raise_on_warnings': True,
            }
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            #self.cnx.close()
            print("Connected to database")
    def insert_to_DB(self):
        try:
            cursor = self.cnx.cursor()
            add_temprature = ("INSERT INTO Hallway "
                              "(temprature) "
                              "VALUES (%s)" %self.temp)
            # Insert new temprature
            cursor.execute(add_temprature)
            #emp_no = cursor.lastrowid
            # Make sure data is committed to the database
            self.cnx.commit()
            cursor.close()
        except:
            print("Cannot insert, no connection to database, connecting...")
            self.connect_to_DB()
            print("Retrying insert in 5 minutes")
    def read_temp_raw(self):
        try:
            f = open(self.device_file, 'r')
            lines = f.readlines()
            f.close()
        except AttributeError:
            print("INFO: Not able to read temperature. Mocks lines instead")
            lines = ['aa 01 4b 46 7f ff 06 10 84 : crc=84 YES', 'aa 01 4b 46 7f ff 06 10 84 t=26625']
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            #time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)
            return '{:.1f}'.format( float(temp_c)/1000 )

    def update(self):

        try:
            self.temp = self.read_temp()
        except NameError:
            print("INFO: Unable to read temperatures")
            self.temp = 22.1

if __name__ == '__main__':
    app = Tempratures()
    app.connect_to_DB()
    while True:
        app.update()
        app.insert_to_DB()
        time.sleep(300)



