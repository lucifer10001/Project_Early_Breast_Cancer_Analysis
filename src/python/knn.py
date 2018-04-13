#!/usr/bin/env python3

#####################################################
##    WISCONSIN BREAST CANCER MACHINE LEARNING     ##
#####################################################
#
# Project by Raul Eulogio
#
# Project found at: https://www.inertia7.com/projects/3
#

"""
Kth Nearest Neighbor Classification
"""

import time
import sys, os
import pandas as pd
import helper_functions as hf
from helper_functions import training_set, class_set, test_set, test_class_set
from sklearn.neighbors import KNeighborsClassifier # Kth Nearest Neighbor
from sklearn.model_selection import cross_val_score # Cross validation
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating Area Under Curve for ROC's!
from sklearn.externals import joblib

# Fitting model
fit_knn = KNeighborsClassifier(n_neighbors=3)

# Training model
fit_knn.fit(training_set,
	class_set)

# Since KNN was first algorithm I included training set metrics
# to give context
# We predict the class for our training set
predictionsTrain = fit_knn.predict(training_set)

# Measure the accuracy based on the training set
accuracy_train = fit_knn.score(training_set,
	class_set)

train_error_rate = 1 - accuracy_train

# First we predict the Dx for the test set and call it predictions
predictions = fit_knn.predict(test_set)

# Test Set Metrics
test_crosstb_comp = pd.crosstab(index = test_class_set,
                           columns = predictions)

test_crosstb = test_crosstb_comp.as_matrix()

# Let's get the accuracy of our test set
accuracy = fit_knn.score(test_set,
	test_class_set)

test_error_rate = 1 - accuracy

predictions_prob_knn = fit_knn.predict_proba(test_set)[:, 1]

# ROC Curve and AUC Calculations
fpr, tpr, _ = roc_curve(test_class_set,
	predictions_prob_knn)

auc_knn = auc(fpr, tpr)

# Uncomment to save your model as a pickle object!
# joblib.dump(fit_knn, 'pickle_models/model_knn.pkl')

if __name__ == '__main__':

	print(fit_knn)

	# KNN Optimal K
	# Inspired by:
	# https://kevinzakka.github.io/2016/07/13/k-nearest-neighbor/

	myKs = []
	for i in range(0, 50):
		if (i % 2 != 0):
			myKs.append(i)

	cross_vals = []
	for k in myKs:
		knn = KNeighborsClassifier(n_neighbors=k)
		scores = cross_val_score(knn,
			training_set,
			class_set,
			cv = 10,
			scoring='accuracy')
		cross_vals.append(scores.mean())

	MSE = [1 - x for x in cross_vals]
	optimal_k = myKs[MSE.index(min(MSE))]
	print("Optimal K is {0}".format(optimal_k))

	# Here we create a matrix comparing the actual values
	# vs. the predicted values
	print(pd.crosstab(predictionsTrain,
		class_set,
		rownames=['Predicted Values'],
		colnames=['Actual Values']))

	print("Here is our accuracy for our training set:\n {0: .3f}"\
		.format(accuracy_train))

	print("The train error rate for our model is:\n {0: .3f}"\
		.format(train_error_rate))

	print('Cross Validation')

	hf.cross_val_metrics(fit_knn, training_set, class_set,
		print_results = True)

	# Let's compare the predictions vs. the actual values
	print(test_crosstb)

	# TEST ERROR RATE!!
	print("Here is our accuracy for our test set:\n {0: .3f}"\
		.format(accuracy))

	# Here we calculate the test error rate!
	print("The test error rate for our model is:\n {0: .3f}"\
		.format(test_error_rate))

else:
	def return_knn():
		'''
		Function to output values created in script
		'''
		return fpr, tpr, auc_knn, predictions, test_error_rate

	mean_cv_knn, std_error_knn = hf.cross_val_metrics(fit_knn,
		training_set,
		class_set,
		print_results = False)
