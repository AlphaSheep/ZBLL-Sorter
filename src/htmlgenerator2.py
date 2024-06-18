#!/usr/bin/python3
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


def generateHTML(sortedZBLLdict, knownAlgs, ocllProbs, collProbs, zbllProbs, ocllImg, collImg, zbllImg):

    css = """

    body {
        background-color: #000;
        text-align: center;
    }

    div.zbllalgcount {
        background: #222;
        font-family: monospace;
        color: #ddd;
        padding: 15px;
        margin: 20px 10px;
        height: 64px;
        text-align: left;
        font-size: 1.2em;
    }

    div.zbllalgcount div {
        padding: 5px ;
    }

    div.zbllblock {

        color: #ddd;
        background: #444;
        font-family: Verdana, Arial, sans-serif;
        font-size: 6pt;
        position: absolute;
        display: block;
        text-align: center;
        border: 1px solid #000;
        width: 105px;
        height: 190px;
        padding: 2px;
    }

    div.zbllalg {
        padding: 8px 2px;
        font-size: 8pt;
    }

    div.zbllblock:hover, div.collblock:hover, div.ocllblock:hover {
        background: #446;
    }
    div.knownfull {
        color: #fff;
        background: #163;
    }
    div.knownpartial{
        background: #ffd;
    }
    div.notknown {
        background: #222;
    }
    """

    cssFileName = 'main.css'
    cssPath = savePath + '/css/' + cssFileName

    copyrightMsg = """
    Copyright &copy; 2015 Brendan Gray and Sylvermyst Technologies
    """

    i=0
    html = '<!DOCTYPE html>\n<html>\n    <head>\n'
    html+= '        <link rel="stylesheet" type="text/css" href="css/'+cssFileName+'">\n'
    html+= '        <link rel="stylesheet" type="text/css" href="css/cube.css">\n'
    html+= '    </head>\n    <body>\n'

    x = 0
    y = 150

    oclls = getList(sortedZBLLdict)
    algs = knownAlgs

    algcount = len(algs.keys())
    casecount = len(zbllProbs.keys())-1

    algcountminussune = len([k for k in algs.keys() if k[0] not in 'AS'])
    casecountminussune = len([k for k in zbllProbs.keys() if k[0] not in 'AS'])-1

    html += '        <div class="zbllalgcount"><div>Progress toward full ZBLL: '
    html += '<b>{:} / {:}</b> ({:.2f}%)</div>\n'.format(algcount, casecount, algcount/casecount*100)
    html += '            <div>Excluding Sune and Anti-Sune: '
    html += '<b>{:} / {:}</b> ({:.2f}%)</div>\n'.format(algcountminussune, casecountminussune, algcountminussune/casecountminussune*100)
    html += '        </div>'

    html += '        <div class="zbllcontainer">\n\n'

    for ocll in oclls:

        y += 2

        colls = getList(sortedZBLLdict[ocll])
        for coll in colls:

            x = 20#165

            css+='\n#Case'+coll+' {\n    left: '+str(x)+';\n    top: '+str(y)+';\n}'
            x += 0#162
            y += 0

            for zbll in sortedZBLLdict[ocll][coll]:
                if zbll[0] in algs.keys():
                    classes = ' knownfull'
                else:
                    classes = ' notknown'

                html += '    <div class="zbllblock'+classes+'" id="CaseZBLL'+str(i)+'">'
                html += 'ZBLL case #'+str(i)+'<br/>'+zbll[0]+'\n        '
                html += "<br/>P: "+"{:.2f}".format(zbllProbs[zbll[0]]/77.76)
                html += "% ("+probFractionString(zbllProbs[zbll[0]], 7776)+")\n <br/><br/>        "
                html += '<div class="cube-image" data-case="'+zbll[0]+'"></div>'

                if zbll[0] in algs.keys():
                    html+='<br/><div class="zbllalg">'+algs[zbll[0]]+'</div>\n'
                else:
                    html+='\n'

                html+='    </div>\n'

                css+='\n#CaseZBLL'+str(i)+' {\n    left: '+str(x)+'px;\n    top: '+str(y)+'px;\n}'
                x += 110

                i+=1

            y += 201

        y += 60
        x = 0

    html+= '\n        <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ=" crossorigin="anonymous"></script>\n'
    html+= '\n        <script src="js/cube.js"></script>\n'
    html+= '\n\n        </div>\n    </body>\n</html>\n'

    # Save CSS file
    fCSS = open(cssPath, 'w')
    fCSS.write(css)
    fCSS.close()

    return html

if __name__ == '__main__':
    pass
