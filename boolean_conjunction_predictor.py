import numpy as np
import sys


def consistency_algorithm(X, Y, d):
    h0 = []
    for j in range(d):
        h0.append(1)  # activate xi
        h0.append(1)  # activate not(xi)
    h = h0
    num_of_examples = len(X)
    for k in range(num_of_examples):
        current_example = X[k]
        if Y[k] == 1 and get_prediction(h, current_example, d) == 0:
            for j in range(d):
                if current_example[j] == 1:
                    h[j + 1] = 0  # deactivate not(xi)
                if current_example[j] == 0:
                    h[j] = 0  # deactivate xi
    return h


# Given hypothesis h, input t and size - returns result of prediction:

def get_prediction(h, example, d):
    for i in range(d):
        if h[i] == 1 and example[i] == 0:
            return 0
        if h[i+1] == 1 and example[i] == 1:
            return 0
    return 1

# Given hypothesis h, size and file - writes h to file


def print_hypothesis(h, d, f):
    f.write("Hypothesis is: ")
    for i in range(d):
        if h[i] == 1:
            f.write("x"+str(i+1)+", ")
        elif h[i+1] == 1:
            f.write("not(x"+str(i+1)+"), ")


path = sys.argv[0]
training_examples = np.loadtxt("data.txt")
d = len(training_examples[0]) - 1  # size of input
X = (training_examples[:, 0:d])  # example inputs
Y = (training_examples[:, d])  # example labels
# print(X)
# print(Y)
h = consistency_algorithm(X, Y, d)
f = open("output.txt", "w")
print_hypothesis(h, d, f)
f.close()

