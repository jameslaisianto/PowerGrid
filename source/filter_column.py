# filter_column.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017


# Takes a list objects and calls func on each element if specified to
# extract a dictionary for filtering. Outputs a dictionary of lists
def filter_columns(sample_list, filter_list, func=lambda a,b: a[b]):
    # Build the output framework
    out = {}
    for element in filter_list:
        out[element] = []
    
    # Iterate through the samples to fill the output
    for sample in sample_list:
        is_good = True
        # Check sample goodness
        for element in filter_list:
            if func(sample, element) is None:
                is_good = False
                break
        # Insert elements
        if is_good:
            for element in filter_list:
                out[element].append(func(sample, element))
                
    return out


# Test driver
from power_sample import PowerSample
import datetime
import csv
from parse import csv_to_power_samples
def main(argv):
    power_samples = csv_to_power_samples(argv[1])
    columns = filter_columns(power_samples,
            ['date','time','global_intensity'],
            lambda a,b: a.properties[b])
            
    print(columns)
        

if __name__ == '__main__':
    import sys
    main(sys.argv)   
 
