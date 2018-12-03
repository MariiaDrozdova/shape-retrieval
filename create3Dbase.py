import sys
import os
from testSilhouettes import *
from randomSphereVectors import *

d = 20
centers0, directions0 = determineViewDirections(d)
iteration0 = 0
execute("models/m913.off", centers0, directions0, iteration0, ["models/m913.off"])
"""
models_list = os.listdir("models/")[163:164]
for i in range(len(models_list)):
	models_list[i] = 'models/' + models_list[i]
centers0, directions0 = determineViewDirections(d)
for i in range(len(models_list)):
	for iteration0 in range(d):
		execute(models_list[i], centers0, directions0, iteration0, models_list)
"""
