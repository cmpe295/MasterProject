'''
Created on Oct 25, 2015

@author: dyao
'''

from matplotlib import pyplot

def pyplot_apply_2d(label_x='x', label_y='y', title='Interesting Graph\nCheck it out'):
    pyplot.xlabel(label_x)
    pyplot.ylabel(label_y)
    pyplot.title(title)
    pyplot.legend()
    pyplot.show()

def basics_and_your_first_graph():
    
    pyplot.plot([1,2,3,4], [4,7,8,12], label='first line')
    
    x = [2,3,4]
    y = [10,17,15]
    pyplot.plot(x, y, label='second line')
    
    pyplot.title("my test graph")
    pyplot.xlabel('matplot x label')
    pyplot.ylabel('matplot y label')
    pyplot.legend()
    
    pyplot.show()
    

def reading_from_file_and_plot():

    log_f = open('testlog/test.log', 'r')
    data_entry = log_f.read().split('\n')
    log_f.close()
    
    x = [int(tup.split(',')[1]) for tup in data_entry]
    y = [int(tup.split(',')[0]) for tup in data_entry]
    
    pyplot.plot(x, y)
    pyplot.show()
    
def barcharts_and_histograms():
    # barchart
    x = [2,4,6,8,10]
    y = [6,7,8,2,4]
     
    x2 = [1,3,5,9,11]
    y2 = [7,8,2,4,2]
     
    pyplot.bar(x, y, label='Bars1', color='red')
    pyplot.bar(x2, y2, label='Bars2', color='cyan')
    
    # histogram
    population_ages = [22,55,62,45,21,22,34,42,52, 4, 99,102, 110, 120, 121, 130, 111, 115, 112, 80,75, 65, 54, 44, 43, 42, 48, 49]
    # ids = [x for x in range(len(population_ages))]
    bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]
    
    pyplot.hist(population_ages, bins, histtype='bar', rwidth=0.8, label='histogram')
    
    
    pyplot.xlabel('x')
    pyplot.ylabel('y')
    pyplot.title('Interesting Graph\nCheck it out')
    pyplot.legend()
    pyplot.show()
    
    
def scatter_plots():
    x = [1,2,3,4,5,6,7,8]
    y = [5,2,4,2,1,4,5,2]
    
    pyplot.scatter(x, y, label='skitscat', color='black', marker='*', s=100)
    pyplot_apply_2d()


def stack_plots():
    days = [1,2,3,4,5]
    sleeping = [7,8,6,11,7]
    eating = [2,3,4,3,2]
    working = [7,8,7,2,2]
    playing = [8,5,7,8,13]
    
    
    pyplot.plot([], [], color='magenta', label='Sleeping', linewidth=3)
    pyplot.plot([], [], color='cyan', label='Eating', linewidth=3)
    pyplot.plot([], [], color='red', label='Working', linewidth=3)
    pyplot.plot([], [], color='black', label='Playing', linewidth=3)
    pyplot.stackplot(days, sleeping, eating, working, playing, colors=['magenta', 'cyan', 'red', 'black'])
    pyplot_apply_2d()

    
if __name__ == '__main__':
#     basics_and_your_first_graph()
#     reading_from_file_and_plot()
#     barcharts_and_histograms()
#     scatter_plots()
    stack_plots()