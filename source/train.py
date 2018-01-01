# train.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017
from power_sample import PowerSample
from parse import csv_to_power_samples as Parse
from filter_column import filter_columns
import numpy as np
import hmm
# Test driver
def main(argv):
	power_samples_list = Parse(argv[1])
	directory = argv[2]
	#column name = attributes
	#"Global_active_power","Global_reactive_power","Voltage",
	#"Global_intensity","Sub_metering_1","Sub_metering_2","Sub_metering_3"
	# column_dict = {'global_active_power':1,'global_reactive_power':2,'voltage':3,'global_intensity':4,'sub_metering_1':5,'sub_metering_2':6,'sub_metering_3':7}
	column_dict = {1:'global_active_power',2:'global_reactive_power',3:'voltage',4:'global_intensity'}

	#filter = states
	filter_dict = {1:'day',2:'month',3:'season',4:'time'}
	for column_ in range(1,5):
		for filter_ in range(1,5):
			print(column_dict[column_])
			print(filter_dict[filter_])
			print(directory+'/'+str(column_)+str(filter_))
			hmm.generate(power_samples_list, column_dict[column_], filter_dict[filter_], directory+'/'+str(column_)+str(filter_))
			#returns date and time and bunch of 1s and 0s
if __name__ == '__main__':
	import sys
	main(sys.argv)


