import librosa
import scipy.stats
import numpy as np
import glob


# get distance between two file representations
def euclidean_distance(row1, row2):

	return np.sqrt(np.sum(np.square(row1 - row2[:20])))

# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors):

	distances = list()
	for train_row in train:
		dist = euclidean_distance(test_row, train_row) # distance between test file and current train file
		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1]) # sort by distances
	neighbors = list()
	for i in range(num_neighbors):
		neighbors.append(distances[i][0]) # get the train file
	return neighbors


# Make a classification prediction with neighbors
def predict_classification(train, test_row, num_neighbors):

	neighbors = get_neighbors(train, test_row, num_neighbors) # the nearest neighbors
	output_values = [np.mean(row[-1]) for row in neighbors] # the neighbors targets
	prediction = max(set(output_values), key=output_values.count) # most frequent target
	return int(prediction)

# load audio file into mfcc sequence
def get_file_mfcc(f_path, digit):

	y , sr = librosa.load(f_path, sr=None) # audio time series and sampling rate
	mfcc = librosa.feature.mfcc(y=y, sr=sr) # mfcc sequence
	mfcc = scipy.stats.zscore (mfcc, axis=1) # Normalization
	if digit != -1: # train file
		mfcc = np.append(mfcc, [[digit]*mfcc.shape[1]], axis=0) # append to train file its value
	return mfcc

# load audio files to dataset
def load_training_data(array, digit, dataset):

	for i in range(len(array)):
		file = get_file_mfcc(array[i], digit)
		dataset.append(file)

def compare(predictions, targets):

	total = 0
	hits = 0
	all_ts = targets.readlines()
	all_ps = predictions.readlines()
	for target in all_ts:
		if target[43] != '0':
			total += 1
			for p in all_ps:
				if p == target:
					hits += 1
	return (hits/total)*100


dataset = []
ones = glob.glob("train_data/one/*.wav")
twos = glob.glob("train_data/two/*.wav")
threes = glob.glob("train_data/three/*.wav")
fours = glob.glob("train_data/four/*.wav")
fives = glob.glob("train_data/five/*.wav")
tests = glob.glob("test_files/*.wav")

load_training_data(ones, 1, dataset)
load_training_data(twos, 2, dataset)
load_training_data(threes, 3, dataset)
load_training_data(fours, 4, dataset)
load_training_data(fives, 5, dataset)

k = 1
output_file = open("output.txt", "w")
for i in range(len(tests)):
	file_name = tests[i]
	output_file.write(file_name[11:]+" - ")
	test_file = get_file_mfcc(tests[i], -1)
	prediction = predict_classification(dataset, test_file, k)
	output_file.write(str(prediction)+"\n")
output_file.close()
output_file = open("output.txt", "r")
targets = open("gold_output.txt", "r")
print("Accuracy is: "+str(compare(output_file, targets)))
output_file.close()
targets.close()





