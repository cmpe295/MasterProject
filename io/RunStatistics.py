from Statistics import Statistics

#no SSD cache
myStat = Statistics({
    'file'          : './output/gen.csv',
    'ssd_size'      : 000*1024*1024,        
    'ssd_seq_write' : 400*1024*1024,
    'ssd_seq_read'  : 500*1024*1024,
    'ssd_ran_write' : 80*1000,
    'ssd_ran_read'  : 100*1000,
    'ssd_read_hit'   : 0.91,                
    'hdd_seq_write' : 400*1024*1024,
    'hdd_seq_read'  : 500*1024*1024,
    'hdd_ran_write' : 1400,
    'hdd_ran_read'  : 1400
})
myStat.run()


#400GB SSD without optimizer
myStat = Statistics({
    'file'          : './output/gen.csv',
    'ssd_size'      : 200*1024*1024,        
    'ssd_seq_write' : 400*1024*1024,
    'ssd_seq_read'  : 500*1024*1024,
    'ssd_ran_write' : 80*1000,
    'ssd_ran_read'  : 100*1000,
    'ssd_read_hit'   : 0.91,                
    'hdd_seq_write' : 400*1024*1024,
    'hdd_seq_read'  : 500*1024*1024,
    'hdd_ran_write' : 1400,
    'hdd_ran_read'  : 1400
})
myStat.run()


#400GB SSD with optimizer
myStat = Statistics({
    'file'          : './output/optimize.csv',
    'ssd_size'      : 200*1024*1024,        
    'ssd_seq_write' : 400*1024*1024,
    'ssd_seq_read'  : 500*1024*1024,
    'ssd_ran_write' : 80*1000,
    'ssd_ran_read'  : 100*1000,
    'ssd_read_hit'   : 0.91,                
    'hdd_seq_write' : 400*1024*1024,
    'hdd_seq_read'  : 500*1024*1024,
    'hdd_ran_write' : 1400,
    'hdd_ran_read'  : 1400
})
myStat.run()
