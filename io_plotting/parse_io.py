'''
Created on Oct 25, 2015

@author: dyao
'''

import re,json

def parse_iosnoop(pid, log_path):
    log_f = open(log_path)
    log_content = log_f.read()
    
    
    filtered_data = []
    
    for line in log_content.split('\n'):
        # sudo iosnoop -st |tee /Users/dyao/Documents/workspace/MasterProject/io_plotting/testlog/iosnoop.log
        matcher = re.match(r'\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\w)\s+(\d+)\s+(\d+)\s+(\w+)\s+(.*)\s*', line, re.IGNORECASE)

        
        if matcher != None:            
            time_start_us = int(matcher.group(1))
            time_end_us = int(matcher.group(2))
            user_id = int(matcher.group(3))
            process_id = int(matcher.group(4))
            rw_direction = str(matcher.group(5))
            block_addr = int(matcher.group(6))
            size_byte = int(matcher.group(7))
            command = str(matcher.group(8))
            path_name = str(matcher.group(9))
            if process_id == pid:
                entry = {'STIME': time_start_us,
                         'TIME': time_end_us,
                         'UID': user_id,
                         'PID': process_id,
                         'D': rw_direction,
                         'BLOCK': block_addr,
                         'SIZE': size_byte,
                         'COMM': command,
                         'PATHNAME': path_name
                         }
                filtered_data.append(entry) 
    log_f.close()
    
    
    return filtered_data
        
        
if __name__ == '__main__':
    
    ret_obj = parse_iosnoop(565, '/Users/dyao/Documents/workspace/MasterProject/io_plotting/testlog/iosnoop.log')
    print json.dumps(ret_obj, indent=4)
    
