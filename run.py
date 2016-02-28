#!/usr/bin/python

import sys
import os
import csv

if(len(sys.argv)<2):
    print 'Valid arguments as bellow:'
    print '\t install'
    print '\t teragen 1g'
    print '\t terasort'
    print '\t parse'
    print '\t iplot'
    print '\t bplot'
    exit(1)

command = sys.argv[1].lower();
curdir = os.getcwd()

if(command=='install'):
    print 'Start to install TeraSort module'
    #os.system('cd spark-terasort && mvn install')
    print 'Start to install matplotlib'
    os.system('pip install matplotlib')
    print 'Start to install bokeh'
    os.system('pip install bokeh')

if(command=='teragen'):
    if(len(sys.argv)!=3):
        print 'Error: Size of target data must be specified.'
        exit(1)
    print 'Start to generate random data, size will be: ' + sys.argv[2]
    shellcmd =   'spark-submit --class com.github.ehiggs.spark.terasort.TeraGen ' \
               + curdir + '/spark-terasort/target/spark-terasort-1.0-SNAPSHOT-jar-with-dependencies.jar ' \
               + sys.argv[2] + ' file://' + curdir + '/spark-terasort/data/in'
    os.system(shellcmd)

if(command=='terasort'):
    sparkcmd =   'spark-submit --class com.github.ehiggs.spark.terasort.TeraSort ' \
               + curdir + '/spark-terasort/target/spark-terasort-1.0-SNAPSHOT-jar-with-dependencies.jar ' \
               + ' file://' + curdir + '/spark-terasort/data/in' \
               + ' file://' + curdir + '/spark-terasort/data/out'
    iosnoopcmd =   "osascript -e 'tell app \"Terminal\" \n" \
                + "\tdo script \" cd " + curdir + "&& mkdir logs && rm -rf ./logs/io.log && sudo iosnoop -s -t | tee ./logs/io.log\" \n" \
                + "end tell' "
    os.system(iosnoopcmd)
    os.system(sparkcmd)

if(command=='iplot'):
    os.system('python ./io_plotting/io_plot.py')

if(command=='bplot'):
    os.system('python ./bokeh_plot/plot.py')

if(command=='parse'):
    log_file = open('./logs/io.log')
    log_content = log_file.read().split('\n');
    log_content.pop()
    content_list = []
    for line in log_content:
        each = line.split()
        try:
            if each[7] in {'java','mdworker'}: 
                content_list.append(each) 
        except:
            pass
    csv_file = open('./logs/io.csv','wb')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(content_list)
