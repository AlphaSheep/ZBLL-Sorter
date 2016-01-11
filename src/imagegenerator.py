'''
Created on 04 Mar 2015

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

import pylab
import copy

from matplotlib.patches import Rectangle

from constants import *


def deStrCase(s):
    return [int(s[0]), int(s[1]), int(s[2]), int(s[3]), 
            int(s[5]), int(s[6]), int(s[7]), int(s[8]), 
            int(s[10]), int(s[11]), int(s[12]), int(s[13])]


def twistedCornerCols(cols, twist):
    return (cols+cols+cols)[3-twist:6-twist]


def getColours(case, stage='ZBLL'):
    co = case[:4]
    cp = case[4:8]
    ep = case[8:]
    corners = copy.deepcopy(cornerBaseCols)
    edges = copy.deepcopy(edgeBaseCols)
    cpCols = [corners[cp[0]], corners[cp[1]], corners[cp[2]], corners[cp[3]]]
    if stage in ['OCLL']:
        for c in cpCols:
            c[1] = neutralCol
            c[2] = neutralCol    
    cornerCols = [twistedCornerCols(cpCols[0], co[0]), twistedCornerCols(cpCols[1], co[1]), twistedCornerCols(cpCols[2], co[2]), twistedCornerCols(cpCols[3], co[3]),]    
    edgeCols = [edges[ep[0]], edges[ep[1]], edges[ep[2]], edges[ep[3]]]
    if stage in ['OCLL', 'COLL']:
        for c in edgeCols:
            c[1] = neutralCol
            
    colMatrix = [[            None, cornerCols[3][2], edgeCols[3][1], cornerCols[0][1], None            ],
                 [cornerCols[3][1], cornerCols[3][0], edgeCols[3][0], cornerCols[0][0], cornerCols[0][2]],
                 [  edgeCols[2][1],   edgeCols[2][0],        U      ,   edgeCols[0][0],   edgeCols[0][1]],
                 [cornerCols[2][2], cornerCols[2][0], edgeCols[1][0], cornerCols[1][0], cornerCols[1][1]],
                 [            None, cornerCols[2][1], edgeCols[1][1], cornerCols[1][2], None            ]]
    
    return colMatrix
    
    
                    

def plotColMatrix(cols):
    pylab.figure(figsize=(1,1), dpi=100)
    ax = pylab.gcf().gca()
    for i in range(len(cols)):
        for j in range(len(cols[i])):
            if not cols[i][j] is None:
                width = 1
                height = 1
                xmod = 0
                ymod = 0  
                if i==0:
                    width = 0.5
                    xmod = 0.5 
                elif i==4:
                    width = 0.5
                if j==0:
                    height = 0.5
                    ymod = 0.5
                elif j==4:
                    height=0.5
                r = Rectangle((i+xmod,j+ymod),width,height,fill=True,fc=cols[i][j], ec=[0,0,0], lw=1)
                ax.add_patch(r)
    r = Rectangle((1,1),3,3,fill=False, ec=[0,0,0], lw=3)
    ax.add_patch(r)
    pylab.axis('tight')
    pylab.axis('equal')
    pylab.axis('off')
    pylab.xlim([0.4,4.6])
    pylab.ylim([0.4,4.6])
    
    
def savecurrent(fileName):
    pass
    

    
    
def plotEdgeCycle(llcase):
    if type(llcase)==str:
        case = deStrCase(llcase)
    else:
        case = llcase
    edges = case[8:]
    for i in range(4):        
        x0 = edgeLocs[i][0]
        x1 = edgeLocs[edges[i]][0]
        y0 = edgeLocs[i][1]
        y1 = edgeLocs[edges[i]][1]
        opt = {'head_width': 0.2, 'head_length': 0.4, 'width': 0.05, 'length_includes_head': True}
        if not (x0==x1 and y0==y1):
            pylab.arrow(x0,y0,x1-x0,y1-y0, color='k', **opt)
    

def plotCornerCycle(llcase):
    if type(llcase)==str:
        case = deStrCase(llcase)
    else:
        case = llcase
    corners = case[4:8]
    for i in range(4):        
        x0 = cornerLocs[i][0]
        x1 = cornerLocs[corners[i]][0]
        y0 = cornerLocs[i][1]
        y1 = cornerLocs[corners[i]][1]
        opt = {'head_width': 0.2, 'head_length': 0.4, 'width': 0.05, 'length_includes_head': True}
        if not (x0==x1 and y0==y1):
            pylab.arrow(x0,y0,x1-x0,y1-y0, color='k', **opt)
    


def plot(llcase, label=False, stage='ZBLL', edgeCycle=False, cornerCycle=False):
    if type(llcase)==str:
        case = deStrCase(llcase)
    else:
        case = llcase
    cols = getColours(case, stage=stage)
    plotColMatrix(cols)
    if label:
        pylab.text(0,0,llcase)
    if edgeCycle:
        plotEdgeCycle(case)
    if cornerCycle:
        plotCornerCycle(case)
            
        
def draw():
    pylab.show()
    
def save(filename, size=200):
    
    pylab.savefig(filename, figsize=(1,1), dpi=size)
    pylab.close()
    

def main():
    caseSolved = '0000 0123 0123'
    caseSune = '1011 2301 1320'
    
    plot('1212 0213 0132', stage='COLL', edgeCycle=False)
    #draw()
    save("test.png")


if __name__ == '__main__':
    main()
