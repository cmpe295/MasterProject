import bokeh.charts as charts
import pandas

import bokeh.plotting as plotting

def read_csv(csv_file):
    #file = './logs/io.csv'
    file = csv_file
    colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
    data = pandas.read_csv(file,names = colnames)
    return data;

def plot_addr_count(csv_file,direction, title):
    data = read_csv(csv_file)
    data_addr = map(lambda x: x/8, data.BLOCK.tolist())
    data_dir = data.D.tolist()
    map_dir2addr = zip(data_dir, data_addr)

    if direction == 'R':
        dic_out = []
        for item in map_dir2addr:
            if item[0]=='R':
                dic_out.append(item[1])
    elif direction == 'W':
        dic_out = []
        for item in map_dir2addr:
            if item[0]=='W':
                dic_out.append(item[1])

    title = title + '-' + csv_file.split('/')[-1]
    p = charts.Histogram(dic_out, bins=100, color='#FB9A99', title=title)
    charts.output_file("/tmp/%s.html" % title)
    charts.show(p)

def plot_time_addr(csv_file,direction, title):
    data = read_csv(csv_file)
    data_addr = zip(data.D.tolist(), map(lambda x: x/8, data.BLOCK.tolist())) 
    data_time = zip(data.D.tolist(), range(0, len(data_addr)))

    print data_addr
    print data_time

    if direction == 'R':
        x = []
        y = []
        for item in data_addr:
            if item[0]=='R':
                y.append(item[1])
        for item in data_time:
            if item[0]=='R':
                x.append(item[1])
    if direction == 'W':
        x = []
        y = []
        for item in data_addr:
            if item[0]=='W':
                y.append(item[1])
        for item in data_time:
            if item[0]=='W':
                x.append(item[1])


    title = title + '-' + csv_file.split('/')[-1]
    plotting.output_file('/tmp/%s.html' % title)
    r = plotting.figure(x_axis_type='datetime')
    r.title = title

    r.line(x, y)
    plotting.show(r)


def plot_time_size(csv_file,direction, title):
    data = read_csv(csv_file)
    data_size = zip(data.D.tolist(), map(lambda x: x/4096, data.SIZE.tolist()))
    data_time = zip(data.D.tolist(), range(0, len(data_size)))

    print data_size
    print data_time

    if direction == 'R':
        x = []
        y = []
        for item in data_size:
            if item[0]=='R':
                y.append(item[1])
        for item in data_time:
            if item[0]=='R':
                x.append(item[1])
    if direction == 'W':
        x = []
        y = []
        for item in data_size:
            if item[0]=='W':
                y.append(item[1])
        for item in data_time:
            if item[0]=='W':
                x.append(item[1])


    title = title + '-' + csv_file.split('/')[-1]
    plotting.output_file('/tmp/%s.html' % title)
    r = plotting.figure(x_axis_type='datetime')
    r.title = title

    r.line(x, y)
    plotting.show(r)




def plot_size_count(csv_file,dir,title):
    data = read_csv(csv_file)
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    data_dir = data.D.tolist()
    length = len(data_size)
    data_to_show = []
    for i in range(0,length):
        if(data_dir[i] == dir):
            data_to_show.append(data_size[i])

    print "Total data:", sum(data_to_show) , "MB"


    p = charts.Histogram(data_to_show,bins=100,color='#FB9A99',title=title)
    charts.output_file("/tmp/"+title+".html",title=title)
    charts.show(p)

def plot_shuffle_size_count(csv_file,dir,title):
    data = read_csv(csv_file)
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    data_dir = data.D.tolist()
    data_path = data.PATHNAME.tolist()
    length = len(data_size)
    data_to_show = []
    for i in range(0,length):
        if(data_dir[i] == dir and 'shuffle' in data_path[i]):
            data_to_show.append(data_size[i])

    print "Total shuffle data:", sum(data_to_show) , "MB"


    p = charts.Histogram(data_to_show,bins=100,color='#1F78B4',title=title)
    charts.output_file("/tmp/"+title+".html",title=title)
    charts.show(p)


def plot_size_time(csv_file,dir,title):
    data = read_csv(csv_file)
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    data_dir = data.D.tolist()
    length = len(data_size)
    data_to_show = []
    for i in range(0,length):
        if(data_dir[i]==dir):
            data_to_show.append(data_size[i])
    x = range(0,len(data_to_show))
    y = data_to_show


    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    plotting.output_file("/tmp/"+title+".html",title=title)
    r = plotting.figure(x_axis_type = "datetime", tools=TOOLS)
    r.title = title
    r.grid.grid_line_alpha=0.3

    r.line(x, y, color='#1F78B4', legend=title)
    #r.line(dates, choam, color='#FB9A99', legend='CHOAM')
    plotting.show(r)  # open a browser

def plot_addr_time(csv_file,dir,title):       # Y: address, X: time
    data = read_csv(csv_file)
    data_addr = map(lambda x: x, data.SIZE.tolist())
    data_dir = data.D.tolist()
    length = len(data_addr)
    data_to_show = []
    for i in range(0,length):
        if(data_dir[i]==dir):
            data_to_show.append(data_addr[i])
    x = range(0,len(data_to_show))
    y = data_to_show


    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    plotting.output_file("/tmp/"+title+".html",title=title)
    r = plotting.figure(x_axis_type = "datetime", tools=TOOLS)
    r.title = title
    r.grid.grid_line_alpha=0.3

    r.line(x, y, color='#1F78B4', legend=title)
    #r.line(dates, choam, color='#FB9A99', legend='CHOAM')
    plotting.show(r)  # open a browser

def plot_address_count():           #1: check address range count
    pass

def plot_seqOftime():           #1: random; 2: seq
    pass

def plot_dependencyOftime():           #1: check dependency
    pass

def plot_shuffleaddressOftime():       # Y: address, X: time
    pass

def plot_task_type_pi():    #percentage of shuffle,part-in,part-out
    pass

def plot_read_type_pi():        #percentage of 4K, 16K, 64K IO.
    pass

def plot_write_type_pi():
    pass

def plot_read_time_pi():        #percentage of 4K time, 16K time, 64K time
    pass

def plot_write_time_pi():
    pass

def plot_read_4k_time():
    pass

def plot_read_64k_time():
    pass

def plot_read_512k_time():
    pass

def plot_write_4k_time():
    pass

def plot_write_64k_time():
    pass

def plot_write_230k_time():
    pass

def plot_write_240k_time():
    pass

def plot_write_420k_time():
    pass

def plot_write_430k_time():
    pass

def plot_write_960k_time():
    pass

def plot_write_1024k_time():
    pass


if __name__ == '__main__':
#    plot_size_count('R','read_size_count')
#    plot_shuffle_size_count('R','read_shuffle_size_count')
#    plot_size_count('W','write_size_count')
#    plot_shuffle_size_count('W','write_shuffle_size_count')
#
#    plot_size_time('R','read_size_time')
#    plot_size_time('W','write_size_time')
#    plot_addr_time('R','read_addr_time')
#    plot_addr_time('W','write_addr_time')

    org = './output/gen.csv'
    opt = './output/optimize.csv'

    plot_addr_count(org,'W', 'plot_addr_count_W')
    plot_addr_count(opt,'W', 'plot_addr_count_W')

    #plot_addr_count(org,'R', 'plot_addr_count_R')
    #plot_addr_count(opt,'R', 'plot_addr_count_R')

    #plot_time_addr(org,'W', 'plot_time_addr_W')
    #plot_time_addr(opt,'W', 'plot_time_addr_W')

    #plot_time_addr(org,'R', 'plot_time_addr_R')
    #plot_time_addr(opt,'R', 'plot_time_addr_R')

    #plot_time_size(org,'W', 'plot_time_size_W')
    #plot_time_size(opt,'W', 'plot_time_size_W')

    #plot_time_size(org,'R', 'plot_time_size_R')
    #plot_time_size(opt,'R', 'plot_time_size_R')

