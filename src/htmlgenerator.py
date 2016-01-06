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
    
    
    return html

if __name__ == '__main__':
    pass