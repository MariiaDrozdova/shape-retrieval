from gabor_feature import get_feature_vector
import cv2
import pickle
import os
from collections import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib
_k = 8
_n = 4
_samples = 16
_w0 = 0.13
_folder_views = "images/"
_n_clusters = 50
_model_adresse = 'kmeans.sav'
_histogram_adresse = "original_histograms.pickle"
_features_adresse = "original_features.pickle"
_sketch_name = "sketches/888.png"

def getAllViews():
    l = os.listdir(_folder_views)
    all_views = []
    for i in l:
        all_views.append(_folder_views + i)
    return all_views

def getAllViews():
    l = os.listdir(_folder_views)
    all_views = []
    for i in l:
        all_views.append(_folder_views + i)
    return all_views

def processDatabase():
    features = []
    features_per_objectview = []
    names = []
    basic_views = getAllViews()
    for basic_view in basic_views[:11]:
        sketch = cv2.Canny(cv2.imread(basic_view, 0), 100, 200)
        if np.sum(sketch) == 0:
            continue
        features_objectview = get_feature_vector(sketch, k=_k, n=_n, samples=_samples)
        features.extend(features_objectview )
        features_per_objectview.append(features_objectview)
        names.append(basic_view)
    kmeans = KMeans(n_clusters=_n_clusters, random_state=0).fit(features)
    joblib.dump(kmeans, _model_adresse)
    features_data = [features, features_per_objectview, names]
    with open(_features_adresse, 'wb') as f:
        pickle.dump(features_data, f)
    
def createHistogram(centers):
    h = Counter()
    for i in centers:
        h[i] += 1
    h = dict(sorted(h.items()))
    return h

def createHistograms(kmeans, names, features_per_objectview):
    histograms = []
    for i in range(len(features_per_objectview)):
        feature_objectview = features_per_objectview[i]
        h = createHistogram(kmeans.predict(feature_objectview))
        h['object'] = names[i]
        histograms.append(h)
    histograms.sort(key=lambda x: [(i, x[i]) for i in x.keys()])
    return histograms

def processSketchHistogram(h,N,f):
    hi_sum = np.sum(list(h.values())[:-1])
    print(hi_sum)
    print(N)
    print(f)
    for j in h.keys(): 
        if j == 'object':
            continue
        if f[j] != 0:
            h[j] = h[j]/hi_sum*np.log(N/f[j])
        else:
            h[j] = 0
    print(h.values())
    h_sum = np.sum(([i**2 for i in list(h.values())[:-1]]))
    print(h_sum)
    for j in h.keys():
        if j == 'object':
            continue
        h[j] = h[j]/h_sum
    return h
    
def saveHistograms(): 
    with open(_features_adresse, 'rb') as f:
        features_data = pickle.load(f)
    features_per_objectview = features_data[1]
    names = features_data[2]
    kmeans = joblib.load(_model_adresse)
    histograms = createHistograms(kmeans, names, features_per_objectview)
    N = len(histograms)
    f = np.zeros(kmeans.n_clusters)
    for h in histograms:
        for j in h.keys():
            print(j)
            if j == 'object':
                continue
            f[j] = (f[j] + 1)
    for j in range(len(histograms)):
        histograms[j] = processSketchHistogram(histograms[j],N,f)
    data = [histograms, N, f]
    with open(_histogram_adresse, 'wb') as f:
        pickle.dump(data, f)
        
def readHistograms():
    with open(_histogram_adresse, 'rb') as f:
        data = pickle.load(f)
    histograms = data[0]
    N = data[1]
    f = data[2]
    return histograms, N, f

def processSketch(N, f, sketch_name=_sketch_name):
    #sketch = cv2.Canny(cv2.imread(sketch_name, 0), 100, 200)
    sketch = cv2.imread(sketch_name, 0)
    features_sketch = get_feature_vector(sketch, k=_k, n=_n, samples=_samples)
    #example = np.random.random([_samples*_samples, _n**2*_k])
    kmeans = joblib.load(_model_adresse)
    histogram_for_sketch = createHistogram(kmeans.predict(features_sketch))
    print(histogram_for_sketch)
    processed_histogram_for_sketch = processSketchHistogram(histogram_for_sketch, N, f)
    return processed_histogram_for_sketch

def findSimilarity(h1, h2):
    res = 0
    for i in h1.keys():
        if i == 'object':
            continue
        try:
            res = res + h1[i]*h2[i]
        except KeyError:
            pass
    return res

def searchSimilarity(histograms, sketch_histogram):
    nearest = -1
    max_similarity = -1
    h_copy = histograms.copy()
    h_copy.sort(key=lambda x: findSimilarity(x, sketch_histogram))
    return(h_copy)
        
#processDatabase()
#saveHistograms()
histograms, N, f = readHistograms()
#print(histograms)
sketch_histogram = processSketch(N, f, 'images/m51_outfile_3.jpg')
print(sketch_histogram)
searchSimilarity(histograms, sketch_histogram)
#print(processSketch(N, f))
