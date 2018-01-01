# filter.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017

from power_sample import PowerSample
from parse import csv_to_power_samples as Parse
from filter_column import filter_columns as col_filter
import datetime
import csv
import numpy as np


# Query for Morning, Daytime or Night. Multiple states can be queried at the same time.
# Example usage: statearray = ['Morning', 'Daytime']
# filter_statetime(power_sample_list, statearray)
def state_cond(power_sample):
    h = power_sample.time.hour + power_sample.time.minute / 60. + power_sample.time.second / 3600.
    selected=[] 

    #dividing the hours data into 3 states, morning, daytime and night
    if h >= 5 and h < 10:
        selected.append('morning')
    elif h >= 10 and h < 23:
        selected.append('daytime')
    else:
        selected.append('night')
    return selected

def filter_statetime(power_sample_list, state_list):
    state_dict = {'morning':1, 'daytime':2, 'night':3}

    selected=[]
    for state in state_list:
        for power_sample in power_sample_list: 
            temparr = state_cond(power_sample)
            if temparr[0] == state:
                selected.append(power_sample)
    return selected

def state_list(power_sample_list):
    state_dict = {'morning':1, 'daytime':2, 'night':3}

    selected=[]
    for power_sample in power_sample_list: 
        h = power_sample.time.hour + power_sample.time.minute / 60. + power_sample.time.second / 3600.
        #dividing the hours data into 3 states, morning, daytime and night
        if h >= 5 and h < 10:
            selected.append('morning')
        elif h >= 10 and h < 23:
            selected.append('daytime')
        else:
            selected.append('night')
    return selected

def initial_prob_state(power_sample_list):
    state_dict = {'morning':[], 'daytime':[], 'night':[]}

    for power in power_sample_list:
        temparr = state_cond(power)
        if temparr[0] == 'morning':
            state_dict['morning'].append(power)
        elif temparr[0] == 'daytime':
            state_dict['daytime'].append(power)
        else:
            state_dict['night'].append(power)

    prob = lambda x: np.count_nonzero(state_dict[x],axis=1)/np.count_nonzero(power_sample_list, axis=1)
    
    return (prob('morning'), prob('daytime'), prob('night'))

def trans_prob_state(power_samples_list):
# Test for Emission Probability
    print('States Probability')
    night = filter_statetime(power_samples_list, ['night'])
    nignig = (np.count_nonzero(night,axis=1)-1)/np.count_nonzero(night, axis=1)
    nigday = 0
    nigmorn = 1/np.count_nonzero(night, axis=1)
    print(nignig+nigday+nigmorn)

    print('Daytime')
    daytime = filter_statetime(power_samples_list, ['daytime'])
    daynig = 1/np.count_nonzero(daytime, axis=1)
    daymorn = 0
    dayday = (np.count_nonzero(daytime,axis=1)-1)/np.count_nonzero(daytime, axis=1)
    print(dayday+daymorn+daynig)

    print('Morning')
    morning = filter_statetime(power_samples_list, ['morning'])
    mornnig = 0
    mornday = 1/np.count_nonzero(morning, axis=1)
    mornmorn = (np.count_nonzero(morning,axis=1)-1)/np.count_nonzero(morning, axis=1)
    print(mornnig+mornday+mornmorn)

    trans_matrix = np.array([[mornmorn,mornday,mornnig],
                                [daymorn,dayday,daynig],
                                [nigmorn,nigday,nignig]])
    return trans_matrix


# Query for particular days needed from a PowerSample List
def dayname(power_sample_list,day_list):
    day_dict = {'monday':1, 'tuesday':2,'wednesday':3, 'thursday':4,'friday':5, 'saturday':6,'sunday':7}
    #dictionary for all day name
    # day = datetime.date.isoweekday(power_sample_list)

    selected=[] 
    for day in day_list: 
        for power_sample in power_sample_list: 
            if power_sample.date.isoweekday() == day_dict[day]: 
                selected.append(power_sample) 
    return selected

def day_list(power_sample_list):
    day_dict = {'monday':1, 'tuesday':2,'wednesday':3, 'thursday':4,'friday':5, 'saturday':6,'sunday':7}
    get_day=[]
    for power in power_sample_list:
        if power.date.isoweekday() == 1:
            get_day.append('monday')
        elif power.date.isoweekday() == 2:
            get_day.append('tuesday')
        elif power.date.isoweekday() == 3:
            get_day.append('wednesday')
        elif power.date.isoweekday() == 4:
            get_day.append('thursday')
        elif power.date.isoweekday() == 5:
            get_day.append('friday')
        elif power.date.isoweekday() == 6:
            get_day.append('saturday')
        else:
            get_day.append('sunday')
    return get_day
# Query for Month. Multiple states can be queried at the same time.
# Example usage: year_array = ['January', 'February']
# monthname(power_sample_list, month_array)
def monthname(power_sample_list, month_list):
    month_dict = {'january':1, 'february':2,'march':3, 
                'april':4,'may':5, 'june':6,'july':7,
                'august':8,'september':9, 'october':10,'november':11
                ,'december':12}

    selected=[]
    for pick_month in month_list:
        for power_sample in power_sample_list:
            if power_sample.date.month == month_dict[pick_month]:

                selected.append(power_sample)
    return selected

def month_list(power_sample_list):
    month_dict = {1:'january', 2:'february',3:'march', 
                4:'april',5:'may', 6:'june',7:'july',
                8:'august',9:'september', 10:'october',11:'november'
                ,12:'december'}

    get_month=[]
    for power in power_sample_list:
        for i in range(1,13):
            if power.date.month == i:
                get_month.append(month_dict[i])
    return get_month

# Query for Year. Multiple states can be queried at the same time.
# Example usage: year_array = ['2012', '2013']
# yearname(power_sample_list, year_array)
def yearname(power_sample_list, year_list):
	#Why you put it into temporary array?
	selected=[]
	for pick_year in year_list:
		for power_sample in power_sample_list:
			if power_sample.date.year == int(pick_year):
				selected.append(power_sample)
	return selected

def year_list(power_sample_list):
    get_year=[]
    for power in power_sample_list:
        get_year.append(power.date.year)
    return get_year

def season(power_sample):
	month = power_sample.date.month
	selected=[] 
	#dividing the hours data into 3 states, morning, daytime and night
	if month == 12 or month < 3:
		selected.append('winter')
	elif month >= 3 and month < 6:
		selected.append('spring')
	elif month >= 6 and month < 9:
		selected.append('summer')
	else:
		selected.append('fall')
	return selected

def season_list(power_sample_list):
    selected=[]
    for power_sample in power_sample_list:
        month = power_sample.date.month
         
        #dividing the hours data into 3 states, morning, daytime and night
        if month == 12 or month < 3:
            selected.append('winter')
        elif month >= 3 and month < 6:
            selected.append('spring')
        elif month >= 6 and month < 9:
            selected.append('summer')
        else:
            selected.append('fall')
    return selected


#4 Seasons
def seasonsname(power_sample_list, season_list):
	selected=[]
	for pick_season in season_list:
		for power_sample in power_sample_list:
			temparr = season(power_sample)	
			if  temparr[0]== pick_season:
				selected.append(power_sample)
	return selected

def initial_prob_season(power_sample_list):
    season_dict = {'spring':[], 'summer':[], 'fall':[], 'winter':[]}

    for power in power_sample_list:
        temparr = season(power)
        if temparr[0] == 'spring':
            season_dict['spring'].append(power)
        elif temparr[0] == 'summer':
            season_dict['summer'].append(power)
        elif temparr[0] == 'fall':
            season_dict['fall'].append(power)
        else:
            season_dict['winter'].append(power)

    prob = lambda x: np.count_nonzero(season_dict[x],axis=1)/np.count_nonzero(power_sample_list, axis=1)
    
    initial_season_matrix = np.array([[prob('spring'), prob('summer'), prob('fall'),prob('winter')]])
    print(prob('spring')+ prob('summer')+ prob('fall')+prob('winter'))
    return initial_season_matrix

def trans_prob_season(power_samples_list):
# Test for Emission Probability
    print('Season Probability')

    spring = seasonsname(power_samples_list, ['spring'])
    sprspr = (np.count_nonzero(spring,axis=1)-1)/np.count_nonzero(spring, axis=1)
    sprsum = 1/np.count_nonzero(spring, axis=1)
    sprfall = 0
    sprwin = 0
    print(sprspr+sprsum+sprfall+sprwin)

    print('Summer')
    summer = seasonsname(power_samples_list, ['summer'])
    sumsum = (np.count_nonzero(summer,axis=1)-1)/np.count_nonzero(summer, axis=1)
    sumfall = 1/np.count_nonzero(summer, axis=1)
    sumspr = 0
    sumwin = 0
    print(sumspr+sumsum+sumfall+sumwin)

    print('Fall')
    fall = seasonsname(power_samples_list, ['fall'])
    fallfall = (np.count_nonzero(fall,axis=1)-1)/np.count_nonzero(fall, axis=1)
    fallwin = 1/np.count_nonzero(fall, axis=1)
    fallspr = 0
    fallsum = 0
    print(fallspr+fallsum+fallfall+fallwin)

    print('Winter')
    winter = seasonsname(power_samples_list, ['winter'])
    winwin = (np.count_nonzero(winter,axis=1)-1)/np.count_nonzero(winter, axis=1)
    winspr = 1/np.count_nonzero(winter, axis=1)
    winfall = 0
    winsum = 0
    print(winspr+winsum+winfall+winwin)

    trans_season_matrix = np.array([[sprspr,sprsum,sprfall,sprwin],
                            [sumspr,sumsum,sumfall,sumwin],
                            [fallspr,fallsum,fallfall,fallwin],
                            [winspr,winsum,winfall,winwin]])
    return trans_season_matrix

def filter_list(power_sample_list,filter_name):
    if filter_name == 'day':
        return day_list(power_sample_list)
    elif filter_name == 'month':
        return month_list(power_sample_list)
    elif filter_name == 'year':
        return year_list(power_sample_list)
    elif filter_name == 'season':
        return season_list(power_sample_list)
    elif filter_name == 'state':
        return state_list(power_sample_list)


def find_quartiles(power_sample_list, observation_list):
    columns = col_filter(power_sample_list,
            [observation_list],
            lambda a,b: a.properties[b])
    q2 = np.percentile(columns[observation_list],67)
    q1 = np.percentile(columns[observation_list],33)
    
    quartile_dict = {'low':[], 'medium':[], 'high':[]}
    
    for col in columns[observation_list]:
        if col <= q1:
            quartile_dict['low'].append(col)
        elif col > q2:
            quartile_dict['high'].append(col)
        else:
            quartile_dict['medium'].append(col)
    
    prob = lambda x: np.count_nonzero(quartile_dict[x],axis=1)/np.count_nonzero(columns[observation_list], axis=1)
    
    return (prob('low'), prob('medium'), prob('high'))


def tokenize_samples(power_sample_list, observation):
    column = col_filter(power_sample_list,
            [observation],
            lambda a,b: a.properties[b])[observation]
    high = np.percentile(column,67)
    low = np.percentile(column,33)
    for i in range(0,len(column)):
        if column[i] <= low:
            column[i] = 0
        elif column[i] > high:
            column[i] = 2
        else:
            column[i] = 1
    return column


def get_emmission_array(power_samples_list,attr_list):
    # Test for Emission Probability
    print('Emission Probability')
    night = filter_statetime(power_samples_list, ['night'])
    night_low, night_medium, night_high = find_quartiles(night,attr_list)
    print(night_low+night_medium+night_high)

    print('Daytime')
    daytime = filter_statetime(power_samples_list, ['daytime'])
    daytime_low, daytime_medium, daytime_high = find_quartiles(daytime,attr_list)
    print(daytime_low+daytime_medium+daytime_high)

    print('Morning')
    morning = filter_statetime(power_samples_list, ['morning'])
    morning_low, morning_medium, morning_high = find_quartiles(morning,attr_list)
    print(morning_low+morning_medium+morning_high)

    emmision_matrix = np.array([[morning_low, morning_medium, morning_high],
                                [daytime_low, daytime_medium, daytime_high],
                                [night_low, night_medium, night_high]])
    return emmision_matrix


def to_state_day(date,time):
    get_day=[]
    for day_ in date:
        get_day.append(day_.isoweekday() - 1)
    return get_day

def to_state_month(date,time):
    get_month=[]
    for date_ in date:
        get_month.append(date_.month - 1)
    return get_month

def to_state_season(date,time):
    selected=[]
    for date_ in date:
        month = date_.month
         
        #dividing the hours data into 3 states, morning, daytime and night
        if month == 12 or month < 3:
            selected.append(3) #Winter
        elif month >= 3 and month < 6:
            selected.append(0) #Spring
        elif month >= 6 and month < 9:
            selected.append(1) #Summer
        else:
            selected.append(2) #Fall
    return selected

def to_state_time(date,time):
    selected=[]
    for time_ in time: 
        h = time_.hour + time_.minute / 60. + time_.second / 3600.
        #dividing the hours data into 3 states, morning, daytime and night
        if h >= 5 and h < 10:
            selected.append(0)
        elif h >= 10 and h < 23:
            selected.append(1)
        else:
            selected.append(2)
    return selected


def to_state(date,time,filter_type):
    if filter_type == 'day':
        list_ = to_state_day(date,time)
        return (7,list_)
    elif filter_type == 'month':
        list_ = to_state_month(date,time)
        return (12,list_)
    elif filter_type == 'season':
        list_ = to_state_season(date,time)
        return (4,list_)
    elif filter_type == 'time':
        list_ = to_state_time(date,time)
        return (3,list_)
    else:
        raise ValueError('Undefined filter type')


# def to_symbol(column_name_list, column_name):
#     columns = column_name_list
#     q2 = np.percentile(columns,67)
#     q1 = np.percentile(columns,33)

#     quartile_dict = []
    
#     for col in columns:
#         if col <= q1:
#             quartile_dict.append(0)
#         elif col > q2:
#             quartile_dict.append(2)
#         else:
#             quartile_dict.append(1)
#     return (3, quartile_dict)

def to_symbol(columns, column_name):
    if column_name == 'global_active_power':
        return to_nsymbols(columns, 5)
    elif column_name == 'global_reactive_power':
        return to_nsymbols(columns, 3)
    elif column_name == 'voltage':
        return to_nsymbols(columns, 3)
    elif column_name == 'global_intensity':
        return to_nsymbols(columns, 3)
    elif column_name == 'sub_metering_1':
        return to_nsymbols(columns, 3)
    elif column_name == 'sub_metering_2':
        return to_nsymbols(columns, 3)
    elif column_name == 'sub_metering_3':
        return to_nsymbols(columns, 3)
    else:
        raise ValueError('Undefined filter type')

def to_nsymbols(column_name_list, n_division):
    n_array =[]
    n_size = 100 / n_division
    count =(100 / n_division)
    for i in range(0,n_division-1):
        n_array.append(np.percentile(column_name_list,n_size))
        n_size = count + n_size
    n_array.append(np.percentile(column_name_list,100))    

    quartile_list = []
    
    for col in column_name_list:
        for i in range(0, n_division):
            if col <= n_array[i]:
                quartile_list.append(i)
                break

    return (n_division, quartile_list)
    
def range_values(column_name_list):
    n_array =(np.ptp(column_name_list))
    return n_array



# Test driver
def main(argv):
    power_samples_list = Parse(argv[1])

 #    # Test for dayname
 #    print('Dayname')
 #    days = ['monday','tuesday','wednesday', 'thursday']
 #    result = dayname(power_samples_list, days)
 #    for value in result:
 #    	print(value.date)
 #    print('\n')

 #    # Test for three_states
 #    print('Three States')
 #    states = ['night']
 #    result = filter_statetime(power_samples_list, states)
 #    for value in result:
 #    	print(value)

 #    result = day_list(power_samples_list)
 #    for value in result:
 #      print(value)
 #    print('\n') 

 #    #Test 4 States
 #    columns1 = col_filter(power_samples_list,
 #            ['date'],
 #            lambda a,b: a.properties[b])
 #    columns2 = col_filter(power_samples_list,
 #            ['time'],
 #            lambda a,b: a.properties[b])


 #    filter_type = 'day'
 #    result = to_state(columns1['date'],columns2['time'],filter_type)
 #    print(result)


    columns3 = col_filter(power_samples_list,
            ['voltage'],
            lambda a,b: a.properties[b])


    filter_type = 'voltage'
    result = to_symbol(columns3[filter_type],filter_type)
    print(result)

    print('Range')
    result = range_values(columns3[filter_type])
    print(result)

 #    result = filter_list(power_samples_list, 'state')
 #    print(result)
 #    print('\n') 

 #    result = initial_prob_state(power_samples_list)
 #    for value in result:
 #      print(value)
 #    print('\n')

 #    #Test state prob
 #    print('Probability States')
 #    result = trans_prob_state(power_samples_list)
 #    for value in result:
 #      print(value)
 #    print('\n')

 #    result = initial_prob_season(power_samples_list)
 #    for value in result:
 #      print(value)
 #    print('\n')

 #    #Test state prob
 #    print('Probability Season')
 #    result = trans_prob_season(power_samples_list)
 #    for value in result:
 #      print(value)
 #    print('\n')


 #    #Test for Quartile
 #    print('Quartile')
 #    observation = 'voltage'
 #    result2 = find_quartiles(power_samples_list, observation)
    # print(result2)
 #    print('\n')

 #    #Test
 #    result = get_emmission_array(power_samples_list,'voltage')
 #    for value in result:
 #      print(value)
 #    print('\n')

 #    #Tokenize
 #    observation = 'voltage'
 #    result = tokenize_samples(power_samples_list, observation)
 #    for value in result:
 #      print(value)
 #    print('\n')

 #    #Test for the yearname Range: 2006-2009
 #    print('Yearname')
 #    year = [2008, 2009]
 #    result = yearname(power_samples_list, year)
 #    for value in result:
 #    	print(value.date)
 #    print('\n')
 #    # #Test for the monthname Range: 2006-2009
 #    print('Monthname')
 #    month = ['december', 'january']
 #    result = monthname(power_samples_list, month)
 #    for value in result:
 #    	print(value.date)
 #    print('\n')
	# # Test for seasons
 #    print('Seasons')
 #    seasons = ['winter']
 #    result = seasonsname(power_samples_list, seasons)
 #    for value in result:
 #    	print(value.time)
 #    print('\n')
    

if __name__ == '__main__':
    import sys
    main(sys.argv)

