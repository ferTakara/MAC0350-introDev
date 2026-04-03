const abas = document.querySelectorAll(".aba");
let indiceAtual = 0;

function selecionar(botaoClicado) {
    let botoes = document.querySelectorAll("button");

    botoes.forEach(btn => {
        btn.classList.remove("ativo");
    });

    botaoClicado.classList.add("ativo");
}

function ativarAba(index) {
    abas.forEach(btn => btn.classList.remove("ativo"));
    abas[index].classList.add("ativo");
}

abas.forEach((btn, i) => {
    btn.addEventListener("click", () => {
        indiceAtual = i;
        ativarAba(indiceAtual);
    });
});

document.addEventListener("keydown", (e) => {
    if (
        e.key.toLowerCase() === "p" &&
        e.shiftKey &&
        e.altKey &&
        e.ctrlKey
    ) {
        e.preventDefault();

        indiceAtual = (indiceAtual + 1) % abas.length;
        ativarAba(indiceAtual);
    }
});