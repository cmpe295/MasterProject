from bokeh.charts import Histogram, output_file, show
import pandas

def plot1(file):

    colnames = ['STIME','TIME','UID','PID','D','BLOCK','SIZE','COMM','PATHNAME']

    data = pandas.read_csv(file,names = colnames)
    data_size = map(lambda x: x/1024, data.SIZE.tolist())
    #print data_size

    p = Histogram(data_size,bins=100,title="data size distribution")

    output_file("/tmp/plot.html",)

    show(p)

if __name__ == '__main__':
    plot1('./logs/io.csv')
    
