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
import pylab

from imagegenerator import plot, draw, save
from casegenerator import getUniqueZBLLCases

#-------------------------
# Constants
#-------------------------

savePath = '../'

ocllCaseNames = {'0000': '0',
                 '0012': 'T',
                 '0021': 'U',
                 '0102': 'L',
                 '0111': 'A',
                 '0222': 'S',
                 '1122': 'P',
                 '1212': 'H'}
cpllCaseNames = {'0123': '0',
                 '0132': 'F',
                 '0321': 'D',
                 '0213': 'R',
                 '0231': 'L',
                 '0312': 'B'}

globalGenerateImages = False
globalGenerateSetImages = False

ocllImageSize = 128
collImageSize = 96
zbllImageSize = 64

#-------------------------
# Functions
#-------------------------

def getList(d):
    l = list(d.keys())
    l.sort()
    return l


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
                
                print(str(i)+'.\tSetting image for ',zbllName)

                path = 'images/' + coll + '/'
                if not os.access(savePath + path.split('/')[0], 0):
                    os.mkdir(savePath + path.split('/')[0])
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
    

def probFractionString(cases, maxCases):
    num = cases
    denom = maxCases
    i = num
    while i>1:
        while (num % i == 0) and (denom % i == 0):
            num = int(num/i)
            denom = int(denom/i)
        i-=1
    return str(num)+'/' +str(denom)
        
    
#-------------------------
# Main program
#-------------------------

def main():
    
    zblls = getUniqueZBLLCases()
    
    print(' Number of unique cases found:',len(zblls))
    
    sortedZBLLdict = sortCases(zblls)

    ocllImg, collImg, zbllImg = getImages(sortedZBLLdict, generateImages=globalGenerateImages, generateSetImages=globalGenerateSetImages)    
    ocllProbs, collProbs, zbllProbs = getProbablities(zblls) 

    
    if False:
        print('\n\n\n')
        l = list(ocllProbs.keys())
        l.sort()
        for p in l:
            print(p,round(ocllProbs[p]/77.76,2), probFractionString(ocllProbs[p],7776))
        print('\n\n\n')
        
        l = list(collProbs.keys())
        l.sort()
        for p in l:
            print(p,round(collProbs[p]/77.76,2), probFractionString(collProbs[p],7776))
    
    
    
    
    css = """
    html, body {
        font-family: Verdana;
        font-size: 8pt;
    }
    table {
        border-collapse: collapse;
        border: 2px solid #000;
    }
    td {
        border: 1px solid #000;
    }
    td {
        min-width: 90px;
        text-align: center;
        padding: 5px;
        font-size: 8pt;
    }
    td.sep {
        border: 2px solid #000;
        min-width: 2px;
        width: 2px;
        padding: 0;
    }
    """
    
    copyrightMsg = """
    Copyright &copy; 2015 Brendan Gray and Sylvermyst Technologies
    """
    
    i=0
    html = '<html><head><style>'+css+'</style></head><body><table>'
    oclls = getList(sortedZBLLdict)
    for ocll in oclls:
        colls = getList(sortedZBLLdict[ocll])
        html+="<tr><td>OCLL case: "+ocll+'<br/><img src="'+ocllImg[ocll]+'" width="'+str(ocllImageSize)+'px" />'
        html+="<br/>Probability: "+"{:.2f}".format(ocllProbs[ocll]/77.76)+"% ("+probFractionString(ocllProbs[ocll], 7776)+")</td><td><table>\n    "
        for coll in colls:
            html+="<tr><td>COLL case: "+coll+'<br/><img src="'+collImg[coll]+'" width="'+str(collImageSize)+'px" />'
            html+="<br/>Probability: "+"{:.2f}".format(collProbs[coll]/77.76)+"% ("+probFractionString(collProbs[coll], 7776)+')</td><td class="sep"> </td>\n        '
            for zbll in sortedZBLLdict[ocll][coll]:
                html+="<td>ZBLL case #"+str(i)+"<br/>"+zbll[0]+'<br/><img src="'+zbllImg[zbll[0]]+'" width="'+str(zbllImageSize)+'px" />'
                html+="<br/>Probability: "+"{:.2f}".format(zbllProbs[zbll[0]]/77.76)+"% ("+probFractionString(zbllProbs[zbll[0]], 7776)+")</td>\n        "
                i+=1
            html+="</td></tr>\n    "
        html += "</table></td></tr>"
    html += "</table>"
    html += "<p>"+copyrightMsg+"</p></body></html>"
    
    
    
    with open(savePath+"index.html", 'w') as outFile:
        outFile.write(html)


if __name__ == '__main__':
    main()
