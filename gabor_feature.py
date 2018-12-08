import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from skimage.filters import gabor_kernel

# by default, the sketch size is 600
# gabor filter 
def get_gabor_value(u, v, sigma_x, sigma_y, w0, theta):
    x = u* math.cos(theta)-v*math.sin(theta)
    y = u* math.sin(theta)+v*math.cos(theta)    
    res = math.exp(-2*(math.pi**2)*(((x-w0)**2)*sigma_x**2 + (y**2)*sigma_y**2))
    return res 

def get_gabor_filter(theta, side_length = 600, line_width = 0.02, lamb = 0.2, w = 0.13):
    sigma_x = line_width * w
    sigma_y = sigma_x / lamb 
    u = np.arange(-side_length/2, side_length/2)
    v = np.arange(-side_length/2, side_length/2)
    g = np.zeros([side_length,side_length])
    for i in range (side_length):
        for j in range (side_length):
            x = u[j]
            y = v[i]
            g[i][j] = get_gabor_value(x,y,sigma_x,sigma_y,w,theta)
    return g
    
def get_gabor_bank(imgpath, k = 8):
    thetas = np.linspace(0,math.pi, k+1)[:-1]
    index = 0
    for theta in thetas:
        g = get_gabor_filter(theta)
        index = index + 1 
        plt.savefig("%stheta=%02d.png" % (imgpath, index))

# gabor response 
# frequency method of the article 
def get_gabor_response1(theta, img, w0):
    img_fft = np.fft.fftshift(np.fft.fft2(img))
    g = get_gabor_filter(theta,w = w0)
    response_fft = np.multiply(img_fft,g)
    response = np.fft.ifft2(np.fft.ifftshift(response_fft))
    return np.abs(response)
# internal method of the skimage
def get_gabor_response2(theta,img,w0):
    kernel = gabor_kernel(w0, theta)
    new_img = cv2.filter2D(img,-1,np.real(kernel),borderType= cv2.BORDER_CONSTANT)
    return new_img

# feature extraction 
def get_feature_vector(image,k,n,samples):
    # k the number of orientation
    # image : the original image (gray,single-channel)
    # n: number of tails 
    # samples: samples*samples number of points to sample
    thetas = np.linspace(0,math.pi, k+1)[:-1]
    responses = []
    for theta in thetas:
        res_image =  get_gabor_response2(theta, image, 0.13)
        res_image = response_mask(res_image, image)
        responses.append(res_image)
    feature = []
    points = get_sampling_points(image.shape[0],image.shape[1],samples)
    for point in points:
        patch_feature = []
        for i in range(k):
            res_image = responses[i]
            res_feature = get_patch_response(res_image,point,n,ratio=0.2)
            patch_feature = patch_feature + res_feature
        if np.sum(patch_feature)!=0.0: 
            norm = np.sqrt(np.sum(np.multiply(patch_feature, patch_feature)))
            patch_feature = patch_feature/norm
            feature.append(patch_feature)
            #print(patch_feature)
    return feature
    
def get_single_direction_feature(image,tail):
    # image : the response image 
    # tail : the number of subdivision along one dimension
    h = image.shape[0]
    w = image.shape[1]
    h_len = int(h/tail)
    w_len = int(w/tail)
    response = []
    for i in range (tail):
        for j in range (tail):
            sub_image = image[i*h_len:(i+1)*h_len,j*w_len:(j+1)*w_len]
            sub_res = np.sum(sub_image)
            response.append(sub_res)
    return response
    
def response_mask(res_img, ori_img):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for i in range(ori_img.shape[0]):
        flag = False
        for j in range(ori_img.shape[1]):
            if ori_img[i][j]< 5:
                min_y = i
                flag = True
                break
        if flag:
            break
    for i in range(ori_img.shape[0]-1,-1,-1):
        flag = False
        for j in range(ori_img.shape[1]):
            if ori_img[i][j]< 5:
                max_y = i
                flag = True
                break
        if flag:
            break
    for i in range(ori_img.shape[1]):
        flag = False
        for j in range(ori_img.shape[0]):
            if ori_img[j][i]< 5:
                min_x = i
                flag = True
                break
        if flag:
            break
    for i in range(ori_img.shape[1]-1,-1,-1):
        flag = False
        for j in range(ori_img.shape[0]):
            if ori_img[j][i]< 5:
                max_x = i
                flag = True
                break
        if flag:
            break
    mask = np.zeros(ori_img.shape)
    mask[min_y:max_y,min_x:max_x] = 1
    return np.multiply(mask,res_img)

# sampling 
def get_sampling_points(h,w,n):
    x_sample = random.sample(range(0,w),n)
    y_sample = random.sample(range(0,h),n)
    return [[i,k] for i in x_sample for k in y_sample]

def get_patch_response(image,point,n,ratio=0.2):
    # image : masked image response 
    # n: number of tails 
    w = image.shape[1]
    h = image.shape[0]
    ratio_x = math.sqrt(ratio)
    patch_x = int(w * ratio_x) 
    patch_y = int(h * ratio_x)
    patch = np.zeros([patch_y,patch_x])
    # coordinates in the original image 
    img_x0 = max(0,int(point[0]-patch_x/2))
    img_x1 = min(w-1,int(point[0]+patch_x/2))
    img_y0 = max(0,int(point[1]-patch_y/2))
    img_y1 = min(h-1,int(point[1]+patch_y/2))
    # coordinates in the patch image 
    patch_x0 = int(patch_x/2 -(point[0]-img_x0))
    patch_x1 = int(patch_x/2 +(img_x1-point[0]))
    patch_y0 = int(patch_y/2 -(point[1]-img_y0))
    patch_y1 = int(patch_y/2 +(img_y1-point[1]))
    patch[patch_x0:patch_x1,patch_y0:patch_y1] = image[img_x0:img_x1,img_y0:img_y1]
    return get_single_direction_feature(patch,n)

""" 
image = cv2.imread("/Users/yingyu/INF574/images/m1004_outfile_1.jpg",cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(image,199,199)
edges = cv2.resize(edges, (600, 600), interpolation=cv2.INTER_CUBIC)
features = get_feature_vector(edges,8,4,12)
print(features)
print(len(features))
"""
