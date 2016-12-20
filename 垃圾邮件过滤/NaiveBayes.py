# coding:utf-8
print "the algorithm is training.it may take a very long time.so,please,wait patiently."
import jieba
import re, os
import numpy as np
import datetime


def getdata(direction, label):
    datas = []
    labels = []
    for file_name in os.listdir(direction):
        m_file = direction + "/" + file_name
        tmp_set = set()
        with open(m_file, "r") as f:
            for line in f:
                wordlist = re.findall(u'[\u4E00-\u9FD5]', line.decode('gbk', 'ignore'))
                string = ''.join(wordlist)
                if len(string) > 0:
                    seg_list = jieba.cut(string)
                    [tmp_set.add(word) for word in seg_list]
        datas.append(list(tmp_set))
        labels.append(label)
    return datas, labels


def GetDataSet():
    SpamDatas, SpamLabels = getdata("spam", 1)
    HealthDatas, HealthLabels = getdata("health", 0)
    return SpamDatas + HealthDatas, SpamLabels + HealthLabels


def CreateVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def SetOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("The word: %s is not in my Vocabulary!" % word)
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = np.log(p1Num / p1Denom)
    p0Vect = np.log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive


def ClassifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


def GetTestData():
    testdatas = []
    filenames = []
    for file_name in os.listdir("test"):
        m_file = "test/" + file_name
        tmp_set = set()
        with open(m_file, "r") as f:
            for line in f:
                wordlist = re.findall(u'[\u4E00-\u9FD5]', line.decode('gbk', 'ignore'))
                string = ''.join(wordlist)
                if len(string) > 0:
                    seg_list = jieba.cut(string)
                    [tmp_set.add(word) for word in seg_list]
        testdatas.append(list(tmp_set))
        filenames.append(file_name)
    return testdatas, filenames


def NaiveBayes():
    listOPosts, listClasses = GetDataSet()
    myvocablist = CreateVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(SetOfWords2Vec(myvocablist, postinDoc))
    p0V, p1V, pAb = trainNB0(np.array(trainMat), np.array(listClasses))
    testdatas, filenames = GetTestData()
    with open("result", "w") as r:
        for i in range(len(testdatas)):
            newdata = np.array(SetOfWords2Vec(myvocablist, testdatas[i]))
            result = ClassifyNB(newdata, p0V, p1V, pAb)
            r.write(filenames[i] + " is classified as:" + str(result) + "\n")
    r.close()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    NaiveBayes()
    stop_time = datetime.datetime.now()
    print "This program started at:" + start_time.strftime("%b-%d-%y %H:%M") + "\nAnd stopped at:" + stop_time.strftime(
        "%y-%b-%d %H:%M") + "\nLast:" + str((stop_time - start_time).seconds) + " seconds"
