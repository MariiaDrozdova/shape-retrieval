import sys
import os
from testSilhouettes import *
from randomSphereVectors import *

d = 5

models_list = os.listdir("models/")
centers0, directions0 = determineViewDirections(d)
for iteration0 in range(d):
	execute("models/"+models_list[136], centers0, directions0, iteration0)
