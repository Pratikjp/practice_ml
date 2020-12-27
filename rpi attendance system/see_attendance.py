import os
import numpy as np
import time
"""
This script allows to see the attendance for a provided date.
it lists the attendance by subject.
"""
import MySQLdb
from datetime import datetime
import datetime

def validate(dat):
    try:
        datetime.datetime.strptime(dat,'%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")
    
def read_from_db():
    try:
        queryy="SELECT Subject, Present, Absent FROM attendance_sys WHERE date='%s'" % dat
        c.execute(queryy)
        result = c.fetchall()

        if result :
            for i in range(0,len(result)):
                subject=result[i][1]
                present=result[i][2]
                absent=result[i][3]
            print "%s" % subject
            print "%s" % present
            print "%s" % absent
        else:
            print "No record found"
            
    except:
        print "read error"
        
def main():
    read_from_db()

if __name__ == '__main__':
	dat = raw_input("Enter date:")
	validate(dat)
    try:
        db = MySQLdb.connect("localhost","root","asd","attendance")
        c= db.cursor()
    except:
        print ("error connecting to database")
             
    try:
      main()
    except KeyboardInterrupt:
      print ("bye bye...")
      pass    
