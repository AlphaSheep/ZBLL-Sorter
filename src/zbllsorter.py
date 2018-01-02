#!/usr/bin/python3
'''
ZBLL Case Sorter
Sorts all ZBLL cases for the last layer of a Rubik's cube.

Created on 03 Mar 2015

    Copyright (c) 2015 Brendan Gray and Sylvermyst Technologies

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

'''

import os
import json
import pylab

from casegenerator import getUniqueZBLLCases
from htmlgenerator2 import generateHTML
from imagegenerator import plot, save
from utilities import getList, probFractionString

from constants import *

#-------------------------
# Functions
#-------------------------


def sortCases(zblls):
    keys = list(zblls.keys())
    keys.sort()

    sortedZBLLdict = {}

    i=0
    for k in keys:
        [ocll, cpll, epll] = k.split(' ')

        ocllName = ocllCaseNames[ocll]
        collName = ocllName+cpllCaseNames[cpll]
        zbllName = collName+'-'+epll

        print(str(i)+'.\tFound new case: ', ocllName+' : '+collName+'\t', k,'---', (len(zblls[k])))


        if not ocllName in sortedZBLLdict.keys():
            sortedZBLLdict[ocllName] = {}

        if not collName in sortedZBLLdict[ocllName].keys():
            sortedZBLLdict[ocllName][collName] = []

        sortedZBLLdict[ocllName][collName].append((zbllName, k))
        i+=1

    return sortedZBLLdict


def getImages(sortedZBLLdict, generateImages=True, generateSetImages=True):

    ocllImg = {}
    collImg = {}
    zbllImg = {}

    i=0
    for ocll in getList(sortedZBLLdict):
        isFirstOCLL = True
        for coll in getList(sortedZBLLdict[ocll]):
            isFirstCOLL = True
            for zbll in sortedZBLLdict[ocll][coll]:

                zbllName = zbll[0]

                # print(str(i)+'.\tSetting image for ',zbllName)

                path = 'images/' + coll + '/'
                if generateSetImages or generateImages:
                    if not os.access(savePath + path.split('/')[0], 0):
                        os.mkdir(savePath + path.split('/')[0])
                if generateImages:
                    if not os.access(savePath + path, 0):
                        os.mkdir(savePath + path)
                zbllfilename = path + zbllName + '.png'

                # Generate OCLL image
                if isFirstOCLL:
                    ocllfilename = "images/" + ocll + '.png'
                    if generateSetImages:
                        plot(zbll[1], stage="OCLL")
                        save(savePath + ocllfilename, size=ocllImageSize)
                    ocllImg[ocll] = ocllfilename
                    isFirstOCLL = False

                # Generate COLL image
                if isFirstCOLL:
                    collfilename = "images/"+coll+'.png'
                    if generateSetImages:
                        plot(zbll[1], stage="COLL")
                        save(savePath+collfilename, size=collImageSize)
                    collImg[coll] = collfilename
                    isFirstCOLL = False

                # Generate ZBLL image
                if generateImages:
                    plot(zbll[1])
                    save(savePath+zbllfilename, size=zbllImageSize)

                zbllImg[zbllName] = zbllfilename
                i=i+1

    return ocllImg, collImg, zbllImg


def getProbablities(zblls):

    keys = list(zblls.keys())
    keys.sort()
    ocllProbs = {}
    collProbs = {}
    zbllProbs = {}

    for k in keys:
        [ocll, cpll, epll] = k.split(' ')

        ocllName = ocllCaseNames[ocll]
        collName = ocllName+cpllCaseNames[cpll]
        zbllName = collName+'-'+epll

        if not ocllName in ocllProbs.keys():
            ocllProbs[ocllName] = len(zblls[k])
        else:
            ocllProbs[ocllName] += len(zblls[k])

        if not collName in collProbs.keys():
            collProbs[collName] = len(zblls[k])
        else:
            collProbs[collName] += len(zblls[k])
        if not zbllName in zbllProbs.keys():
            zbllProbs[zbllName] = len(zblls[k])
        else:
            zbllProbs[zbllName] += len(zblls[k])

    return ocllProbs, collProbs, zbllProbs

def dumpZbllJson(zbllDict):
    zbllNameDict = {}
    for ocll in zbllDict.keys():
        zbllNameDict[ocll] = {}
        for coll in zbllDict[ocll].keys():
            zbllNameDict[ocll][coll] = []
            for zbll in zbllDict[ocll][coll]:
                zbllNameDict[ocll][coll].append(zbll[0])
    with open(savePath+"zblls.json",'w') as zblljson:
        json.dump(zbllNameDict, zblljson, indent=2)

#-------------------------
# Main program
#-------------------------

def main():

    zblls = getUniqueZBLLCases()
    sortedZBLLdict = sortCases(zblls)
    
    print(' Number of unique cases found:',len(zblls))

    ocllImg, collImg, zbllImg = getImages(sortedZBLLdict, generateImages=globalGenerateImages, generateSetImages=globalGenerateSetImages)    
    ocllProbs, collProbs, zbllProbs = getProbablities(zblls) 

    
    html = generateHTML(sortedZBLLdict, ocllProbs, collProbs, zbllProbs, ocllImg, collImg, zbllImg)
    
    with open(savePath+"index.html", 'w') as outFile:
        outFile.write(html)
    dumpZbllJson(sortedZBLLdict)


if __name__ == '__main__':
    main()
