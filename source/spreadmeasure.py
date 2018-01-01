from power_sample import PowerSample
from parse import csv_to_power_samples

import numpy as np

def get_column(samples, column_string):
    temparr = []

# Refactored by our God, Sean

    for sample in samples:
        if(sample.properties[column_string] is None):
            continue
        temparr.append(sample.properties[column_string])
	
    return temparr


def mean(samples, column_string):
    temparr = get_column(samples, column_string)
    meanvalue = np.average(temparr)
    return meanvalue

def stddev(samples, column_string):
    temparr = get_column(samples, column_string)
    stdvalue = np.std(temparr)
    return stdvalue

# EXAMPLE USAGE
#################
''' 

samples = csv_to_power_samples('/home/vagrant/PowerGrid/data/test1.txt')
meanv = mean(samples, 'voltage')
print(meanv)

'''
#################