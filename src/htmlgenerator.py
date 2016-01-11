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

from utilities import getList, probFractionString

from constants import *


def generateHTML(sortedZBLLdict, ocllProbs, collProbs, zbllProbs, ocllImg, collImg, zbllImg):

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
    
    div.ocllblock {
        position: absolute;
        display: block;
        text-align: center;
        border: 2px solid #000;
        width: 128px;
        height: 879px; 
        padding: 5px;
        margin: 1px;
    }
    div.collblock {
        position: absolute;
        display: block;
        text-align: center;
        border: 1px solid #000;
        width: 96px;    
        height: 135px;  
        padding: 5px;
        margin: 1px;
    }
    div.zbllblock {
        position: absolute;
        display: block;
        text-align: center;
        border: 1px solid #000;
        width: 90px;        
        padding: 5px;
        margin: 1px;
    }
    div.zbllblock:hover, div.collblock:hover, div.ocllblock:hover {
        background: #ccf;
    }
    """

    cssFileName = 'stylesheet.css'

    copyrightMsg = """
    Copyright &copy; 2015 Brendan Gray and Sylvermyst Technologies
    """
    
    i=0
    html = '<html><head><link rel="stylesheet" type="text/css" href="'+cssFileName+'"></head><body>'
    
    x = 0
    y = 0
    
    oclls = getList(sortedZBLLdict)
    for ocll in oclls:
        html+='<div class="ocllblock" id="Case'+ocll+'">' + 'OCLL case: '+ocll+'<br/>'
        html+='<img src="'+ocllImg[ocll]+'" width="'+str(ocllImageSize)+'px" />'
        html+="<br/>Probability: "+"{:.2f}".format(ocllProbs[ocll]/77.76)+"% ("+probFractionString(ocllProbs[ocll], 7776)+')'
        html+='</div>'
        
        ocllx = x
        oclly = y
        y += 2
        
        colls = getList(sortedZBLLdict[ocll])
        for coll in colls:
            
            x= 145
            
            html+='<div class="collblock" id="Case'+coll+'">' + 'COLL case: '+coll+'<br/>'
            html+='<img src="'+collImg[coll]+'" width="'+str(collImageSize)+'px" />'
            html+="<br/>Probability: "+"{:.2f}".format(collProbs[coll]/77.76)+"% ("+probFractionString(collProbs[coll], 7776)+')'
            html+='</div>'
            
            css+='\n#Case'+coll+' {\n    left: '+str(x)+';\n    top: '+str(y)+';\n}'
            x += 112
            y += 6
            
            for zbll in sortedZBLLdict[ocll][coll]:
                html+='<div class="zbllblock" id="CaseZBLL'+str(i)+'">' + 'ZBLL case #'+str(i)+'<br/>'+zbll[0]+'<br/>'
                html+='<img src="'+zbllImg[zbll[0]]+'" width="'+str(zbllImageSize)+'px" />'
                html+="<br/>Probability: "+"{:.2f}".format(zbllProbs[zbll[0]]/77.76)+"% ("+probFractionString(zbllProbs[zbll[0]], 7776)+")</td>\n        "
                html+='</div>'

                css+='\n#CaseZBLL'+str(i)+' {\n    left: '+str(x)+';\n    top: '+str(y)+';\n}'
                x += 101

                i+=1

            y += 140
        
        css+='\n#Case'+ocll+' {\n    left: '+str(ocllx)+';\n    top: '+str(oclly)+';    height: '+str(y-oclly-12)+';\n}'
        
        y += 10
        x = 0
        
    # Save CSS file
    fCSS = open('../'+cssFileName, 'w')
    fCSS.write(css)
    fCSS.close()
    
    return html

if __name__ == '__main__':
    pass