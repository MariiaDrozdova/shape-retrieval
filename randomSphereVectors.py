import random
import math
import numpy as np

def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, n_dontknow = tuple([int(s) for s in file.readline().strip().split(' ')])
    n_verts = n_verts
    n_faces = n_faces
    verts = []
    faces = []
    for i_vert in range(n_verts):
        verts.append([])
        for s in file.readline().strip().split(' '):
            if len(s) > 0:
                verts[i_vert].append(float(s))
    for i_face in range(n_faces):
        faces.append([])
        try:
            for s in file.readline().strip().split(' ')[1:]:
                if len(s) > 0:
                    faces[i_face].append(int(s))
        except:
            for s in file.readline().strip().split('\t')[1:]:
                if len(s) > 0:
                    faces[i_face].append(int(s))
    return verts, faces

def dist(p1, p2):
	assert(len(p1)==len(p2))
	distance = 0
	for i in range(len(p1)):
		distance = distance + (p1[i]-p2[i])**2
	return np.sqrt(distance)

def sum(p1, p2):
	assert(len(p1)==len(p2))
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = p1[i] + p2[i]
	return res

def opp(p1):
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = -p1[i]
	return res

def div(p1, a):
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = p1[i]/a
	return res

class Sphere:
	def __init__(self, d, centers=None, verts=None, faces=None, ):
		if verts is None:
			self.verts, self.faces = read_off(open("../models/sphere2.off"))
		else:
			self.verts = verts
			self.faces = faces
		if centers is None:
			self.d = d
			self.centers = []
			numbers = []
			while (len(numbers) < d):
				r = random.randint(0, len(self.verts)-1)
				if r not in numbers:
					numbers.append(r)
			for i in numbers:
				self.centers.append(self.verts[i])
		else:
				
			self.d = len(centers)
			self.centers = centers
		self.original_centers = self.centers.copy()
		self.energy = np.inf		
		res = [0]*3
		for i in self.verts:
			res = sum(res, i)
		
		res = div(res, len(self.verts))
		R = dist(sum(self.verts[0], opp(res)), [0,0,0])

	def createClusters(self):
		new_centers = [[0,0,0]]*self.d
		size_of_clusters = [0]*self.d
		new_energy = 0
		for i in range(len(self.verts)):
			vert_to_center_min = dist(self.verts[i], self.centers[0])
			center_n = 0
			for j in range(1, len(self.centers)):
				vert_to_center = dist(self.verts[i], self.centers[j])
				if (vert_to_center < vert_to_center_min):
					vert_to_center_min = vert_to_center
					center_n = j
			#print(new_centers[center_n])
			#print(self.verts[i])
			#print(vert_to_center_min)
			new_centers[center_n] = sum(new_centers[center_n], self.verts[i])
			size_of_clusters[center_n] = size_of_clusters[center_n] + 1
			new_energy = new_energy + vert_to_center_min

		for j in range(0, len(self.centers)):
			#print(size_of_clusters[j])
			new_centers[j] = div(new_centers[j],size_of_clusters[j])
		self.centers = new_centers
		self.energy = new_energy

	def findRelaxedClusters(self):
		current_energy = self.energy
		new_energy = -np.inf
		while (new_energy != current_energy):

			current_energy = self.energy

			self.createClusters()
			new_energy = self.energy
		


def generateRandomSphereVector():
	u = random.random()
	v = random.random()
	theta = 2* math.pi*u
	fi = math.acos(2*v-1)
	nx = math.cos(theta)*math.cos(fi)
	ny = math.cos(theta)*math.sin(fi)
	nz = math.sin(theta)
	return [nx, ny, nz]

def generateRandomSphereVectors(d):
	res = []
	for i in range(d):
		res.append(generateRandomSphereVector())
	return res

def determineViewDirections(d = 10):
	a = Sphere(d)
	a.findRelaxedClusters()
	return a.original_centers, a.centers
	#print(generateRandomSphereVectors(10))

