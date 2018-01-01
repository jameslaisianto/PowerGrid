import numpy as np
from hmmlearn import hmm
import filter as filter_
from power_sample import PowerSample
from parse import csv_to_power_samples as Parse
from filter_column import filter_columns
import pickle

# Extract parameters
def extract(power_samples, column_name, filter_type):
    # columns is a dictionary containing date, time and the selected column
    # column_name
    columns = filter_columns(power_samples,
                ['date','time', column_name],
                lambda a,b: a.properties[b])
            
    # to_state needs to be implemented, and takes the date and time 
    # columns to form a new state column populated with the corresponding
    # state
    columns['state'] = filter_.to_state(columns['date'], columns['time'], filter_type)
    # Tokenize the selected y values
    columns['symbol'] = filter_.to_symbol(columns[column_name], column_name)
    return columns


# Build transition matrix
# Use the categorized data to determine state transition matrix values
# From --> rows, To --> columns
def calculate(columns):
    transition_dict = {}
    for element in columns['state'][1]:
        if element in transition_dict:
            transition_dict[element].append(element)
        else:
            transition_dict[element] = []
        last = element

    # We now have a dictionary with transitions from key to value
    # and should be able to fill the transition matrix
    # using the first matrix as the order. Note: we should fix this so that
    # an order matrix defines order (or the categories are numeric and in
    # order
    transition_matrix = np.zeros(shape=(columns['state'][0], columns['state'][0]))
    for item in transition_dict.items():
        # Sum the transition probability slices
        for element in item[1]: # NOTE: This method is not very robust #macm316
            transition_matrix[item[0], element] = (transition_matrix[item[0], element] +
                    (1 / len(item[1])))
    # Build emission matrix
    # For each state simpily count the number of each symbol occurence
    emission_dict = {}
    for i in range(0, len(columns['state'])):
        if columns['state'][1][i] in emission_dict:
            emission_dict[columns['state'][1][i]].append(columns['symbol'][1][i])
        else:
            emission_dict[columns['state'][1][i]] = []
    # We now have a dictionary with a list of observed symbols for each state
    # that we will convert to an emission matrix
    emission_matrix = np.zeros(shape=(columns['state'][0], columns['symbol'][0]))
    for item in emission_dict.items():
        for element in item[1]:
            emission_matrix[item[0], element] = (emission_matrix[item[0], element] +
                    (1 / len(item[1])))

    # Build initial state vector
    # For now we are going to have equal probability
    initial_matrix = np.full((columns['state'][0],1), 1/columns['state'][0])

    return (transition_matrix, emission_matrix, initial_matrix)


# Fit model
def build(transition_matrix, emission_matrix, initial_matrix, columns, dump_path=None):
    model = hmm.MultinomialHMM(n_components=columns['state'][0])
    model.transmat_ = transition_matrix
    model.emissionprob_ = emission_matrix
    model.startprob_ = initial_matrix

    model = model.fit(np.array(columns['symbol'][1]).reshape(-1,1))

    # Output a trained model to file for later use
    if dump_path is not None:
        with open(dump_path, 'wb') as outfile:
            pickle.Pickler(outfile).dump(model)
    
    return model

# Load a trained model from file for use
def load(load_path):
        with open(load_path, 'rb') as infile:
            return pickle.Unpickler(infile).load()

# Run a test data set through the specified model and compare to
# the predicted sequence to the actual sequence
def predict(model, columns):
    # prob goes unused, but could be used in other calculation methods
    prob, sequence = model.decode(np.array(columns['symbol'][1]).reshape(-1,1))
    difference = []
    for i in range(0, len(columns['state'][1])):
        # Compare predicted to actual
        if sequence[i] != columns['state'][1][i]:
            difference.append(False)
        else:
            difference.append(True)
    # return tuple of (actual, predicted, difference)
    return (columns['state'][1], sequence, difference)
    
# Run a test data set through the specified model and generate log
# log-likelyhood scores
def score(model, columns):
    # prob does unused, but could be used in other calculation methods
    prob, scores = model.score_samples(np.array(columns['symbol'][1]).reshape(-1,1))
    # Sequence is a num_samples x num_symbols array with probabilities
    # we therefore take the sum of the incorrect states to be the
    # probability of an anomaly, and the correct state to be the 
    # probability of a normal sample
    difference = []
    confidence = []
    for i in range(0, len(columns['state'][1])):
        # Compare predicted to actual
        print(scores[i,:])
        if scores[i, columns['state'][1][i]] >= 0.1: # 10% likelyhood
            difference.append(False)
            confidence.append(scores[i, columns['state'][1][i]])
        else:
            difference.append(True)
            confidence.append(0.9 - scores[i, columns['state'][1][i]])
            
    # return tuple of (actual, predicted, difference)
    return (columns['state'][1], difference, confidence)
    
# Generate models
def generate(power_samples, column_name, filter_type, dump_path=None):
    columns = extract(power_samples, column_name, filter_type)
    matrix_tuple = calculate(columns)
    model =  build(matrix_tuple[0], matrix_tuple[1], matrix_tuple[2], columns, dump_path)
    return (model, columns)
    
# Mark
def mark(power_samples, column_name, filter_type, load_path=None, model=None, method='predict'):
    if model is None:
        if load_path is None:
            raise ValueError
        model = load(load_path)
    columns = extract(power_samples, column_name, filter_type)
    if method == 'predict':
        return predict(model, columns)
    elif method == 'score':
        return score(model, columns)
    else:
        raise ValueError("Invalid mark method")
    
def main(argv):
    power_samples = Parse(argv[1])
    model, columns = generate(power_samples, 'global_intensity', 'day') ### Day is going to be day soon
    #test_samples = Parse(argv[2])
    result = mark(power_samples, 'global_intensity', 'day', None, model, method = 'predict')
    print(list(zip(result[1], result[2])))
    print(list(result[2]).count(True))
    print(list(result[2]).count(False))
    
if __name__ == '__main__':
    import sys
    main(sys.argv)   


