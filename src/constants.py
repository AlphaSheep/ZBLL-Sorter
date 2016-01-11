'''
Created on 06 Jan 2016

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


savePath = '../'

algFileName = '../algorithms.txt'


globalGenerateImages = False
globalGenerateSetImages = False

ocllImageSize = 128
collImageSize = 96
zbllImageSize = 64


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



cornerTwistSet = [0, 1, 2]    # 0: oriented; 1: twisted clockwise; 2: twisted anticlockwise
cornerPermSet = [0, 1, 2, 3]  # 0: UBL, 1: UBR, 2: UFR, 3: UFL
edgePermSet = [0, 1, 2, 3]    # 0: UB, 2: UR, 3: UF, 4: UL



# ColorScheme

U = [1,1,0] # yellow
F = [0,0,1] # blue
R = [0.9, 0, 0] # red
B = [0,0.75,0] # green
L = [1, 0.6, 0] # orange
D = [1,1,1] # white
neutralCol = None #[0.6, 0.6, 0.6]

cornerBaseCols = [[U,L,B], [U,B,R], [U,R,F], [U,F,L]] # clockwise, starting on U
edgeBaseCols = [[U,B], [U,R], [U,F], [U,L]]

edgeLocs = [(2.5,3.5), (3.5,2.5), (2.5,1.5), (1.5,2.5)]
cornerLocs = [(1.5,3.5), (3.5,3.5), (3.5,1.5), (1.5,1.5)]

