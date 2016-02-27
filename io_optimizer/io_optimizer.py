import copy
import json
from collections import OrderedDict

# this object represents the optimized disk IO
#    - whenever read from or write to disk, this object will be appended
IO_ORIG = []
IO_DISK = []
IO_BUFFER = []

BUFFER = []
BUFF_SIZE = 5

__COST_R_RAW = 10
__COST_W_RAW = 20

__COST_R_BUF = 1
__COST_W_BUF = 2

_CostPreoptm = 0
_CostPostoptm = 0


__DEBUG = False
__VERBOSE = False

def read_input(io_log):
    io_obj = open(io_log).read().split('\n')
    ret = []
    for line in io_obj:
        try:
            ret.append({'ts' : line.split(',')[1],
                        'rw' : line.split(',')[4],
                        'addr' : line.split(',')[5],
                        'size' : line.split(',')[6],
                        })
        except:
            print 'skipping'
            continue
        
    #print json.dumps(ret, indent=4)
    return ret

def dump_buff_algo1():
    '''
    optimization algo 1
        - whenever buffer gets full, execute this algorighm and dump write ios from buffer to disk
        - this algorithm detects the in-buffer IO entries
            - sort the address in increasing mannar and write to disk  (assuming this will reduce the IO cost)
        
    initial design is to run this as a thread
    
    @return: (cost, buff_new, todisk)
    '''
    AVGCOST_W_SEQADDR = 4
    
    buff_new = []
    todisk = sorted(BUFFER, key=lambda item : item['addr'])
    cost_delta = AVGCOST_W_SEQADDR * len(BUFFER)
    
    return cost_delta, buff_new, todisk

            
def dump_buff_algo2():
    '''
    if address covers consecutive blocks, combine the multiple write into a single write
        - consider special case of slotted missing blocks (read such blocks to fill the missing and do a single write)
    '''
    __threshold = BUFF_SIZE/10
    __cost_per_dump = 1
    
    cost_delta = 0
    buff_new = copy.deepcopy(BUFFER)
    todisk = []
    
    left=right=0
    for right in range(len(BUFFER)):
        if right == 0:
            continue
        else:
            if int(BUFFER[right]['addr'])-int(BUFFER[right-1]['addr'])==1:
                if right == len(BUFFER)-1:
                    if right-left >= __threshold:
                        todisk += BUFFER[left:right+1]
                        for i in range(left, right+1):
                            buff_new[i] = None
                        cost_delta += __cost_per_dump
            else:
                if right-left >= __threshold:
                    todisk += BUFFER[left:right]
                    for i in range(left, right):
                        buff_new[i] = None
                    cost_delta += __cost_per_dump
                left=right
    temp = []
    for item in buff_new:
        if item != None:
            temp.append(item)
    buff_new = temp
    
    return cost_delta, buff_new, todisk

        


def get_cost_preopt(io_obj):
    cost = 0
    for item in io_obj:
        if item['rw'] == 'R':
            cost += __COST_R_RAW
        elif item['rw'] == 'W':
            cost += __COST_W_RAW
            
    return cost

def buffer_write_item(item):
    global BUFFER
    global IO_DISK
    global _CostPostoptm
    
    if len(BUFFER) < BUFF_SIZE:
        dbg('buffer write: NOT FULL (item: %s | buff_len: %s)' % (item, len(BUFFER)))  
        BUFFER.append(item)     # TODO: may need to improve: if write to the same location, overwrite the existing one
        IO_BUFFER.append(item)
        _CostPostoptm += __COST_W_BUF
    else:
        # save item to disk and dump buffer
        dbg('buffer write: FULL (item: %s | buff_len: %s)' % (item, len(BUFFER)))
        IO_DISK.append(item)
        _CostPostoptm += __COST_W_RAW
        
        # selecting the optimized algorithm
        result=[]
        result.append(dump_buff_algo1())
        result.append(dump_buff_algo2())
        
        all_result = sorted(result, key=lambda item : item[0])
        for rslt in all_result:
            print 'result: %s' % str(rslt)
        selected = all_result[0]
        print 'selected: %s' % str(selected)
        
        buffer_dump_write (selected[0], selected[1], selected[2])
        
def buffer_read_item(item):
    global BUFFER
    global IO_DISK
    global _CostPostoptm
    
    if in_buff(item) == True:
        dbg('buffer read: HIT (item: %s | buff_len: %s)' % (item, len(BUFFER)))
        IO_BUFFER.append(item)
        _CostPostoptm += __COST_R_BUF
    else:
        dbg('buffer read: MISS (item: %s | buff_len: %s)' % (item, len(BUFFER)))
        IO_DISK.append(item)
        _CostPostoptm += __COST_R_RAW
            
def buffer_dump_write(cost_d, buff_new, todisk):
    global BUFFER
    global IO_DISK
    global _CostPostoptm
    
    BUFFER = buff_new
    IO_DISK += todisk
    _CostPostoptm += cost_d
    print 'buffer: %s, cost:%s' % (str(BUFFER), _CostPostoptm)

def in_buff(item):
    _id = item['addr']
    for io in BUFFER:
        if io['addr'] == _id:
            return True
    return False

def print_summary(io_list, banner=None):
    global __VERBOSE    
    print '--------------------------->'
    print '%s Disk IO (len: %s), BufferSize: %s' % (banner, len(io_list), len(BUFFER))
    print '%s Buffer IO (len: %s), BufferSize: %s' % (banner, len(IO_BUFFER), len(BUFFER))
    if __VERBOSE:
        for io in io_list:
            print '---> %s' % OrderedDict(io)
    print '<---------------------------\n\n'

def dbg(msg):
    global __DEBUG
    if __DEBUG:
        print '[Debug] %s' % msg

if __name__ == '__main__':
#     global __DEBUG
    __DEBUG = False
    __VERBOSE = False
    
    #IO_ORIG = read_input('/Users/dyao/Documents/workspace/MasterProject/logs/io.csv')
    IO_ORIG = read_input('/Users/dyao/Documents/workspace/MasterProject/logs/io_short.csv')
    
    _CostPreoptm = get_cost_preopt(IO_ORIG)
    print '\n\n================ Summary ================'
    print 'original cost is: %s' % _CostPreoptm
    print_summary(IO_ORIG, 'original')
    
    
    for io in IO_ORIG:
        if io['rw'] == 'W':  # put to write buffer if its a write
            buffer_write_item(io)
        if io['rw'] == 'R':
            buffer_read_item(io)
    print '\n\n================ Summary ================'
    print 'optimized cost is %s' % _CostPostoptm
    print_summary(IO_DISK, 'optimized')
    print BUFFER


    print '\n\n================ Summary ================'
    print 'Original Cost: %s, Optimized: %s' % (_CostPreoptm, _CostPostoptm)
