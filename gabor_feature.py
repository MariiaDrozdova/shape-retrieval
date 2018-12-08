import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
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
def get_gabor_response2(theta, img,w0):
    kernel = gabor_kernel(w0, theta)
    new_img = cv2.filter2D(image,-1,np.real(kernel),borderType= cv2.BORDER_CONSTANT)
    return new_img

# feature extraction 
def get_feature_vector(image,k,n, w0):
    # k the number of orientation
    # image : the original image (gray,single-channel)
    thetas = np.linspace(0,math.pi, k+1)[:-1]
    feature = []
    for theta in thetas:
        res_image =  get_gabor_response2(theta, image, w0)
        res_feature = get_single_direction_feature(res_image,n)
        feature = feature + res_feature
    norm = np.sqrt(np.sum(np.multiply(feature, feature)))
    feature = feature/norm
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
    