import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import sys
import os, shutil
from os import listdir
from pathlib import Path
from PIL import Image
from matplotlib import image
from matplotlib import pyplot
inp = sys.argv[1]
df = pd.read_csv('eyewear_ml_challenge.csv')
from urllib.request import urlretrieve
images_dir = Path('Images').expanduser()
dim = (128,128)
X_image_train = []
df['present'] = False
print("Reached 1")
for fname in listdir(images_dir):
    ind = fname[:-4]
    df['present'][int(ind)] = True
    fpath = os.path.join(images_dir, fname)
    im = Image.open(fpath)
    im_resized = im.resize(dim)
    X_image_train.append(im_resized)
    # break

## Converting the image to numpy array
X_image_array=[]
for x in range(len(X_image_train)):
    X_image=np.array(X_image_train[x],dtype='uint8')
    X_image_array.append(X_image)
    # break
print("Reached 2")
# print(X_image_array[0].shape)
data = np.stack(X_image_array) 
data = data.reshape(len(data),-1)
data = data/255
# inp = 'dummy_pic.png'
dim = (128,128)
im = Image.open(fpath)
inp = im.resize(dim)
inp = np.array(inp,dtype='uint8')
inp = inp.reshape(1,-1)
inp = inp/255
from scipy.spatial import distance
d = []
cnt = 0
df['distance'] = 0.0
for i in range(0,len(data)):
  image1 = data[i]
  image2 = inp
  dist = distance.euclidean(image1,image2)
  d.append(dist)
  while(True):
    if(not df['present'][cnt]):
      cnt+=1
    else:
      break
  # print(str(dist) + " " + str(cnt))

  df['distance'][cnt] = dist
  cnt+=1
print("Reached 3")
df = df.loc[df['present'] == True]
df = df.sort_values('distance')
for i in range(0,10):
  url = df.iloc[i]['Image_Front']
  urlretrieve(url,'AnswerImages/' + str(i) + '.jpg')
print("Reached 4")
