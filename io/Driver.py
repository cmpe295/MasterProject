#!/usr/local/bin/python2.7
import sys,os
import time
import logging

class Driver():

    def __init__(self):
        self.target = ''
        self.dummy = bytearray(['2']*10000000)
        logging.basicConfig(level=logging.DEBUG)

    def open(self,target):
        self.target = target
        os.system('sudo diskutil unmountDisk ' + self.target)
        print self.target
        self.disk = file(self.target,'rb+')

    def close(self):
        self.disk.close()


    def read(self,addr,size):
        self.disk.seek(addr)
        os.fsync(self.disk)
        return self.disk.read(size)

    def write(self,addr,size):
        self.disk.seek(addr)
        self.disk.write(buffer(self.dummy,0,size))
        os.fsync(self.disk)

    def write_multi(self,arr):
        for each in arr:
            self.write(each[0],each[1])


    def drive(self,d,addr,size):
        self.disk.seek(addr)
        if(d=='W'):
            self.disk.write(buffer(self.dummy,0,size))
            logging.debug("(W)--->>>: addr: %d, size: %d",addr,size)
        else:
            self.disk.read(size)
            logging.debug("(R)<<<---: addr: %d, size: %d",addr,size)
        os.fsync(self.disk)


if __name__ == '__main__':
    myDriver = Driver()
    myDriver.open('/dev/disk2')
    arrs = [ ]
    for i in range (0,1000):
        arrs.append([0,512*80])

    start_time = time.time()
    myDriver.write_multi(arrs)
    end_time = time.time()
    print "time spent:", end_time - start_time
    myDriver.close()
