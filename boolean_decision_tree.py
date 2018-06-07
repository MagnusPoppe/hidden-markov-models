import pandas as pd
from math import log2

_TRAINING_FILE = "/Users/magnus/Downloads/data/training.csv"
_TESTING_FILE = "/Users/magnus/Downloads/data/test.csv"

def entropy(V):
    """ ENTROPY SHOWS HOW MUCH OF THE TOTAL DECSISION SPACE AN ATTRIBUTE TAKES UP """
    return - sum(vk * log2(vk) for vk in V if vk > 0)

def remainder(attribute, examples):
    """ REMAINDER EXPLAINS HOW MUCH IS UNDECIDED AFTER AN ATTRIBUTE IS SET """
    remain = 0
    p, n = len(examples[examples['CLASS'] == 1]), len(examples[examples['CLASS'] == 2])
    for k in examples[attribute].unique():
        ex = examples[[attribute, 'CLASS']][examples[attribute] == k]
        pk, nk = len(ex[ex['CLASS'] == 1]), len(ex[ex['CLASS'] == 2])
        remain += ((pk + nk) / (p + n)) * entropy([pk / (pk + nk), nk / (pk + nk)])
    return remain

def importance(attribute, examples):
    """ INFORMATION GAIN FORMULA """
    p = len(examples[attribute][examples['CLASS'] == 1])
    n = len(examples[attribute][examples['CLASS'] == 2])
    return entropy([p/(p+n), n/(p+n)]) - remainder(attribute, examples)

def plurality(examples):
    return 1 if len(examples['CLASS'][examples['CLASS'] == 1]) > len(examples['CLASS']) / 2 else 2

def decision_tree(examples, attributes, parent_examples):
    """ CREATES A DECISION TREE BASED ON A SET OF EXAMPLES AND ATTRIBUTES. """
    if examples.empty:                   return plurality(parent_examples)
    elif (examples['CLASS'] == 1).all(): return 1
    elif (examples['CLASS'] == 2).all(): return 2
    elif attributes.empty:               return plurality(examples)
    
    rating = [importance(a, examples) for a in attributes]
    A = attributes[rating.index(max(rating))]
    node = {A: {}}
    for k in examples[A].unique():
        node[A][k] = decision_tree(examples[examples[A] == k], attributes.drop(A), examples)
    return node

def classify(tree, example):
    attr = list(tree.keys())[0]
    res = tree[attr][example[attr]]
    if isinstance(res, dict):
        return classify(res, example)
    else:
        return res
    

if __name__ == "__main__":
    # Load datasets:
    training = pd.read_csv(_TRAINING_FILE, header=0)
    testing = pd.read_csv(_TESTING_FILE, header=0)

    # Build tree:
    tree = decision_tree(training, training.columns[:-1], None)
    
    # Test by classifying each dataset:
    for name, data in {"train":training, "test": testing}.items():
        correct = 0
        for _, example in data.iterrows():
            classification = example['CLASS']
            result = classify(tree, example.drop('CLASS'))
            correct += 1 if result == classification else 0
        print("Accuracy on", name, "set:\t", correct / len(data))