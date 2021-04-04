import numpy as np
import glob
import pandas as pd
import graphviz as gv
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/graphviz-2.38/release/bin/'

def read_dataset(path):
    file = open(path, "r")
    names = []
    dataset = []
    lines = file.readlines()
    for line in lines:
        string = str(line)
        if string.startswith("##"):
            split = string.split(",")
            names.append(split[1])
        elif string.startswith("%%") is not True and string.startswith("//") is not True:
            index = 0
            dictionary = dict()
            for category in names:
                dictionary[category] = string[index]
                index += 2
            dictionary["class"] = string[index]
            dataset.append(dictionary)
    return pd.DataFrame(dataset)

def entropy(target_col):
    """
    Calculate the entropy of a dataset.
    The only parameter of this function is the target_col parameter which specifies the target column
    """
    elements,counts = np.unique(target_col,return_counts = True)
    entropy = np.sum([(-counts[i]/np.sum(counts))*np.log2(counts[i]/np.sum(counts)) for i in range(len(elements))])
    return entropy

def InfoGain(data, split_attribute_name, target_name="class"):
    """
    Calculate the information gain of a dataset. This function takes three parameters:
    1. data = The dataset for whose feature the IG should be calculated
    2. split_attribute_name = the name of the feature for which the information gain should be calculated
    3. target_name = the name of the target feature. The default for this example is "class"
    """
    # Calculate the entropy of the total dataset
    total_entropy = entropy(data[target_name])

    ##Calculate the entropy of the dataset

    # Calculate the values and the corresponding counts for the split attribute
    vals, counts = np.unique(data[split_attribute_name], return_counts=True)

    # Calculate the weighted entropy
    Weighted_Entropy = np.sum(
        [(counts[i] / np.sum(counts)) * entropy(data.where(data[split_attribute_name] == vals[i]).dropna()[target_name])
         for i in range(len(vals))])

    # Calculate the information gain
    Information_Gain = total_entropy - Weighted_Entropy
    return Information_Gain, Weighted_Entropy

def decision_tree_build(data, total_data, features, target_name="class", parent_class = None):
    if len(np.unique(data[target_name])) <= 1:
        return np.unique(data[target_name])[0]
    elif len(data)==0:
        return np.unique(total_data[target_name])[np.argmax(np.unique(total_data[target_name],return_counts=True)[1])]
    elif len(features) == 0:
        return parent_class
    else:
        # Set the default value for this node --> The mode target feature value of the current node
        parent_class = np.unique(data[target_name])[
            np.argmax(np.unique(data[target_name], return_counts=True)[1])]

        # Select the feature which best splits the dataset
        item_values = []
        entropies = []
        for feature in features:
            item_val, entropy_val = InfoGain(data, feature, target_name)
            item_values.append(item_val)
            entropies.append(entropy_val)
            # Return the information gain values for the features in the dataset
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]

        # Create the tree structure. The root gets the name of the feature (best_feature) with the maximum information
        # gain in the first run
        node = best_feature+",Info Gain: "+str(round(max(item_values),5))+",Entropy: "+str(round(min(entropies),5))
        tree = {best_feature: {}}
        # infoTree = {node: {}}

        # Remove the feature with the best inforamtion gain from the feature space
        features = [i for i in features if i != best_feature]

        # Grow a branch under the root node for each possible value of the root node feature

        for value in np.unique(data[best_feature]):
            value = value
            # Split the dataset along the value of the feature with the largest information gain and therwith create sub_datasets
            sub_data = data.where(data[best_feature] == value).dropna()

            # Call the ID3 algorithm for each of those sub_datasets with the new parameters --> Here the recursion comes in!
            subtree = decision_tree_build(sub_data, total_data, features, target_name, parent_class)

            # Add the sub tree, grown from the sub_dataset to the tree under the root node
            tree[best_feature][value] = subtree
            # infoTree[node][value] = subInfoTree

        return tree

def plot_tree(tree, g):
    if type(tree) is not dict:
        g.node(tree)
    else:
        keys = tree.keys()
        for key in keys:
            g.node(key)
            values = tree[key]
            if len(values) > 1:
                for val in values:
                    plot_tree(val, g)
            else:
                g.node(values[0])
                g.edge(key, values, label=values[0][0])
    g.view()

def predict(query,tree,default = "B"):
    for key in list(query.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]]
            except:
                return default
            result = tree[key][query[key]]
            if isinstance(result, dict):
                return predict(query, result)
            else:
                return result

def print_accuracy(data, tree):
    queries = data.iloc[:,:-1].to_dict(orient = "records")
    # Create a empty DataFrame in whose columns the prediction of the tree are stored
    predicted = pd.DataFrame(columns=["predicted"])
    # Calculate the prediction accuracy
    for i in range(len(data)):
        predicted.loc[i, "predicted"] = predict(queries[i], tree, "B")
    print('The prediction accuracy is: ', (np.sum(predicted["predicted"] == data["class"]) / len(data)) * 100, '%')


array = read_dataset("train.txt")
tree = decision_tree_build(array,array,array.columns[:-1])
print(tree)
# g = gv.Digraph("decision_tree", "plot.png")
test = read_dataset("test.txt")
print_accuracy(test,tree)
# plot_tree(tree,g)

