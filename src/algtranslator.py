#!/usr/bin/python3
'''
Rubik's cube algorithm translator.

A module for translating an algorithm expressed as a string into a series of moves,
and then applying those moves to obtain the final cube state.

Created on 05 Mar 2015

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

import copy

from imagegenerator import plot, draw
from casegenerator import strCase, getUniqueZBLLCases, getAllRotations
from utilities import getStringAfterSep
from constants import ocllCaseNames, cpllCaseNames

# Recognised move set:
# U, U', U2, R, R', R2, F, F', F2, L, L', L2, B, B', B2, D, D', D2,
# u, u', u2, r, r', r2, f, f', f2, l, l', l2, b, b', b2, d, d', d2,
# M, M', M2, E, E', E2, S, S', S2, x, x', x2, y, y', y2, z, z', z2

solvedCube = [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7,8,9,10,11], [0,1,2,3,4,5]]

# format: [corner orientations: UBL, UBR, UFR, UFL, DBL, DBR, DFR, DFL. 0 is oriented, 1 is twisted clockwise, 2 is twisted anticlockwise]
#         [corner permutations: UBL, UBR, UFR, UFL, DBL, DBR, DFR, DFL]
#         [edge orientations wrt z-axis: UB, UR, UF, UL, BL, BR, FR, FL, DB, DR, DF, DL. 0 is oriented in <R,U,L,D>, 1 is flipped in <R,U,L,D>.]
#         [edge permutations: UB, UR, UF, UL, BL, BR, FR, FL, DB, DR, DF, DL]
#         [center permutations: U, F, R, B, L, D]

# Note: Orientation is applied after permutation
# Numbers represent location that each piece moves to.
#                    CO                  CP                  EO                           EP                            Centers
movesDict = {
             "U" : [[0,0,0,0, 0,0,0,0], [1,2,3,0, 4,5,6,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [1,2,3,0, 4,5,6,7, 8,9,10,11], [0,1,2,3,4,5]], #
             "U2": [[0,0,0,0, 0,0,0,0], [2,3,0,1, 4,5,6,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [2,3,0,1, 4,5,6,7, 8,9,10,11], [0,1,2,3,4,5]], #
             "U'": [[0,0,0,0, 0,0,0,0], [3,0,1,2, 4,5,6,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [3,0,1,2, 4,5,6,7, 8,9,10,11], [0,1,2,3,4,5]], #
             "R" : [[0,1,2,0, 0,2,1,0], [0,5,1,3, 4,6,2,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,5,2,3, 4,9,1,7, 8,6,10,11], [0,1,2,3,4,5]], #
             "R2": [[0,0,0,0, 0,0,0,0], [0,6,5,3, 4,2,1,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,9,2,3, 4,6,5,7, 8,1,10,11], [0,1,2,3,4,5]], #
             "R'": [[0,1,2,0, 0,2,1,0], [0,2,6,3, 4,1,5,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,6,2,3, 4,1,9,7, 8,5,10,11], [0,1,2,3,4,5]], #
             "F" : [[0,0,1,2, 0,0,2,1], [0,1,6,2, 4,5,7,3], [0,0,1,0, 0,0,1,1, 0,0,1,0], [0,1,6,3, 4,5,10,2, 8,9,7,11], [0,1,2,3,4,5]], #
             "F2": [[0,0,0,0, 0,0,0,0], [0,1,7,6, 4,5,3,2], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,10,3, 4,5,7,6, 8,9,2,11], [0,1,2,3,4,5]], #
             "F'": [[0,0,1,2, 0,0,2,1], [0,1,3,7, 4,5,2,6], [0,0,1,0, 0,0,1,1, 0,0,1,0], [0,1,7,3, 4,5,2,10, 8,9,6,11], [0,1,2,3,4,5]], #
             "L" : [[2,0,0,1, 1,0,0,2], [3,1,2,7, 0,5,6,4], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,7, 3,5,6,11, 8,9,10,4], [0,1,2,3,4,5]], #
             "L2": [[0,0,0,0, 0,0,0,0], [7,1,2,4, 3,5,6,0], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,11, 7,5,6,4, 8,9,10,3], [0,1,2,3,4,5]], #
             "L'": [[2,0,0,1, 1,0,0,2], [4,1,2,0, 7,5,6,3], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,4, 11,5,6,3, 8,9,10,7], [0,1,2,3,4,5]], #
             "D" : [[0,0,0,0, 0,0,0,0], [0,1,2,3, 7,4,5,6], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,3, 4,5,6,7, 11,8,9,10], [0,1,2,3,4,5]], #
             "D2": [[0,0,0,0, 0,0,0,0], [0,1,2,3, 6,7,4,5], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,3, 4,5,6,7, 10,11,8,9], [0,1,2,3,4,5]], #
             "D'": [[0,0,0,0, 0,0,0,0], [0,1,2,3, 5,6,7,4], [0,0,0,0, 0,0,0,0, 0,0,0,0], [0,1,2,3, 4,5,6,7, 9,10,11,8], [0,1,2,3,4,5]], #
             "B" : [[1,2,0,0, 2,1,0,0], [4,0,2,3, 5,1,6,7], [1,0,0,0, 1,1,0,0, 1,0,0,0], [4,1,2,3, 8,0,6,7, 5,9,10,11], [0,1,2,3,4,5]], #
             "B2": [[0,0,0,0, 0,0,0,0], [5,4,2,3, 1,0,6,7], [0,0,0,0, 0,0,0,0, 0,0,0,0], [8,1,2,3, 5,4,6,7, 0,9,10,11], [0,1,2,3,4,5]], #
             "B'": [[1,2,0,0, 2,1,0,0], [1,5,2,3, 0,4,6,7], [1,0,0,0, 1,1,0,0, 1,0,0,0], [5,1,2,3, 0,8,6,7, 4,9,10,11], [0,1,2,3,4,5]], #

             "M" : [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [1,0,1,0,0,0,0,0,1,0,1,0], [2,1,10,3,4,5,6,7,0,9,8,11],[1,5,2,0,4,3]], #
             "M2": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [10,1,8,3,4,5,6,7,2,9,0,11],[5,3,2,1,4,0]], #
             "M'": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [1,0,1,0,0,0,0,0,1,0,1,0], [8,1,0,3,4,5,6,7,10,9,2,11],[3,0,2,5,4,1]], #
             "E" : [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,1,1,1,1,0,0,0,0], [0,1,2,3,5,6,7,4,8,9,10,11], [0,4,1,2,3,5]], #
             "E2": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [0,1,2,3,6,7,4,5,8,9,10,11], [0,3,4,1,2,5]], #
             "E'": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,1,1,1,1,0,0,0,0], [0,1,2,3,7,4,5,6,8,9,10,11], [0,2,3,4,1,5]], #
             "S" : [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,1,0,1,0,0,0,0,0,1,0,1], [0,9,2,1,4,5,6,7,8,11,10,3], [2,1,5,3,0,4]], #
             "S2": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [0,11,2,9,4,5,6,7,8,3,10,1], [5,1,4,3,2,0]], #
             "S'": [[0,0,0,0,0,0,0,0], [0,1,2,3,4,5,6,7], [0,1,0,1,0,0,0,0,0,1,0,1], [0,3,2,11,4,5,6,7,8,1,10,9], [4,1,0,3,5,2]], #


             "u" : [[0,0,0,0,0,0,0,0], [1,2,3,0,4,5,6,7], [0,0,0,0,1,1,1,1,0,0,0,0], [1,2,3,0,5,6,7,4,8,9,10,11], [0,4,1,2,3,5]], #
             "u2": [[0,0,0,0,0,0,0,0], [2,3,0,1,4,5,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [2,3,0,1,6,7,4,5,8,9,10,11], [0,3,4,1,2,5]], #
             "u'": [[0,0,0,0,0,0,0,0], [3,0,1,2,4,5,6,7], [0,0,0,0,1,1,1,1,0,0,0,0], [3,0,1,2,7,4,5,6,8,9,10,11], [0,2,3,4,1,5]], #
             "r" : [[0,1,2,0,0,2,1,0], [0,5,1,3,4,6,2,7], [1,0,1,0,0,0,0,0,1,0,1,0], [8,5,0,3,4,9,1,7,10,6,2,11], [3,0,2,5,4,1]], #
             "r2": [[0,0,0,0,0,0,0,0], [0,6,5,3,4,2,1,7], [0,0,0,0,0,0,0,0,0,0,0,0], [10,9,8,3,4,6,5,7,2,1,0,11], [5,3,2,1,4,0]], #
             "r'": [[0,1,2,0,0,2,1,0], [0,2,6,3,4,1,5,7], [1,0,1,0,0,0,0,0,1,0,1,0], [2,6,10,3,4,1,9,7,0,5,8,11], [1,5,2,0,4,3]], #
             "f" : [[0,0,1,2,0,0,2,1], [0,1,6,2,4,5,7,3], [0,1,1,1,0,0,1,1,0,1,1,1], [0,9,6,1,4,5,10,2,8,11,7,3], [2,1,5,3,0,4]], #
             "f2": [[0,0,0,0,0,0,0,0], [0,1,7,6,4,5,3,2], [0,0,0,0,0,0,0,0,0,0,0,0], [0,11,10,9,4,5,7,6,8,3,2,1], [5,1,4,3,2,0]], #
             "f'": [[0,0,1,2,0,0,2,1], [0,1,3,7,4,5,2,6], [0,1,1,1,0,0,1,1,0,1,1,1], [0,3,7,11,4,5,2,10,8,1,6,9], [4,1,0,3,5,2]], #
             "l" : [[2,0,0,1,1,0,0,2], [3,1,2,7,0,5,6,4], [1,0,1,0,0,0,0,0,1,0,1,0], [2,1,10,7,3,5,6,11,0,9,8,4], [1,5,2,0,4,3]], #
             "l2": [[0,0,0,0,0,0,0,0], [7,1,2,4,3,5,6,0], [0,0,0,0,0,0,0,0,0,0,0,0], [10,1,8,11,7,5,6,4,2,9,0,3], [5,3,2,1,4,0]], #
             "l'": [[2,0,0,1,1,0,0,2], [4,1,2,0,7,5,6,3], [1,0,1,0,0,0,0,0,1,0,1,0], [8,1,0,4,11,5,6,3,10,9,2,7], [3,0,2,5,4,1]], #
             "b" : [[1,2,0,0,2,1,0,0], [4,0,2,3,5,1,6,7], [1,1,0,1,1,1,0,0,1,1,0,1], [4,3,2,11,8,0,6,7,5,1,10,9], [4,1,0,3,5,2]], #
             "b2": [[0,0,0,0,0,0,0,0], [5,4,2,3,1,0,6,7], [0,0,0,0,0,0,0,0,0,0,0,0], [8,11,2,9,5,4,6,7,0,3,10,1], [5,1,4,3,2,0]], #
             "b'": [[1,2,0,0,2,1,0,0], [1,5,2,3,0,4,6,7], [1,1,0,1,1,1,0,0,1,1,0,1], [5,9,2,1,0,8,6,7,4,11,10,3], [2,1,5,3,0,4]], #
             "d" : [[0,0,0,0,0,0,0,0], [0,1,2,3,7,4,5,6], [0,0,0,0,1,1,1,1,0,0,0,0], [0,1,2,3,7,4,5,6,11,8,9,10], [0,2,3,4,1,5]], #
             "d2": [[0,0,0,0,0,0,0,0], [0,1,2,3,6,7,4,5], [0,0,0,0,0,0,0,0,0,0,0,0], [0,1,2,3,6,7,4,5,10,11,8,9], [0,3,4,1,2,5]], #
             "d'": [[0,0,0,0,0,0,0,0], [0,1,2,3,5,6,7,4], [0,0,0,0,1,1,1,1,0,0,0,0], [0,1,2,3,5,6,7,4,9,10,11,8], [0,4,1,2,3,5]], #


             "x" : [[2,1,2,1, 1,2,1,2], [4,5,1,0, 7,6,2,3], [1,0,1,0,0,0,0,0,1,0,1,0], [8,5,0,4,11,9,1,3,10,6,2,7], [3,0,2,5,4,1]], #
             "x2": [[0,0,0,0, 0,0,0,0], [7,6,5,4, 3,2,1,0], [0,0,0,0,0,0,0,0,0,0,0,0], [10,9,8,11,7,6,5,4,2,1,0,3], [5,3,2,1,4,0]], #
             "x'": [[2,1,2,1, 1,2,1,2], [3,2,6,7, 0,1,5,4], [1,0,1,0,0,0,0,0,1,0,1,0], [2,6,10,7,3,1,9,11,0,5,8,4], [1,5,2,0,4,3]], #

             "y" : [[0,0,0,0,0,0,0,0], [1,2,3,0,5,6,7,4], [0,0,0,0,1,1,1,1,0,0,0,0], [1,2,3,0,5,6,7,4,9,10,11,8], [0,4,1,2,3,5]], #
             "y2": [[0,0,0,0,0,0,0,0], [2,3,0,1,6,7,4,5], [0,0,0,0,0,0,0,0,0,0,0,0], [2,3,0,1,6,7,4,5,10,11,8,9], [0,3,4,1,2,5]], #
             "y'": [[0,0,0,0,0,0,0,0], [3,0,1,2,7,4,5,6], [0,0,0,0,1,1,1,1,0,0,0,0], [3,0,1,2,7,4,5,6,11,8,9,10], [0,2,3,4,1,5]], #

             "z" : [[1,2,1,2,2,1,2,1], [1,5,6,2,0,4,7,3], [1,1,1,1,1,1,1,1,1,1,1,1], [5,9,6,1,0,8,10,2,4,11,7,3], [2,1,5,3,0,4]], #
             "z2": [[0,0,0,0,0,0,0,0], [5,4,7,6,1,0,3,2], [0,0,0,0,0,0,0,0,0,0,0,0], [8,11,10,9,5,4,7,6,0,3,2,1], [5,1,4,3,2,0]], #
             "z'": [[1,2,1,2,2,1,2,1], [4,0,3,7,5,1,2,6], [1,1,1,1,1,1,1,1,1,1,1,1], [4,3,7,11,8,0,2,10,5,1,6,9], [4,1,0,3,5,2]] #
            }


ignoreSymbols = '()[]{} '


class AlgReadError(Exception):
    pass

class NotZBLLError(Exception):
    pass


def checkAndSplitAlg(alg):
    strippedAlg = getBaseAlg(alg)
    splitAlg = strippedAlg.split(' ') # Separate by spaces
    moves = []
    for move in splitAlg:
        if not move:
            continue
        move = move.strip(ignoreSymbols)
        if not move in movesDict.keys():
            return False, 'Move not recognised: "'+move+'"'
        moves.append(movesDict[move])
    return True, moves


def getBaseAlg(alg):
    strippedAlg = alg.strip().split('//')[0].strip() # Drop everything after a double slash (allow comments in algs)
    return strippedAlg


def getComment(alg):
    endPart = getStringAfterSep(alg, '//').strip()
    comment = endPart.split('//')[0]
    recog = getStringAfterSep(endPart, '::').strip()
    return comment.strip(), recog.strip()


def applyAlg(alg, startCase=solvedCube):
    result = copy.deepcopy(startCase) # don't accidentally change the startCase
    for move in alg:
        step = copy.deepcopy(result)
        # corner permutation:

        for i in range(len(move[1])):
            step[0][move[1][i]] = result[0][i]
            step[1][move[1][i]] = result[1][i]
        # edge permutation:
        for i in range(len(move[3])):
            step[2][move[3][i]] = result[2][i]
            step[3][move[3][i]] = result[3][i]
        # center permutation:
        for i in range(len(move[4])):
            step[4][move[4][i]] = result[4][i]
        # Note. We're done with the old result. We need to update orientations based on step now.
        # corner orientation:
        for i in range(len(move[0])):
            step[0][i] = (step[0][i] + move[0][i]) % 3
        # edge orientation:
        for i in range(len(move[2])):
            step[2][i] = (step[2][i] + move[2][i]) % 2
        result = copy.deepcopy(step)

    return result


def applyInverseAlg(alg, startCase=solvedCube):
    result = copy.deepcopy(startCase) # don't accidentally change the startCase
    for i in range(len(alg)-1,-1,-1):
        move = [alg[i]]
        result = applyAlg([applyAlg(move)], result)
    return result

def getLLCase(case):
    llcase = case[0][:4] + case[1][:4] + case[3][:4]
    return llcase


def getInverseCase(alg):
    inverse = applyInverseAlg(alg)
    return inverse


def rotateToReferencePosition(case, ignoreY=False):
    # Rotate if U centre not on top.
    if case[4][0]==0:
        pass
    elif case[4][1]==0:
        case = applyAlg([movesDict["x"]], case)
    elif case[4][2]==0:
        case = applyAlg([movesDict["z'"]], case)
    elif case[4][3]==0:
        case = applyAlg([movesDict["x'"]], case)
    elif case[4][4]==0:
        case = applyAlg([movesDict["z"]], case)
    elif case[4][5]==0:
        case = applyAlg([movesDict["x2"]], case)

    if not ignoreY:
        # Rotate if F centre not in front.
        if case[4][1]==1:
            pass
        elif case[4][2]==1:
            case = applyAlg([movesDict["y"]], case)
        elif case[4][3]==1:
            case = applyAlg([movesDict["y2"]], case)
        elif case[4][4]==1:
            case = applyAlg([movesDict["y'"]], case)
            
    return case
    
    
def getZBLLcase(alg):
    zblls = getUniqueZBLLCases()
    case = rotateToReferencePosition(applyInverseAlg(alg))
    llcase = strCase(getLLCase(case))
    
    for zbll in zblls.keys():
        if llcase in zblls[zbll]:
            return zbll
    raise NotZBLLError("Not an ZBLL case: "+llcase)


def getInitialAUF(alg):
    basezbll = getZBLLcase(alg)
    rotatedCases = [strCase(c) for c in getAllRotations(getLLCase(rotateToReferencePosition(applyInverseAlg(alg), ignoreY=True)))]
    aufs = [r%4 for r in range(len(rotatedCases)) if rotatedCases[r] == basezbll]
    auf = ["(U') ", "(U2) ", "(U) ", ""][max(aufs)]
    return auf
    

def getZBLLCaseName(case):
    [ocll, cpll, epll] = case.split(' ')

    ocllName = ocllCaseNames[ocll]
    collName = ocllName + cpllCaseNames[cpll]
    zbllName = collName + '-' + epll

    return zbllName

def main():

    #rawAlg = "R U R' U' R' F R2 U R' U' R U R' U' F'"
    #rawAlg = "R U R' U R U L' U R' U' L"
    rawAlg = "R U R' U R U2 R'"
    #rawAlg = "U'"
    #rawAlg = " // Solved"
    ok, alg = checkAndSplitAlg(rawAlg)
    #print(alg)
    if not ok:
        print('ERROR: ',alg)
        return
    #print('Alg: ',alg)

    result = applyAlg(alg)
    inverse = getInverseCase(alg)

    case = strCase(getLLCase(result))
    inverse = strCase(getLLCase(inverse))

    print(inverse)
    print(case)

    import pylab

    pylab.Figure()
    plot(case, stage='ZBLL', edgeCycle=False)
    pylab.get_current_fig_manager().window.wm_geometry("+1400+100")

    pylab.Figure()
    plot(inverse, stage='ZBLL', edgeCycle=False)
    pylab.get_current_fig_manager().window.wm_geometry("+1400+300")

    draw()


if __name__ == '__main__':
    main()
