#!/usr/local/bin/python2.7
#from scipy import stats
import numpy as np
import csv

class Gen():
    def __init__(self, config):    
        self.config = config
        self.output = []
        self.done_count = 0
        self.addr_range = np.arange(self.config['range'][0],self.config['range'][1],1)
        self.cur_dir = 'W'
        self.cur_addr = 0
        self.cur_size = 4*1024;
        self.dir_arr = ['W','R']
        self.write_size_arr = [4*1024, 4*1024, 512*1024, 1024*1024]    #put this as input configuration
        self.read_size_arr  = [4*1024, 4*1024, 512*1024, 1024*1024]     #put this as input configuration
        self.seq_length_arr =     [20, 40, 60, 80, 100,200,300,400]
        self.seq_length_percent = [0.3,0.3,0.2,0.2,0.0,0.0,0.0,0.0]
        self.cur_seq = False
        self.seq_threshold = 512*1024
        self.block_size = 512
        self.read_seq_len_factor = 0
        self.write_seq_len_factor = 0
        self.done_write_seq_cnt = 0;
        self.done_write_ran_cnt = 0;
        self.done_read_seq_cnt = 0;
        self.done_read_ran_cnt = 0;
        self.output_file = './output/gen.csv'
        for i in range(0,len(self.seq_length_arr)):
            self.read_seq_len_factor += self.seq_length_arr[i]*self.seq_length_percent[i]
        for i in range(0,len(self.seq_length_arr)):
            self.write_seq_len_factor += self.seq_length_arr[i]*self.seq_length_percent[i]

    #percent is write percent
    def gen_dir(self,write_percent):
        if write_percent > 1 or write_percent < 0:
            print "ERROR input: write_percent:", write_percent
            return '-'
        else:
            self.cur_dir = np.random.choice(self.dir_arr,1,p=[write_percent,1-write_percent])[0]
            return self.cur_dir;

    def gen_addr(self):
        self.cur_addr =  np.random.choice(self.addr_range,1)[0]
        return self.cur_addr

    def gen_size(self):
        size_arr = []
        ran_percent = 0;
        percent1 = 0;
        percent2 = 0;
        percent3 = 0;
        percent4 = 1;
        if self.cur_dir == 'W':
            size_arr = self.write_size_arr
            write_seq_percent_factor =  self.config['write_ran_percent']*self.write_seq_len_factor
            ran_percent = write_seq_percent_factor/(1-self.config['write_ran_percent']+write_seq_percent_factor)
            percent1 = float(ran_percent)*3/4;
            percent2 = float(ran_percent)/4;
            percent3 = float(1-ran_percent)/3;
            percent4 = 1 - (percent1 + percent2 + percent3)
        else:
            size_arr = self.read_size_arr
            read_seq_percent_factor =  self.config['read_ran_percent']*self.read_seq_len_factor
            ran_percent = read_seq_percent_factor/(1-self.config['read_ran_percent']+read_seq_percent_factor)
            #ran_percent = self.config['read_ran_percent']
            percent1 = float(ran_percent)*2/3;
            percent2 = float(ran_percent)/3;
            percent3 = float(1-ran_percent)/2;
            percent4 = 1 - (percent1 + percent2 + percent3)

        self.cur_size = np.random.choice(size_arr,1,p=[percent1,percent2,percent3,percent4])[0]
        self.cur_seq = self.cur_size >= self.seq_threshold
        return self.cur_size

    #generate items(array):
    # (1)if random: generate items with only one element
    # (2)if sequence: generate multiple I/O
    def gen_items(self):
        items = []
        #start sequential IO
        if self.cur_seq:
            self.cur_seq = False
            length = np.random.choice(self.seq_length_arr,1,p=self.seq_length_percent)[0]
            for i in range(0,length):
                item = (self.cur_dir,
                        self.cur_addr + self.cur_size/self.block_size,
                        self.cur_size
                        )
                self.done_count += 1
                items.append(item)
                self.cur_addr += int(self.cur_size/self.block_size);

                
                if self.cur_dir=='W':
                    self.done_write_seq_cnt +=1;
                if self.cur_dir=='R':
                    self.done_read_seq_cnt +=1;
        
        #another dice to decide random or sequential I/O
        else:
            item = (self.gen_dir(self.config['write_percent']),
                    self.gen_addr(),
                    self.gen_size()
                    )
            self.done_count += 1
            items.append(item)

            if self.cur_dir=='W':
                if self.cur_size >= self.seq_threshold:
                    self.done_write_seq_cnt += 1
                else:
                    self.done_write_ran_cnt += 1;
            if self.cur_dir=='R':
                if self.cur_size >= self.seq_threshold:
                    self.done_read_seq_cnt += 1
                else:
                    self.done_read_ran_cnt += 1;

        return items;

    def write_csv(self,items,file):
        out_csv = open(file,'wb')
        content_list = []
        for item in items:
            csv_row = ['-','-',0,0,0,0,0,'hadoop','bin/spark']
            csv_row[4] = item[0]
            csv_row[5] = item[1]
            csv_row[6] = item[2]
            content_list.append(csv_row) 
        csv_writer = csv.writer(out_csv)
        csv_writer.writerows(content_list)

    #generate the final array
    def gen(self):
        while self.done_count < self.config['count']:
            item = self.gen_items()
            self.output.extend(item)
        self.write_csv(self.output,self.output_file)
        self.print_done_cnt()
        

    def print_done_cnt(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "I/O count:", self.done_count
        print "final percentage of write", float(self.done_write_seq_cnt + self.done_write_ran_cnt)/self.config['count']
        if self.done_write_ran_cnt + self.done_write_seq_cnt:
            print "final percentage of write random:", float(self.done_write_ran_cnt)/(self.done_write_seq_cnt+self.done_write_ran_cnt)
        if self.done_read_ran_cnt + self.done_read_seq_cnt:
            print "final percentage of read random:", float(self.done_read_ran_cnt)/(self.done_read_seq_cnt+self.done_read_ran_cnt)
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


if __name__ == '__main__':
  
    myGen = Gen({
        'range': (1,21111),
        'count': 100,
        'write_percent': 0.6,
        'write_ran_percent': 0.5,
        'read_ran_percent': 0.9
    })
    myGen.gen()
    print myGen.output

    #for v in myGen.output:
        #print v
    #myGen.print_done_cnt()
