'''
Created on 06 Jan 2016

    Copyright (c) 2014 Brendan Gray and Sylvermyst Technologies

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


cornerTwistSet = [0, 1, 2]    # 0: oriented; 1: twisted clockwise; 2: twisted anticlockwise
cornerPermSet = [0, 1, 2, 3]  # 0: UBL, 1: UBR, 2: UFR, 3: UFL
edgePermSet = [0, 1, 2, 3]    # 0: UB, 2: UR, 3: UF, 4: UL


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
           

if __name__ == '__main__':
    pass