import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import optimize      
from PIL import Image
import PIL
import cv2
# pip install opencv-python         pip install pillow

# Arrays outside Loop
period, periodUncertainty = [],[]

# Plot Labellings
#plotTitles = ["Experiment 1: displacement of 5°, attempt 1.1","Experiment 1: displacement of 5°, attempt 1.2","Experiment 1: displacement of 5°, attempt 1.3","Experiment 1: displacement of 5°, attempt 1.4","Experiment 1: displacement of 10°, attempt 1.1","Experiment 1: displacement of 10°, attempt 1.2","Experiment 1: displacement of 15°, attempt 1.1","Experiment 1: displacement of 15°, attempt 1.2","Experiment 1: displacement of 15°, attempt 1.3","Experiment 1: displacement of 15°, attempt 1.4","Experiment 1: displacement of 20°, attempt 1.1","Experiment 1: displacement of 20°, attempt 1.2","Experiment 1: displacement of 20°, attempt 1.3","Experiment 1: displacement of 25°, attempt 1.1","Experiment 1: displacement of 25°, attempt 1.2","Experiment 1: displacement of 25°, attempt 1.3","Experiment 1: displacement of 25°, attempt 1.4"]
plotTitles,Number = ["Experiment 1: displacement of 10°, attempt 1.1"], 0

# File Locations
#filePath = "Lab/Term 2/2022.01.27 Not So Simple Pendulum - Computing/Videos/Trimmed/"
filePath = "Lab/Term 2/Pendulum Videos/deprecated-dark/o_5.mp4"
graphDirectory = "Lab/Term 2/Pendulum Graphs/"

# Adjust your font settings
titleFont = {'fontname':'Bodoni 72','size':13}
axesFont = {'fontname':'CMU Sans Serif','size':9}
ticksFont = {'fontname':'DM Mono','size':7}
errorStyle = {'mew':1,'ms':3,'capsize':3,'color':'blue','ls':''}
pointStyle = {'mew':1,'ms':3,'color':'blue'}
lineStyle = {'linewidth':0.5}

# Cropping Dimensions
x_min = 0                                     # left limit
x_max = 1280                                  # right limit
y_min = 0                                     # upper limit
y_max = 320                                   # lower limit
x_lim = x_max-x_min                           # total numbr of pixels in x direction
y_lim = y_max-y_min                           # total numbr of pixels in y direction
    
myvideo = cv2.VideoCapture(filePath)
numberframes = 0

while np.array(myvideo.read())[0]:
    numberframes += 1
myvideo=cv2.VideoCapture(filePath)
#print(numberframes)

# Define Functions
def read_vid():
    imageArray = np.array(myvideo.read())[1]
    return np.array(myvideo.read())[1]
def crop_image(imageArray,startx,endx,starty,endy):
    return imageArray[starty:endy,startx:endx,:]
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.3, 0.6, 0.1])

def coords():
    x,y = [],[]
    
    for i in range(0,y_lim):
        for j in range(0,x_lim):
            if white_bob[i][j]>0:
                x.append(j)
                y.append(i)

    x_ave,y_ave = np.mean(x),np.mean(y)
    Centre = x_ave,y_ave
    
    x_std,y_std = np.std(x),np.std(y)
    Std = x_std,y_std
    return x_ave,y_ave

# Cropping the Video
xx,yy,no_frames = [],[],0

for i in range(numberframes):
    no_frames+=1
    imageArray= np.array(myvideo.read())[1] #read_vid()
    #plt.imshow(imageArray);                                 # Use this code to see the image before cropping. If you are using Spyder in Anaconda, you should use PIL.Image.fromarray(imageArray).show() 
    cr_image = crop_image(imageArray,x_min,x_max,y_min,y_max)  #imageArray,startx,endx,starty,endy
    new_image = np.array(cr_image)
    #plt.imshow(new_image)                                    # Use this code to see the image after cropping.
    grey_image = rgb2gray(new_image)                               
    thresh, blackAndWhiteImage = cv2.threshold(grey_image, 180, 255,cv2.THRESH_BINARY)
    white_bob = np.array(blackAndWhiteImage)
    #plt.imshow(white_bob)                                    #You can use this code to see the black and white image.
    x2,y2 = coords()
    xx.append(x2)
    yy.append(y2)

frame=np.arange(0,no_frames)

# Showing the Plot
plt.plot(frame,xx,color='red')
plt.plot(frame,yy)
plt.xlabel("Frame Number", **axesFont)
plt.ylabel("Displacement", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title("Data for " + plotTitles[0], **titleFont)
plt.savefig(graphDirectory + 'plot - '+plotTitles[Number]+'.png', dpi=500)
plt.show()
plt.figure().clear()
plt.close()
plt.cla()
plt.clf()

# Sine Curve Fit
def sine_pendulum(frame, a, b, c, d):
    return a * np.sin(b * frame + c) + d

#p0=[232.5, 0.1963, -15, 567.5]
params,params_cov = optimize.curve_fit(sine_pendulum, frame, xx, p0=[500, 0.1964, -1.57, 500])
plt.plot(frame, sine_pendulum(frame, *params))
plt.plot(frame,xx)
plt.xlabel("Frame Number", **axesFont)
plt.ylabel("Displacement", **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.title("Sinusodial Curve Fit for " + plotTitles[Number], **titleFont)
plt.savefig(graphDirectory + 'curvefit - '+plotTitles[Number]+'.png', dpi=500)
plt.show()

plt.figure().clear()
plt.close()
plt.cla()
plt.clf()


# Print Optimised Parameters and Curve Fit
print("Output Data: " + plotTitles[Number])
print("Parameters: [a, b, c, d] in the expression A·sin(bx+c)+d")
print(params)
print("Covariance Matrix of Parameters")
print(params_cov)
T = 2*np.pi/(30*params[1])                              # convert b value into period T in seconds
unc_T = T*np.sqrt(params_cov[1,1])/np.sqrt(params[1])   # calculate absolute uncertainty in T
print(T,"±",unc_T,"seconds")

period.append(T)
periodUncertainty.append(unc_T)

plt.figure().clear()
plt.close()
plt.cla()
plt.clf()
