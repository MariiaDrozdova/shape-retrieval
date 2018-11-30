import sys
import os
from testSilhouettes import *
from randomSphereVectors import *

d = 8

for i in os.listdir("models/"):
	print(i)
centers0, directions0 = determineViewDirections(d)
for iteration0 in range(d):
	execute("models/m73.off", centers0, directions0, iteration0)
