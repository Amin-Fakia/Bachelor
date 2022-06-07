import os
import cv2

import glob
dir_path = os.path.dirname(os.path.realpath(__file__))
image_folder=f"{dir_path }/vedoVideo/"

list = os.listdir(image_folder) # dir is your directory path
number_files = len(list)
print(number_files)

img_array = []
for i in range(number_files-1):
    img = cv2.imread(f"{image_folder}/{i}.png")
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()