#!/usr/local/bin/python2.7
import sys,os
import time
from Driver import Driver
import pandas

class Wrapper():

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
        data_addr = data.BLOCK.tolist()
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
    myWrapper = Wrapper()
    myWrapper.open('./io.csv','/dev/disk2')
    myWrapper.run()
    print myWrapper.get_time()
