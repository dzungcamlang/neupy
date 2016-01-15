from operator import itemgetter

import numpy as np
from sklearn import datasets, grid_search
from sklearn.cross_validation import train_test_split
from neupy import algorithms


np.random.seed(0)


def rmsle(actual, expected):
    count_of = expected.shape[0]
    square_logarithm_difference = np.log((actual + 1) / (expected + 1)) ** 2
    return np.sqrt((1 / count_of) * np.sum(square_logarithm_difference))


def scorer(network, X, y):
    result = network.predict(X)
    return rmsle(result, y)


def report(grid_scores, n_top=3):
    scores = sorted(grid_scores, key=itemgetter(1), reverse=False)
    for i, score in enumerate(scores[:n_top]):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


dataset = datasets.load_diabetes()
x_train, x_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, train_size=0.7
)

grnnet = algorithms.GRNN(std=0.5, verbose=True)
grnnet.train(x_train, y_train)
error = scorer(grnnet, x_test, y_test)
print("GRNN RMSLE = {:.3f}\n".format(error))

print("Run Random Search CV")
grnnet.verbose = False
random_search = grid_search.RandomizedSearchCV(
    grnnet,
    param_distributions={'std': np.arange(1e-2, 1, 1e-4)},
    n_iter=400,
    scoring=scorer,
)
random_search.fit(dataset.data, dataset.target)
report(random_search.grid_scores_)
