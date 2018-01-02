
var cubeImages = $('.cube-image');

var pieces = [      'BUL','BU','BUR',
              'LUB','UBL','UB','UBR','RUB',
              'LU', 'UL', 'U', 'UR', 'RU',
              'LUF','UFL','UF','UFR','RUF',
                    'FUL','FU','FUR']

var ocll = {
    '0': [0,0,0,0],
    'A': [0,1,1,1],
    'H': [1,2,1,2],
    'L': [0,1,0,2],
    'P': [1,1,2,2],
    'S': [0,2,2,2],
    'T': [0,0,1,2],
    'U': [0,0,2,1]
}

var cpll = {
    '0': [0,1,2,3],
    'F': [0,1,3,2],
    'D': [0,3,2,1],
    'R': [0,2,1,3],
    'L': [0,2,3,1],
    'B': [0,3,1,2]
}

var EOcols = ['UB','UR','UF','UL'];

var edges = [['UB','BU'],['UR','RU'],['UF','FU'],['UL','LU']];
var corners = [['UBL','LUB','BUL'],['UBR','BUR','RUB'],['UFR','RUF','FUR'],['UFL','FUL','LUF']];

var cornerBaseCols = [['U','L','B'], ['U','B','R'], ['U','R','F'], ['U','F','L']];
var edgeBaseCols = [['U','B'], ['U','R'], ['U','F'], ['U','L']];


for (let i = 0; i < cubeImages.length; i++) {
    
    let cubeImage = $(cubeImages[i]);
    
    let cubecase = cubeImage.attr("data-case");
    
    // Create blocks
    
    for (let p = 0; p < pieces.length; p++) {
        let piece = $(document.createElement('div'))
            .addClass('cube-'+pieces[p])
            .appendTo(cubeImage);
    }
    
    // Colour the centre sticker
    cubeImage.children('.cube-U').addClass('cube-col-U');
    
    // Colour edges
    let epll = cubecase.slice(3).split('').map(Number);
    for (let e = 0; e < 4; e++) { // For each corner
        let ep = epll[e];
        cubeImage.children('.cube-'+edges[e][0]).addClass('cube-col-'+edgeBaseCols[ep][0]);
        cubeImage.children('.cube-'+edges[e][1]).addClass('cube-col-'+edgeBaseCols[ep][1]);
    }
    
    // Colour corners
    for (let c = 0; c < 4; c++) { // For each corner
        let co = ocll[cubecase[0]][c];
        let cp = cpll[cubecase[1]][c];
        for (let s = 0; s < 3; s++) { // For each sticker
            cubeImage.children('.cube-'+corners[c][s]).addClass('cube-col-'+cornerBaseCols[cp][(3+s-co)%3]);
        }
    }
    
}

console.log(cubeImages)
