#!/usr/local/bin/python2.7
import sys,os
import time
from Driver import Driver
import pandas

class DiskDriver():

    def __init__(self):
        self.myDriver = Driver()
        self.data = ''
        self.start_time = 0
        self.end_time = -1
        self.total_time = -1

    def run(self):
        colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
        data = pandas.read_csv(self.data,names = colnames)
        data_dir = data.D.tolist()
        data_addr = map(lambda x: x*512, data.BLOCK.tolist())
        data_size = data.SIZE.tolist()
        arrs = []
        length = len(data_dir)
        self.start_time = time.time()
        for i in range(0,length):
            self.myDriver.drive(data_dir[i],data_addr[i],data_size[i])
        self.end_time = time.time()
        self.total_time = self.end_time - self.start_time
    
        self.myDriver.close()

    def open(self,data,target):
        self.myDriver.open(target)
        self.data = data

    def get_time(self):
        return self.total_time


if __name__ == '__main__':
    time_before = -1
    time_after = -1
    myDiskDriver = DiskDriver()
    myDiskDriver.open('./output/gen.csv','/dev/disk3')
    print "Start drive IO to disk:"
    myDiskDriver.run()
    time_before = myDiskDriver.get_time()

    myDiskDriver.open('./output/optimize.csv','/dev/disk3')
    print "Start drive IO to disk:"
    myDiskDriver.run()
    time_after = myDiskDriver.get_time()
    print "\n"
    print "*************************************************************************" 
    print "* Running time of './output/gen.csv' (before optimize):", time_before, "s"
    print "* Running time of './output/optimize.csv' (after optimize):", time_after, "s"
    print "*************************************************************************" 
    print "\n"

