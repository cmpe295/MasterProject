#!/usr/local/bin/python2.7
#from scipy import stats
import numpy as np
import csv
import pandas

class Statistics():
    def __init__(self, config):    
        self.config = config
        self.io_count = 0
        self.seq_read_size = 0
        self.seq_write_size = 0
        self.ran_read_count = 0
        self.ran_write_count = 0
        self.print_config()

    def read_csv(self,in_file):
        colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
        data = pandas.read_csv(in_file,names = colnames)
        data_dir = data.D.tolist()
        data_addr = map(lambda x: x//8, data.BLOCK.tolist())
        data_size = map(lambda x: x//4096, data.SIZE.tolist())
        arrs = []
        length = len(data_dir)
        for i in range(0,length):
            arrs.append([data_dir[i],data_addr[i],data_size[i]])
        return arrs

    def get_stats(self,arrs):
        self.io_count = len(arrs)
        for each in arrs:
            if each[0] == 'W':
                if each[2]<= 1:
                    self.ran_write_count += 1
                else:
                    self.seq_write_size += each[2]*4096
            else:
                if each[2]<= 1:
                    self.ran_read_count += 1
                else:
                    self.seq_read_size += each[2]*4096
        self.show_stats()

    def show_stats(self):
        print "input seq_write_size:", self.seq_write_size
        print "input seq_read_size:", self.seq_read_size
        print "input ran_write_count:", self.ran_write_count
        print "input ran_read_count:", self.ran_read_count
        print ""

    def run(self):
        arrs = self.read_csv(self.config['file'])
        self.get_stats(arrs)
        total_time = self.cal_time()
        print "Total time:", total_time

    def cal_time(self):
        #seq time
        return self.cal_seq_time() + self.cal_ran_time()

    def cal_seq_time(self):
        seq_write_time = float(self.seq_write_size)/self.config['hdd_seq_write']
        seq_read_time = float(self.seq_read_size)/self.config['hdd_seq_read']

        print "HDD seq write size:", self.seq_write_size
        print "HDD seq write time = hdd_seq_write_size/hdd_seq_write:", seq_write_time
        print "HDD seq read size:", self.seq_read_size
        print "HDD seq read time = hdd_seq_read_size/hdd_seq_read:", seq_read_time
        print ""

        return seq_write_time + seq_read_time

    def cal_ran_time(self):
        #assume ssd only save random data, no seq data
        #assuem 50% percent ssd is used to save write random data
        ssd_ran_write_count = min(self.ran_write_count,self.config['ssd_size']/4096)
        ssd_ran_write_time = float(ssd_ran_write_count)/self.config['ssd_ran_write']

        hdd_ran_write_count = self.ran_write_count - ssd_ran_write_count
        hdd_ran_write_time = float(hdd_ran_write_count)/self.config['hdd_ran_write']

        ssd_ran_read_count = self.ran_read_count * self.config['ssd_read_hit']
        ssd_ran_read_time = float(ssd_ran_read_count)/self.config['ssd_ran_read']

        hdd_ran_read_count = self.ran_read_count - ssd_ran_read_count
        hdd_ran_read_time = float(hdd_ran_read_count)/self.config['hdd_ran_read']

        print "SSD random write count:", ssd_ran_write_count
        print "SSD random write time = ssd_ran_write_count/ssd_write_iops:", ssd_ran_write_time
        print "HDD random write count:", hdd_ran_write_count
        print "HDD random write time = hdd_ran_write_count/hdd_write_iops:", hdd_ran_write_time
        print ""

        print "SSD random read count:", ssd_ran_read_count
        print "SSD random read time = ssd_ran_read_count/ssd_read_iops:", ssd_ran_read_time
        print "HDD random read count:", hdd_ran_read_count
        print "HDD random read time = hdd_ran_read_count/hdd_read_iops:", hdd_ran_read_time
        print ""

        return ssd_ran_write_time + ssd_ran_read_time + hdd_ran_write_time + hdd_ran_read_time




    def print_config(self):
        print ""
        print ""
        print ""
        print "***************************************************"
        print "Input config for Statistics:"
        print self.config
        print ""
    
if __name__ == '__main__':
  
    myStat = Statistics({
        'file'          : './output/gen.csv',
        'ssd_size'      : 200*1024*1024,        #Shrink from 200GB to 200MB because IO count has been shrinked 
        'ssd_seq_write' : 450*1024*1024,
        'ssd_seq_read'  : 500*1024*1024,
        'ssd_ran_write' : 100*1000,
        'ssd_ran_read'  : 130*1000,
        'ssd_read_hit'   : 0.91,                #cache hit for random read
        'ssd_write_percent'   : 0.5,            #how much space can be treated as buffer to save random write
        'hdd_seq_write' : 450*1024*1024,
        'hdd_seq_read'  : 500*1024*1024,
        'hdd_ran_write' : 200,
        'hdd_ran_read'  : 200
    })
    myStat.run()
