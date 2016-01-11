'''
Created on 07 Jan 2016

    Copyright (c) 2016 Brendan Gray and Sylvermyst Technologies

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

from constants import *
from algtranslator import checkAndSplitAlg, getZBLLcase, NotZBLLError, getBaseAlg


def getAlgs(algFileName):
    algs = []
    with open(algFileName) as algfile:
        i = 0
        for line in algfile:
            i += 1
            rawalg = line.strip()
            if not rawalg: 
                continue
            ok, alg = checkAndSplitAlg(rawalg)        
            if not ok:
                print('ERROR on line '+str(i)+': '+alg+' in "'+rawalg+'"')                
            else:
                try:
                    getZBLLcase(alg)
                except NotZBLLError:                    
                    print('ERROR on line '+str(i)+': "'+getBaseAlg(rawalg)+'" does not result in a ZBLL case.')                
                algs.append(alg)
    return algs
                   
                    
def getCases(algs):
    recogisedCases = []
    for alg in algs:
        try:
            recogisedCases.append(getZBLLcase(alg))
        except NotZBLLError:
            print(alg)
        
    return recogisedCases
        
    



def main():
    algs = getAlgs(algFileName)
    for a in algs:
        print(a)
    
    print()
    
    cases = getCases(algs)
    for case in cases:
        print(case)


if __name__ == '__main__':
    main()