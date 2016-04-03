from Gen import Gen
from Shaper import Shaper
from Statistics import Statistics

full_watermark = 0.85
hot_watermark = 4
write_seq_threshold = 128       #128KB
capacity = 400*1000 #400GB
text_file = open("Training-BufSize.txt", "w")

for genRange in xrange(512, 16*1024, 64): #from 512GB to 20TB

    myGen = Gen({
        'range': (1,genRange*1024*1024//512),
        'count': 2*1024*1024*1024//4096,
        'write_percent': 0.5,
        'write_ran_percent': 0.67,
        'read_ran_percent': 0.67
    })
    myGen.gen()



    for bufSize in xrange(1,1024,4):
        ##############################################################
        capacity = bufSize*1024        #200MB
        myShaper = Shaper({
                'capacity': capacity,        
                'full_watermark': full_watermark,
                'hot_watermark': hot_watermark,
                'write_seq_threshold': write_seq_threshold
            })
        myShaper.run('./output/gen.csv','./output/optimize.csv')
        myShaper.print_io_count()

        ##############################################################
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
        text_file.write("%d,%d,%f\n" % (genRange,bufSize,myStat.total_time))

text_file.close()
exit(1)

