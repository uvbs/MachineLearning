#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:22:02 2016

@author: loner
"""
import numpy as np
import os
from PIL import Image
#apply knn to handwriting identify system


#set up KNN system
def classify(sample,dataset,labels,k):
    DatasetRows = dataset.shape[0]
    DifferentOfMtrix = np.tile(sample,(DatasetRows,1)) - dataset
    SquareOfDifferentOfMtrix = DifferentOfMtrix**2
    SquareOfDistance = SquareOfDifferentOfMtrix.sum(axis=1)
    Disatance = SquareOfDistance**0.5
    SortedIndex = Disatance.argsort()
    CountOfLabel = {}
    for i in range(k):
        label = labels[SortedIndex[i]]
        CountOfLabel[label] = CountOfLabel.get(label,0) + 1
    SortedCount = sorted(CountOfLabel.items(), key=lambda d:d[1], reverse=True)
    return SortedCount[0][0]

#open training set
def trainingsetopener(filename):
    f = open('trainingDigits/%s' % filename)
    lines = []
    for line in f.readlines():
        lines.append(line.strip())
    datastring = "".join(lines)
    datalist = list(map(int,list(datastring)))
    return datalist,filename[0]

#construct trainingset
def trainingsetconstructor():
    filelist = os.listdir('trainingDigits')
    dataset = []
    labels = []
    for f in filelist:
        datalist,label = trainingsetopener(f)
        dataset.append(datalist)
        labels.append(label)
    return np.array(dataset),labels

#open and trans sample
def sample_function(image_name):
    image = Image.open(image_name)
    image=image.convert("L")
    resizeimage = image.resize((32,32),Image.ANTIALIAS)
    ImageList = [1 if resizeimage.getpixel((w,h)) < 127.5 else 0 for h in range(0,  32) for w in range(0, 32)]
    return np.array(ImageList)

#main function to  dispatch system
def main():
    Dataset,Labels = trainingsetconstructor()
    sample = sample_function("test.jpg")
    print(classify(sample,Dataset,Labels,20))
    
if __name__ == "__main__":
    main()