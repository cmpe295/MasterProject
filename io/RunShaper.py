from Shaper import Shaper

full_watermark = 0.85
hot_watermark = 4
write_seq_threshold = 128       #128KB

##############################################################
capacity = 10*1000        #1MB
myShaper = Shaper({
        'capacity': capacity,         
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################

##############################################################
capacity = 100*1000        #50MB
myShaper = Shaper({
        'capacity': capacity,         
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################



##############################################################
capacity = 200*1000        #100MB
myShaper = Shaper({
        'capacity': capacity,         
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################


##############################################################
capacity = 400*1000        #200MB
myShaper = Shaper({
        'capacity': capacity,        
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################

##############################################################
capacity = 800*1000        #400MB
myShaper = Shaper({
        'capacity': capacity,         
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################

##############################################################
capacity = 1600*1000        #400MB
myShaper = Shaper({
        'capacity': capacity,         
        'full_watermark': full_watermark,
        'hot_watermark': hot_watermark,
        'write_seq_threshold': write_seq_threshold
    })
myShaper.run('./output/gen.csv','./output/optimize.csv')
myShaper.print_io_count()
##############################################################


exit(1)




