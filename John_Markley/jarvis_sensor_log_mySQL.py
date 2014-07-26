#!/usr/bin/env python

import MySQLdb
import datetime
import sys

now = datetime.datetime.now()

sensorIndex = sys.argv[1]
sensorValue = sys.argv[2]
sensorUoM  = sys.argv[3]
sensorRaw = sys.argv[4]
sensorDateTime = now.strftime("%Y/%m/%d %H:%M:%S.%f")
print(sensorIndex, sensorValue, sensorUoM, sensorRaw, sensorDateTime)
db = MySQLdb.connect("localhost", "root", "raspberry", "jarvis")
curs=db.cursor()
try:
    curs.execute ("INSERT INTO `jarvis`.`sensorLogs` (`logIndex`, `sensorIndex`, `sensorValue`, `sensorUoM`, `sensorRaw`, `sensorDateTime`) VALUES (NULL, '" + sensorIndex + "', '" + sensorValue + "', '" + sensorUoM + "', '" + sensorRaw  + "', '" + sensorDateTime + "')")
    curs.execute ("UPDATE `jarvis`.`sensorList`  SET  `sensorUpdatedAt` =  '" + sensorDateTime + "' WHERE  `sensorList`.`sensorIndex` = 115 ")
    db.commit()
    print "Data committed"
    print "New entry to sensorLog"
    print "Sensor data last update set"
except:
    print "Error: the database is being rolled back"
    db.rollback()
