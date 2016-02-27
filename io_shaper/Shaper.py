#!/usr/local/bin/python2.7
import sys,os
import time
from Buffer import Buffer
import pandas

class Shaper():

    def __init__(self,config):
        self.myBuffer = Buffer(config)
        self.out_csv = ''
        self.in_io_count = 0
        self.out_io_count = 0

    def read_csv(self,in_csv):
        colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
        data = pandas.read_csv(in_csv,names = colnames)
        data_dir = data.D.tolist()
        data_addr = map(lambda x: x//8, data.BLOCK.tolist())
        data_size = map(lambda x: x//4096, data.SIZE.tolist())
        arrs = []
        length = len(data_dir)
        self.in_io_count = length
        self.start_time = time.time()
        for i in range(0,length):
            arrs.append([data_dir[i],data_addr[i],data_size[i]])
        return arrs

    def run(self,in_csv,out_csv):
        arrs = self.read_csv(in_csv)
        self.out_csv = out_csv
        for each in arrs:
            if each[0]=='W':
                #TODO: big file, dont put into cache, need to invalidate cache hit
                if self.myBuffer.add([each[1],each[1]+each[2]]):
                    print "-"
                    pass
                else:
                    print "+"
                    ios = self.myBuffer.get_cold()
                    self.gen_write_io(ios)
            else:
                #TODO: check cache hit
                ios = [[each[1],each[2]]]
                self.gen_read_io(ios)

        #clear all data in Buffer
        ios = self.myBuffer.get_all();

    def gen_write_io(self,ios):
        for each in ios:
            self.write_csv(each)

    def gen_read_io(self,ios):
        for each in ios:
            self.write_csv(each)

    def write_csv(self,item):
        pass

    def print_io_count(self):
        print "=========================================================="
        print "I/O count before optimization:", self.in_io_count
        print "I/O count after optimization:", self.out_io_count
        print "=========================================================="




if __name__ == '__main__':

    myShaper = Shaper({
        'capacity': 1000,
        'full_watermark': 0.85,
        'hot_watermark': 4
    })
    myShaper.run('../logs/io.csv','../logs/optimize.csv')
    myShaper.print_io_count()
