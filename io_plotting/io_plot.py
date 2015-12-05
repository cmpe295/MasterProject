'''
Created on Oct 25, 2015

@author: dyao
'''

import json
from matplotlib import pyplot
from parse_io import parse_iosnoop
from constants import TYPE_TIME2BLOCK, TYPE_TIME2SIZE
from io_plotting.constants import TYPE_BLOCK2SIZE

def io_barchart(io_data, type):
    
    if type == TYPE_TIME2BLOCK:
        process_name = str(io_data[0]['PATHNAME']).lstrip("?")
        x = [item['TIME'] for item in io_data]
        y = [item['BLOCK'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('time (us)')
        pyplot.ylabel('block address (block#)')
        pyplot.title('Time vs Address: \nporcess: '+process_name)
        #pyplot.legend()
        pyplot.show()
    elif type == TYPE_TIME2SIZE:
        process_name = str(io_data[0]['PATHNAME']).lstrip("?")
        x = [item['TIME'] for item in io_data]
        y = [item['SIZE'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('time (us)')
        pyplot.ylabel('size (byte)')
        pyplot.title('Time vs Size: \nprocess: ' \
                     +process_name)
        #pyplot.legend()
        pyplot.show()
    elif type == TYPE_BLOCK2SIZE:
        process_name = str(io_data[0]['PATHNAME']).lstrip("?")
        x = [item['BLOCK'] for item in io_data]
        y = [item['SIZE'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('block (block#)')
        pyplot.ylabel('size (byte)')
        pyplot.title('Block vs Size: \nprocess: '+process_name)
        #pyplot.legend()
        pyplot.show()


    
    

if __name__ == '__main__':
    '''
    16852021303    16852021485      501   378 W 37241704   4096 iStat Menus Stat ??/databases/iStatMenusStatus.db
    16818242122    16818242345      501   565 W 28586352   4096     Safari ??/LocalStorage/https_www.youtube.com_0.localstorage-journal
    '''
    
    io_data = parse_iosnoop(718, '/Users/dyao/Documents/workspace/MasterProject/io_plotting/testlog/iosnoop.log')
    print len(io_data)
    
    print json.dumps(io_data, indent=4)
    
    #io_barchart(io_data, type=TYPE_TIME2SIZE)
    #io_barchart(io_data, type=TYPE_TIME2BLOCK)
    io_barchart(io_data, type=TYPE_BLOCK2SIZE)