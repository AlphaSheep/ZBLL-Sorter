#!/usr/bin/python3
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
from algtranslator import checkAndSplitAlg, getZBLLcase, \
    getInitialAUF, NotZBLLError, getBaseAlg, getZBLLCaseName


def getAlgs(algFileName):
    algs = []
    rawalgs = []
    lineNumbers = []
    with open(algFileName) as algfile:
        lineNumber = 0
        for line in algfile:
            rawalg = line.strip()
            lineNumber += 1
            if not rawalg or rawalg[0] == '#':
                continue
            ok, alg = checkAndSplitAlg(rawalg)
            if not ok:
                print('ERROR on line '+str(lineNumber)+': '+alg+' in "'+rawalg+'"')
            else:
                try:
                    case = getZBLLcase(alg)
                    auf = getInitialAUF(alg)
                    algs.append(alg)
                    rawalgs.append(auf + rawalg)
                    lineNumbers.append(lineNumber)

                except NotZBLLError:
                    print('ERROR on line '+str(lineNumber)+': "'+getBaseAlg(rawalg)+'" does not result in a ZBLL case.')
    return algs, rawalgs, lineNumbers


def getCases(algs):
    recogisedCases = []
    for alg in algs:
        try:
            recogisedCases.append(getZBLLCaseName(getZBLLcase(alg)))
        except NotZBLLError:
            print(alg)

    return recogisedCases


def readKnownCases():
    algs, rawalgs, lineNumbers = getAlgs(algFileName)
    print(len(algs), 'algorithms read\n')
    cases = getCases(algs)

    algsDict = {}
    for i in range(len(cases)):
        if cases[i] in algsDict.keys():
            print('Duplicate: ', algsDict[cases[i]], ' --and--', rawalgs[i])
        algsDict[cases[i]] = rawalgs[i]
    return algsDict



def main():
    algs = readKnownCases()
    count = 0
    for case in sorted(algs.keys()):
        count += 1
        print('{:.0f}.\t'.format(count), case, algs[case])


if __name__ == '__main__':
    main()
