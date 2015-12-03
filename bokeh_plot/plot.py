from bokeh.charts import Histogram, output_file, show
import pandas

def read_csv():
    file = './logs/io.csv'
    colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']
    data = pandas.read_csv(file,names = colnames)
    return data;

def plot1():
    data = read_csv()
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    #print sum(data_size)

    p = Histogram(data_size,bins=100,title="data size distribution")
    output_file("/tmp/plot.html",)
    show(p)

def plot_size_count(dir,title):
    data = read_csv()
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    data_dir = data.D.tolist()
    length = len(data_size)
    data_to_show = []
    for i in range(0,length):
        if(data_dir[i] == dir):
            data_to_show.append(data_size[i])
    print "Total data:", sum(data_to_show) , "MB"
    
    p = Histogram(data_to_show,bins=100,title=title)

    output_file("/tmp/"+title+".html",)

    show(p)

def plot_read_size_count():
    plot_size_count('R','read_size_count')

def plot_write_size_count():
    plot_size_count('W','write_size_count')


if __name__ == '__main__':
    plot_read_size_count()
    plot_write_size_count()
    
