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

savePath = '../'

cornerTwistSet = [0, 1, 2]    # 0: oriented; 1: twisted clockwise; 2: twisted anticlockwise
cornerPermSet = [0, 1, 2, 3]  # 0: UBL, 1: UBR, 2: UFR, 3: UFL
edgePermSet = [0, 1, 2, 3]    # 0: UB, 2: UR, 3: UF, 4: UL


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

generateImages = True

ocllImageSize = 128
collImageSize = 96
zbllImageSize = 64

def getOCLLcases():
    cases = []
    for ct1 in cornerTwistSet:
        for ct2 in cornerTwistSet:
            for ct3 in cornerTwistSet:
                # Set last corner twist such that sum of corner twists is multiple of 3. 
                ct4 = (6-ct1-ct2-ct3)%3 
                cases.append([ct1, ct2, ct3, ct4])
    return cases


def getCPLLcases():
    cases = []
    for cp1 in cornerPermSet:
        for cp2 in cornerPermSet:
            if cp2==cp1:
                continue
            for cp3 in cornerPermSet:
                if cp3==cp2 or cp3==cp1:
                    continue
                # The last corner must be the only remaining corner
                cp4 = 6-cp1-cp2-cp3
                cases.append([cp1, cp2, cp3, cp4])
    return cases


def getEPLLCases():
    cases = []
    for ep1 in edgePermSet:
        for ep2 in edgePermSet:
            if ep2==ep1:
                continue
            for ep3 in cornerPermSet:
                if ep3==ep2 or ep3==ep1:
                    continue
                # The last edge must be the only remaining edge
                ep4 = 6-ep1-ep2-ep3
                cases.append([ep1, ep2, ep3, ep4])    
    return cases
    
    
def calcParity(perm):
    # Count inversions
    # That is, the minimum number of swaps required to correctly permute the pieces
    p = perm[:]
    inversions = 0
    for i in range(3):
        for j in range(i+1, 4):
            if p[i]>p[j]:
                #p[i], p[j] = p[j], p[i]
                inversions += 1
    return inversions
                                

def getZBLLCases():
    cases = []
    for ocll in getOCLLcases():
        for cpll in getCPLLcases():
            for epll in getEPLLCases():
                parity = calcParity(cpll)+calcParity(epll)
                if parity % 2==0:
                    cases.append(ocll+cpll+epll)
    return cases


def rotateCase(case):
    return [case[3],  case[0], case[1], case[2],
            case[7],  case[4], case[5], case[6],
            case[11], case[8], case[9], case[10]]


def prerotateCase(case):
    prerotated = case[:]
    for i in range(4,12):
        prerotated[i] = (prerotated[i]+1)%4
    return prerotated
        
        
def strCase(case):    
    s = ''
    for i in range(len(case)):
        s += str(case[i])
    return s[:4]+' '+s[4:8]+' '+s[8:]  
    
    
def getAllRotations(case):
    # Each case has 16 possible rotations - 4 possible AUFs before the case times 4 possible AUFs after the case.
    # These 16 will not be unique in many cases.
    cases = []
    preRotation = case[:]        
    for _ in range (4):
        preRotation = prerotateCase(preRotation)
        postRotation = preRotation[:]
        for _ in range(4):
            postRotation = rotateCase(postRotation)  
            cases.append(postRotation)
    return cases

        
def getUniqueCases(cases):
    uniqueCases = {}
    for case in cases:
        unique = True
        rotations = getAllRotations(case)
        for rot in rotations:
            if strCase(rot) in uniqueCases.keys():
                unique = False
                uniqueCases[strCase(rot)].append(strCase(case))
                break
        if unique:
            uniqueCases[strCase(case)] = [strCase(case)]
            
    return uniqueCases
            
def getList(d):
    l = list(d.keys())
    l.sort()
    return l


zblls = getZBLLCases()
zblls = getUniqueCases(zblls)

print(' Number of unique cases found:',len(zblls))

keys = list(zblls.keys())
keys.sort()

ocllProbs = {}
collProbs = {}
zbllProbs = {}

ocllImg = {}
collImg = {}

sortedZBLLdict = {}

i=0

for k in keys:
    [ocll, cpll, epll] = k.split(' ')
    
    ocllName = ocllCaseNames[ocll]
    collName = ocllName+cpllCaseNames[cpll]
    zbllName = collName+'-'+epll
    
    print(str(i)+'.\t', ocllName+' : '+collName+'\t', k,'---', (len(zblls[k])))
    
    path = savePath+'images/'+collName+'/'
    if not os.access(path,0):
        os.mkdir(path)
    filename = path+zbllName+'.png'
    
    if not ocllName in sortedZBLLdict.keys():
        sortedZBLLdict[ocllName] = {}
        filename = savePath+"images/"+ocllName+'.png'        
        if generateImages:
            plot(k, stage="OCLL")
            save(filename, size=ocllImageSize)
        ocllImg[ocllName] = filename
        
    if not collName in sortedZBLLdict[ocllName].keys():
        sortedZBLLdict[ocllName][collName] = []
        filename = savePath+"images/"+collName+'.png'        
        if generateImages:
            plot(k, stage="COLL")#, cornerCycle=True)
            save(filename, size=collImageSize)
        collImg[collName] = filename
        
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
    
    sortedZBLLdict[ocllName][collName].append((zbllName, filename, i))
    if generateImages:
        plot(k)#, edgeCycle=True)
        save(filename, size=zbllImageSize)
    i+=1


if False:
    print('\n\n\n')
    l = list(ocllProbs.keys())
    l.sort()
    for p in l:
        print(p,round(ocllProbs[p]/77.76,2))
    print('\n\n\n')
    
    l = list(collProbs.keys())
    l.sort()
    for p in l:
        print(p,round(collProbs[p]/77.76,2))


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


i=0
html = '<html><head><style>'+css+'</style></head><body><table>'
oclls = getList(sortedZBLLdict)
for ocll in oclls:
    colls = getList(sortedZBLLdict[ocll])
    html+="<tr><td>OCLL case: "+ocll+'<br/><img src="'+ocllImg[ocll]+'" width="'+str(ocllImageSize)+'px" />'
    html+="<br/>Probability: "+"{:.2f}".format(ocllProbs[ocll]/77.76)+"%</td><td><table>"
    for coll in colls:
        html+="<tr><td>COLL case: "+coll+'<br/><img src="'+collImg[coll]+'" width="'+str(collImageSize)+'px" />'
        html+="<br/>Probability: "+"{:.2f}".format(collProbs[coll]/77.76)+'%</td><td class="sep"> </td>'
        for zbll in sortedZBLLdict[ocll][coll]:
            html+="<td>ZBLL case #"+str(i)+"<br/>"+zbll[0]+'<br/><img src="'+zbll[1]+'" width="'+str(zbllImageSize)+'px" />'
            html+="<br/>Probability: "+"{:.2f}".format(zbllProbs[zbll[0]]/77.76)+"%</td>"
            i+=1
        html+="</td></tr>"
    html += "</table></td></tr>"
html += "</table></body></html>"


with open(savePath+"index.html", 'w') as outFile:
    outFile.write(html)
