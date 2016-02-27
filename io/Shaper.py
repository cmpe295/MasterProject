#!/usr/local/bin/python2.7
import sys,os
import time
from Buffer import Buffer
import pandas
import csv

class Shaper():

    def __init__(self,config):
        self.myBuffer = Buffer(config)
        self.out_csv = ''
        self.in_io_count = 0
        self.out_io_count = 0
        self.csv_row = ['-','-',0,0,0,0,0,'hadoop','bin/spark']

    def read_csv(self,in_file):
        colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
        data = pandas.read_csv(in_file,names = colnames)
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

    def run(self,in_file,out_file):
        arrs = self.read_csv(in_file)
        self.out_csv = open(out_file,'wb')
        for each in arrs:
            if each[0]=='W':
                #TODO: big file, dont put into cache, need to invalidate the data in cache if cache hit
                if self.myBuffer.add([each[1],each[1]+each[2]]):
                    pass
                else:
                    ios = self.myBuffer.get_cold()
                    self.gen_write_io(ios)
            else:
                #TODO: check cache hit, if hit, return data immediately instead of generate read io
                ios = [[each[1],each[2]]]
                self.gen_read_io(ios)

        #clear all data in Buffer
        ios = self.myBuffer.get_all();

    def gen_write_io(self,ios):
        for each in ios:
            self.write_csv(['W',each[0],each[1]])

    def gen_read_io(self,ios):
        for each in ios:
            self.write_csv(['R',each[0],each[1]])

    def write_csv(self,item):
        content_list = []
        self.csv_row[4] = item[0]
        self.csv_row[5] = item[1]*8
        self.csv_row[6] = item[2]*4096
        content_list.append(self.csv_row) 
        csv_writer = csv.writer(self.out_csv)
        csv_writer.writerows(content_list)

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
    myShaper.run('./output/gen.csv','./output/optimize.csv')
    myShaper.print_io_count()
