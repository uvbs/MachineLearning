#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 21:36:54 2016

@author: loner
"""
import matplotlib.pyplot as plt
import numpy as np
import random
class Clustering:
    def __init__(self,k):

        self.k = k
        f = open("DataSet","r")
        LngandLnt = []
        datasets = f.readlines()
        self.m = len(datasets)
        for data in datasets:
            XandY = data.strip().split("|")
            LngandLnt.append([float(XandY[0]),float(XandY[1])])
        self.dataset = np.array(LngandLnt)
        self.MeanNormalization()
        self.clusters = [self.NormalizedDataset[random.randint(0,self.m)] for _ in range(k)]

    def MeanNormalization(self):
        Means = sum(self.dataset)/self.m
        MeansArray = np.tile(Means,(self.m,1))
        self.NormalizedDataset = self.dataset - MeansArray

    def distance(self,cluster):
        ClusterArray = np.tile(cluster,(self.m,1))
        DiffArray = ClusterArray - self.NormalizedDataset
        SquareDiffArray = DiffArray**2
        SquareDistance = SquareDiffArray.sum(axis=1)
        return SquareDistance**(1/2)

    def GetNewCluster(self):
        self.ColorOfPoint = []
        distances = []
        ClusterPoint = {}
        ZoreArray = np.array([0.0,0.0])
        for j in range(self.k):
            ClusterPoint[j] = []
        for cluster in self.clusters:
            distances.append(self.distance(cluster))
        for i in range(self.m):
            a =[distances[j][i] for j in range(self.k)]
            idx = a.index(min(a))
            ClusterPoint[idx].append(i)
            self.ColorOfPoint.append(idx)

        for index in range(self.k):
            for args in ClusterPoint[index]:
                ZoreArray+=self.NormalizedDataset[args]
            self.clusters[index] = ZoreArray/len(ClusterPoint[index])
            ZoreArray = np.array([0.0,0.0])

    def KmeansMain(self):
        for i in range(50):
            self.GetNewCluster()
        self.DrawThePicture()

    def DrawThePicture(self):
        x = []
        y = []
        for i in self.clusters:
            x.append(i[0])
            y.append(i[1])
        plt.scatter(self.NormalizedDataset[:,0],self.NormalizedDataset[:,1],s=10,c=np.array(self.ColorOfPoint))
        plt.scatter(x,y,s=100,c="r",marker="+")
        plt.show()

if __name__ == '__main__':
    C = Clustering(4)
    C.KmeansMain()
