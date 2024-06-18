#!/usr/bin/python3
'''
Created on 12 July 2019

    Copyright (c) 2019 Brendan Gray and Sylvermyst Technologies

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
from algreader import getAlgs, getCases

def getLineNumbersAndLabels():
    algs, rawalgs, lineNumbers = getAlgs(algFileName)
    cases = getCases(algs)

    return lineNumbers, cases

def labelAlgs(lineNumbers, cases):
    with open(algFileName+"_temp", 'w') as tempFile:
        with open(algFileName) as algfile:
            lineNumber = 0
            for line in algfile:
                lineNumber += 1

                newLine = line

                if (lineNumber in lineNumbers):
                    case = cases[lineNumbers.index(lineNumber)]

                    if (case not in line):
                        whitespaceLength = 72 - len(line)
                        whitespaceLength = max(whitespaceLength, 6)
                        newLine = line[:-1] + (' '*whitespaceLength) + '# ' + case + '\n'

                tempFile.write(newLine)


if __name__=="__main__":
    lineNumbers, cases = getLineNumbersAndLabels()

    labelAlgs(lineNumbers, cases);
