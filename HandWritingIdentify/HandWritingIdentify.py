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
    print(SortedCount)
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

    
#divide image into parts
def imagedivide(image):
    count_pixel = 0
    total_count_pixel = 0
    plainpoint = []
    isbreak = False
    (x,y) = image.size
    ImagePixel = [image.getpixel((w,h)) for h in range(y) for w in range(x)]
    total_count_pixel = sum(ImagePixel)
    MeanOfPixel = total_count_pixel / ( x * y )
    for t_x in range(x):
        for t_y in range(y):
            count_pixel += image.getpixel((t_x,t_y))
        MeanOfColPixel = count_pixel / y
        if MeanOfColPixel < MeanOfPixel:
            plainpoint.append(t_x)    
        count_pixel = 0
    b = []
    breakpoint = []
    for i in range(x):
        if i not in plainpoint and isbreak == False:
            b.append(i);isbreak = True
        if i not in plainpoint and isbreak == True:
            b.append(i)
        if i in plainpoint and isbreak == True:
            breakpoint.append(round(sum(b)/len(b)))
            b = [];isbreak = False
    breakpoint[0] = -1
    startandstop = []
    for i in range(len(breakpoint)):
        if i != len(breakpoint)-1:
            startandstop.append((breakpoint[i]+1,breakpoint[i+1]))
        else:
            startandstop.append((breakpoint[-1],x-1))
    return startandstop
    
    
    
    
    
    
    
    return breakpoint




#open and convert image
def opener(image_name):
    image = Image.open(image_name)
    image=image.convert("L")
    return image
    
    
    
    
    
    
#change sample into bins
def changeimage(image):
    resizeimage = image.resize((32,32),Image.ANTIALIAS)
    ImageList = [1 if resizeimage.getpixel((w,h)) < 127.5 else 0 for h in range(0,  32) for w in range(0, 32)]
    return np.array(ImageList)

    
    
    

#main function to  dispatch system
def main():  
    str = ""
    Dataset,Labels = trainingsetconstructor()
    image = opener("test3.jpg")  
    (x,y) = image.size
    breakpoints = imagedivide(image)
    print(breakpoints )
    for (a,b) in breakpoints:
        partofimage = image.crop((a,0,b+1,32))
        print(partofimage)
        partofimage.show()
        sample = changeimage(partofimage)
        str += classify(sample,Dataset,Labels,100)
    print(str)
        
if __name__ == "__main__":
    main()