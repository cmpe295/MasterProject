#!/usr/local/bin/python2.7
#from scipy import stats
import numpy as np

class Buffer():
    def __init__(self, config):    
        self.capacity = config['capacity']
        self.full_threshold = self.capacity * float(config['full_watermark'])
        self.hot_watermark = config['hot_watermark']
        self.size = 0
        self.addr_map = {}

    def get_size(self):
        return self.size;

    def check_empty(self):
        return self.size == 0

    def check_full(self):
        return self.size >= self.capacity

    def check_almost_full(self):
        return self.size >= self.full_threshold

    def translate_addr(self,addr):
        #translate from 512 bytes to 4KB
        newAddr = [addr[0]//8,addr[1]//8]
        return newAddr;

    def translate_addr_back(self,addr):
        #translate from 4kb to 512byte
        newAddr = [addr[0]*8,addr[1]*8]
        return newAddr;


    def add(self,addr):
        # Buffer user need to check Buffer almost full before adding a new entry
        if self.check_almost_full():
            return False

        realAddr = self.translate_addr(addr)
        for each in range(realAddr[0],realAddr[1]):
            if each not in self.addr_map:
                self.addr_map[each] = 1
                self.size += 1
            else:
                self.addr_map[each] += 1
        return True

    def remove(self,addr):
        realAddr = self.translate_addr(addr)
        for each in range(realAddr[0],realAddr[1]):
            if each not in self.addr_map:
                print "ERROR: trying to remove an address which is not in the buffer"
                return False
            else:
                del self.addr_map[each]
                self.size -= 1;
        return True

    def get_data(self,watermark):
        coldAddr = []
        if not self.check_empty():
            preEndAddr = -1
            for key in self.addr_map:
                startAddr = key
                endAddr = key+1
                if startAddr == preEndAddr:
                    coldAddr[-1][1] += 1
                else:
                    if self.addr_map[key] < watermark:
                        coldAddr.append([startAddr,endAddr])
                        preEndAddr = endAddr
                    else:
                        pass
        for i in range(0,len(coldAddr)):
            coldAddr[i] = self.translate_addr_back(coldAddr[i])
        return coldAddr

    def get_cold(self):
        if self.check_empty():
            return []
        addrs = self.get_data(self.hot_watermark*1)
        if len(addrs):
            return addrs;

        addrs = self.get_data(self.hot_watermark*2)
        if len(addrs):
            return addrs;

        addrs = self.get_data(self.hot_watermark*4)
        if len(addrs):
            return addrs;

        addrs = self.get_data(self.hot_watermark*8)
        if len(addrs):
            return addrs;

        addrs = self.get_data(self.hot_watermark*16)
        if len(addrs):
            return addrs;

        addrs = self.get_data(self.hot_watermark*32)
        if len(addrs):
            return addrs;

        return self.get_all()

    def get_all(self):
        return self.get_data(-1)

    def print_result(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


if __name__ == '__main__':
    myBuffer = Buffer({
        'capacity': 1000,       #how many 4K IO
        'full_watermark': 0.85,
        'hot_watermark': 4
    })

    myBuffer.add([0,8])
    myBuffer.add([0,8])
    myBuffer.add([0,8])
    myBuffer.add([8,16])
    myBuffer.add([8,16])
    myBuffer.add([8,16])
    print myBuffer.addr_map
    print "cold data:",myBuffer.get_cold()
    print myBuffer.addr_map
    myBuffer.remove(myBuffer.get_cold()[0])
    print myBuffer.addr_map
    print myBuffer.get_cold()
