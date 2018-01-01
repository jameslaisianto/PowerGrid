# preprocess.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017

import power_sample as ps
from scipy.interpolate import interp1d
from collections import deque
from operator import itemgetter

# Given a list of points, index a and b
# return f(x) where f is a linear function
# generated from points[a] and points[b]
def lin_interp_x(points, a, b, x):
    return (points[a][1] +
                ((points[b][1]-points[a][1]) /
                (points[b][0]-points[a][0])) *
                (x-points[a][0]))

def interp_x(points, x):
    # Sort the points list
    points.sort(key=itemgetter(0))
    # Split into vectors
    x_list, y_list = zip(*points)
    try: # Cubic spline interpolation
        return interp1d(x_list, y_list, kind='cubic')(x)
    except ValueError:
        if len(points) < 2:
            raise ValueError('Insufficient interpolation points found')
        # Try linear interpolation/extrapolation as fall back
        # Find points closest to x
        for l in range(0, len(points)-1):
            if points[l][0] >= x: # We are past x
                if l == 0:
                    return lin_interp_x(points, l, l+1, x)
                else:
                    return lin_interp_x(points, l-1, l, x)
                    a = points[l-1]
                    b = points[l]
        # x is larger than the first n-1 elements. Use the last elements
        return lin_interp_x(points, len(points)-2, len(points)-1, x)
    
        
                
# Replace None values in power_sample_list with interpolated values
# look backwards and forwards max_pps samples to find pps non-None 
# samples. Note pps stands for 'points per sample'.
def ps_interp_replace(power_sample_list, pps, max_pps, na_threshold):
    for i in range(0, len(power_sample_list)):
        power_sample = power_sample_list[i]
        for prop in power_sample.properties.items():
            if prop[1] is None: # We must interpolate
                # Look back at most max_pps elements for
                # to get pps non-None values
                interp_points_list = []
                front_found = False
                back_found = False
                front_count = 0
                back_count = 0
                for j in range(1, max_pps + 1):
                    if len(interp_points_list) >= pps * 2:
                        break
                    # Append prior non-None points
                    if i - j >= 0:
                        if (power_sample_list[i-j].properties[prop[0]] 
                                is not None):
                            front_found = True
                            interp_points_list.append(
                                    (i-j, # x unit
                                    power_sample_list[i-j].properties[prop[0]]))
                        elif not front_found:
                            front_count = front_count + 1
                    # Append following non-None points
                    if i + j < len(power_sample_list):
                        if (power_sample_list[i+j].properties[prop[0]] 
                                is not None):
                            back_found = True
                            interp_points_list.append(
                                    (i+j, # x unit
                                    power_sample_list[i+j].properties[prop[0]]))
                        elif not back_found:
                            back_count = back_count + 1
                # Confirm that this point does not lay in a NA block
                if (front_count + back_count + 1 >= na_threshold or 
                        not front_found or not back_found):
                    continue
                # We now have a list of surrounding points
                # to be used for interpolation
                temp_props = power_sample_list[i].properties
                # Update with interpolated value
                temp_props[prop[0]] = interp_x(interp_points_list, i)
                # Assign updated value
                power_sample_list[i].properties = temp_props

    return power_sample_list
                    
# Test driver
from parse import csv_to_power_samples
def main(argv):
    power_samples = csv_to_power_samples(argv[1])
    power_samples = ps_interp_replace(power_samples, 10, 1000, 2)
    print("The first ", argv[2], " power samples are: ")
    for i in range(0, int(argv[2])):
        print("Power Sample ", i, ":")
        print(power_samples[i])

if __name__ == '__main__':
    import sys
    main(sys.argv)               
                    
                    
