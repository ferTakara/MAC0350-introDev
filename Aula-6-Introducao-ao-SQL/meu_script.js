/**
 *  Esse script mostra mais recursos do canvas e da JS
 */

// A `main()` só deve ser executada quando tudo estiver carregado
window.onload = main;

// variáveis globais
var ctx;  // contexto de desenho
var velX = 5;  // em pixels
var velY = 3;  // em pixels


//==================================================================
/**
 * função principal
 */
 function main() {
    // veja o canvas id definido no arquivo index.html
    const canvas = document.getElementById('meucanvas');
    // vamos definir um contexto para desenhar em 2D
    ctx = canvas.getContext('2d');
    width = canvas.width;
    height = canvas.height;

    if (!ctx) alert("Não consegui abrir o contexto 2d :-( ");

    circuloAnimation(300, 300, 100)
};

//==================================================================
// outras funções
// ------------------------------------------------------------------
/**
 * desenha um poligono definido por pts e
 * preenchido com uma cor sólida caso wid = 0.
 * Caso contrário, desenha o contorno com lagura wid.
 * @param {array} pts - array de pontos
 * @param {string} cor - cor para pintar o poligono
 * @param {number} wid - largura da borda se wid>0.
 */

function desenhaCirculo (x, y, r) {
    points = []

    for (let i = 0; i <= 360; i++) {
        let newX = x + r * Math.cos(Math.PI * (i / 180))
        let newY = y + r * Math.sin(Math.PI * (i / 180))
        points.push([newX, newY])
    }

    desenhePoligono(points, 'green', 0);
}

//==================================================================
/**
* redesenha o canvas a cada intervalo
* @param {number} maxp
*/
function circuloAnimation(x, y, r) {
    // atualiza a cena, ou seja, a posição do objeto
    posX = x + velX;
    posY = y + velY;

    if (posX < 0) {
        velX *= -1;
        posX = -posX;
    }
    if (posX >= width) {
        velX *= -1;
        posX = width - (posX-width);
    }
    if (posY < 0) {
        velY *= -1;
        posY = -posY;
    }
    if (posY >= height) {
        velY *= -1;
        posY = height - (posY-height);
    }

    // ciclo da animação: limpa a tela e desenhe
    ctx.clearRect( 0, 0, width, height);
    // desenha um quadrado verde
    desenhaCirculo(posX, posY, r)

    // requisita o próximo redesenho
    window.requestAnimationFrame(() => circuloAnimation(posX, posY, r));
};

function desenhePoligono( pts, cor='blue', wid = 10 ) {
    let tam = pts.length;
    console.log("Desenhando poligono", cor, pts, tam);

    let poli = new Path2D();
    poli.moveTo( pts[0][0], pts[0][1] );
    for (let i = 1; i < pts.length; i++) {
        poli.lineTo( pts[i][0], pts[i][1] );
        console.log( pts[i][0], pts[i][1]  );
    }
    poli.closePath(); // cria um contorno fechado.

    if (wid > 0) { 
        ctx.strokeStyle = cor;
        ctx.lineWidth = wid;
        ctx.stroke( poli );
    }
    else { // wid <= 0 preenche o polígono
        ctx.fillStyle=cor;
        ctx.fill( poli );
    }
}

// ------------------------------------------------------------------
/**
 * recebe o texto msg e o desenha na posição (x,y) do canvas.
 * @param {string} msg 
 * @param {number} x 
 * @param {number} y 
 * @param {number} tam - tamanho da fonte
 * @param {string} cor - cor do texto
 */
function desenheTexto (msg, x, y, tam=24, cor = 'black') {
    ctx.fillStyle = cor;
    ctx.font = `${tam}px serif`;  
    ctx.fillText(msg, x, y);
}