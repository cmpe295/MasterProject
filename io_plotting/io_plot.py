'''
Created on Oct 25, 2015

@author: dyao
'''

import json
from matplotlib import pyplot
from parse_io import parse_iosnoop
from constants import TYPE_TIME2BLOCK, TYPE_TIME2SIZE
from constants import TYPE_BLOCK2SIZE

def io_barchart(io_data, type):
    
    if type == TYPE_TIME2BLOCK:
        x = [item['TIME'] for item in io_data]
        y = [item['BLOCK'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('time (us)')
        pyplot.ylabel('block address (block#)')
        pyplot.title('time vs address')
        #pyplot.legend()
        pyplot.show()
    elif type == TYPE_TIME2SIZE:
        x = [item['TIME'] for item in io_data]
        y = [item['SIZE'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('time (us)')
        pyplot.ylabel('size (byte)')
        pyplot.title('time vs size')
        #pyplot.legend()
        pyplot.show()
    elif type == TYPE_BLOCK2SIZE:
        x = [item['BLOCK'] for item in io_data]
        y = [item['SIZE'] for item in io_data]
        pyplot.bar(x, y)
        pyplot.xlabel('block (block#)')
        pyplot.ylabel('size (byte)')
        pyplot.title('block vs size')
        #pyplot.legend()
        pyplot.show()


    
    

if __name__ == '__main__':
    '''
    16852021303    16852021485      501   378 W 37241704   4096 iStat Menus Stat ??/databases/iStatMenusStatus.db
    16818242122    16818242345      501   565 W 28586352   4096     Safari ??/LocalStorage/https_www.youtube.com_0.localstorage-journal
    '''
    
    io_data = parse_iosnoop(0, './logs/io.log')
    print len(io_data)
    
    print json.dumps(io_data, indent=4)
    
    #io_barchart(io_data, type=TYPE_TIME2SIZE)
    #io_barchart(io_data, type=TYPE_TIME2BLOCK)
    io_barchart(io_data, type=TYPE_BLOCK2SIZE)
