// =====================================================================
//  CATÁLOGO NITRON — montagem automática no InDesign
//  Lê saida/catalogo_indesign.csv (gerado por gera_catalogo.py) e monta
//  o catálogo inteiro: 9 produtos por página, nome em PT/EN/ES, cor,
//  volume, tamanho, referência, caixa, código de barras e preço.
//
//  O preço fica na camada "Preço". No fim o script exporta dois PDFs:
//  um com a camada ligada (COM PREÇO) e outro com ela desligada (SEM PREÇO).
//
//  Como rodar: InDesign > Janela > Utilitários > Scripts > Usuário >
//  clique direito > "Mostrar no Finder/Explorer", copie este arquivo para
//  lá e dê dois cliques nele no painel Scripts.
// =====================================================================
#target indesign

// ------------------------------------------------------------------ CONFIG
var CFG = {
    pagina:   { w: 210, h: 297 },            // mm (A4)
    margem:   { top: 30, bottom: 16, left: 12, right: 12 },
    gutter:   4,                               // mm entre cards (igual nas 3 grades)
    // três grades: 3, 4 ou 5 produtos por linha. Cada uma vira uma página-mestre com as colunas.
    // corpo em pt; ean = altura das barras em mm; texto = altura reservada ao bloco de texto em mm
    grades: {
        3: { rows: 3, nome: 7.5, idioma: 6,   specs: 6,   preco: 11,  ean: 8,   texto: 19 },
        4: { rows: 4, nome: 6.5, idioma: 5.3, specs: 5.3, preco: 9.5, ean: 7,   texto: 17 },
        5: { rows: 5, nome: 6,   idioma: 4.8, specs: 4.8, preco: 8.5, ean: 6.5, texto: 19 }
    },
    gradePadrao: 4,                            // usada quando a seção não define POR_LINHA
    // cores da marca (CMYK) — ajuste para o manual da Nitron
    corMarca: [100, 70, 0, 30],
    corTexto: [0, 0, 0, 90],
    corSuave: [0, 0, 0, 55],
    corBorda: [0, 0, 0, 15],
    corSelo:  [0, 90, 100, 0],
    // fonte da marca: Gotham Book e Gotham Bold em tudo (sem itálico)
    fonte:    { familia: "Gotham", book: "Book", bold: "Bold" },
    eanModulo: 0.264,                          // mm (80% do tamanho nominal EAN-13)
    extensoesFoto: [".psd", ".tif", ".tiff", ".png", ".jpg", ".jpeg", ".ai", ".eps", ".pdf"],
    rodapePreco: "Preços da tabela padrão, sujeitos a alteração sem aviso prévio."
};

// ------------------------------------------------------------------ CSV
function lerCSV(arquivo) {
    arquivo.encoding = "UTF-8";
    if (!arquivo.open("r")) throw "Não consegui abrir " + arquivo.fsName;
    var txt = arquivo.read();
    arquivo.close();
    if (txt.charCodeAt(0) === 0xFEFF) txt = txt.substring(1);
    var linhas = [], campo = "", linha = [], aspas = false, i, c;
    for (i = 0; i < txt.length; i++) {
        c = txt.charAt(i);
        if (aspas) {
            if (c === '"') {
                if (txt.charAt(i + 1) === '"') { campo += '"'; i++; }
                else aspas = false;
            } else campo += c;
        } else if (c === '"') aspas = true;
        else if (c === ";") { linha.push(campo); campo = ""; }
        else if (c === "\n" || c === "\r") {
            if (c === "\r" && txt.charAt(i + 1) === "\n") i++;
            linha.push(campo); campo = "";
            if (linha.length > 1 || linha[0] !== "") linhas.push(linha);
            linha = [];
        } else campo += c;
    }
    if (campo !== "" || linha.length) { linha.push(campo); linhas.push(linha); }
    var cab = linhas[0], out = [], r, o, k;
    for (r = 1; r < linhas.length; r++) {
        o = {};
        for (k = 0; k < cab.length; k++) o[cab[k]] = linhas[r][k] || "";
        out.push(o);
    }
    return out;
}

// ------------------------------------------------------------------ EAN-13
var EAN_L = ["0001101","0011001","0010011","0111101","0100011","0110001","0101111","0111011","0110111","0001011"];
var EAN_G = ["0100111","0110011","0011011","0100001","0011101","0111001","0000101","0010001","0001001","0010111"];
var EAN_R = ["1110010","1100110","1101100","1000010","1011100","1001110","1010000","1000100","1001000","1110100"];
var EAN_P = ["LLLLLL","LLGLGG","LLGGLG","LLGGGL","LGLLGG","LGGLLG","LGGGLL","LGLGLG","LGLGGL","LGGLGL"];

function eanValido(e) {
    if (!/^\d{13}$/.test(e)) return false;
    var s = 0, i;
    for (i = 0; i < 12; i++) s += parseInt(e.charAt(i), 10) * (i % 2 ? 3 : 1);
    return (10 - s % 10) % 10 === parseInt(e.charAt(12), 10);
}

// aceita 12 dígitos (calcula o verificador) ou 13; ignora espaços, pontos e traços
function eanCompleta(e) {
    e = String(e || "").replace(/\D/g, "");
    if (e.length !== 12) return e;
    var s = 0;
    for (var i = 0; i < 12; i++) s += parseInt(e.charAt(i), 10) * (i % 2 ? 3 : 1);
    return e + String((10 - s % 10) % 10);
}

function eanBits(e) {
    var p = EAN_P[parseInt(e.charAt(0), 10)], b = "101", i, d;
    for (i = 1; i <= 6; i++) {
        d = parseInt(e.charAt(i), 10);
        b += (p.charAt(i - 1) === "L") ? EAN_L[d] : EAN_G[d];
    }
    b += "01010";
    for (i = 7; i <= 12; i++) b += EAN_R[parseInt(e.charAt(i), 10)];
    return b + "101";
}

// desenha o código como vetor (retângulos) — não depende de fonte nem plugin
// largura total do símbolo com as margens de silêncio (9 + 95 + 7 módulos) — nunca reduzir
function larguraEAN() { return 111 * CFG.eanModulo; }

function desenhaEAN(pg, camada, ean, x, y, h, est) {
    var m = CFG.eanModulo, bits = eanBits(ean);
    var quiet = 9 * m, itens = [], i = 0, ini, guarda, r;
    while (i < 95) {
        if (bits.charAt(i) === "1") {
            ini = i;
            while (i < 95 && bits.charAt(i) === "1") i++;
            guarda = (ini <= 2) || (ini >= 45 && ini <= 49) || (ini >= 92);
            r = pg.rectangles.add(camada, undefined, undefined, {
                geometricBounds: [y, x + quiet + ini * m, y + h + (guarda ? 1.2 : 0), x + quiet + i * m],
                fillColor: "Black", strokeWeight: 0
            });
            itens.push(r);
        } else i++;
    }
    // dígitos legíveis
    var ty = y + h + 0.15, th = 2.4;
    itens.push(txt(pg, camada, [ty, x, ty + th, x + quiet - 0.3], ean.charAt(0), est, Justification.RIGHT_ALIGN));
    itens.push(txt(pg, camada, [ty, x + quiet + 3 * m, ty + th, x + quiet + 45 * m], ean.substr(1, 6), est, Justification.CENTER_ALIGN));
    itens.push(txt(pg, camada, [ty, x + quiet + 50 * m, ty + th, x + quiet + 92 * m], ean.substr(7, 6), est, Justification.CENTER_ALIGN));
    return pg.groups.add(itens, camada);
}

// ------------------------------------------------------------------ helpers
function cor(doc, nome, cmyk) {
    var c = doc.colors.itemByName(nome);
    if (!c.isValid) c = doc.colors.add({ name: nome, model: ColorModel.PROCESS, space: ColorSpace.CMYK, colorValue: cmyk });
    return c;
}

// acha a Gotham como estiver instalada: família "Gotham" + estilo "Book"/"Bold",
// ou famílias separadas "Gotham Book" / "Gotham Bold" (instalações antigas)
var FONTE_FALTANDO = [];
function fonteGotham(peso) {
    var fam = CFG.fonte.familia, sty = CFG.fonte[peso];
    var tentativas = [fam + "\t" + sty, fam + " " + sty + "\tRegular", fam + " " + sty + "\t" + sty, fam + "-" + sty + "\tRegular"];
    for (var i = 0; i < tentativas.length; i++) {
        var f = app.fonts.itemByName(tentativas[i]);
        if (f.isValid) return f;
    }
    FONTE_FALTANDO.push(fam + " " + sty);
    return null;
}

function estilo(doc, nome, props) {
    var s = doc.paragraphStyles.itemByName(nome);
    if (!s.isValid) s = doc.paragraphStyles.add({ name: nome });
    var f = fonteGotham(props.peso || "book");
    if (f) s.appliedFont = f;
    s.pointSize = props.size;
    s.leading = props.leading || props.size * 1.15;
    s.fillColor = props.cor;
    s.spaceAfter = props.after || 0;
    s.justification = props.just || Justification.LEFT_ALIGN;
    s.hyphenation = false;
    return s;
}

function txt(pg, camada, gb, conteudo, nomeEstilo, just) {
    var t = pg.textFrames.add(camada, undefined, undefined, { geometricBounds: gb, contents: conteudo });
    t.textFramePreferences.insetSpacing = [0, 0, 0, 0];
    t.parentStory.paragraphs.everyItem().appliedParagraphStyle = pg.parent.parent.paragraphStyles.itemByName(nomeEstilo);
    if (just) t.parentStory.justification = just;
    return t;
}

// reduz o corpo de cada parágrafo em 4% por vez até caber (mantém a hierarquia PT > EN/ES)
function encaixa(t) {
    var guard = 0, ps, k, sz;
    while (t.overflows && guard < 12) {
        ps = t.parentStory.paragraphs;
        for (k = 0; k < ps.length; k++) {
            sz = ps[k].pointSize * 0.96;
            ps[k].pointSize = sz; ps[k].leading = sz * 1.15;
        }
        guard++;
    }
    return !t.overflows;
}



function achaFoto(pasta, ref) {
    if (!pasta) return null;
    for (var i = 0; i < CFG.extensoesFoto.length; i++) {
        var f = File(pasta.fsName + "/" + ref + CFG.extensoesFoto[i]);
        if (f.exists) return f;
    }
    return null;
}

function juntaNaoVazios(arr, sep) {
    var o = [];
    for (var i = 0; i < arr.length; i++) if (arr[i]) o.push(arr[i]);
    return o.join(sep);
}

// ------------------------------------------------------------------ main
function main() {
    var csvFile = File.openDialog("Escolha o catalogo_indesign.csv", "*.csv");
    if (!csvFile) return;
    var pastaFotos = Folder.selectDialog("Pasta das FOTOS (arquivos com o nome = referência, ex. 233.012.001.png). Cancele se ainda não houver.");
    var itens = lerCSV(csvFile);
    if (!itens.length) { alert("CSV vazio."); return; }

    var doc = app.documents.add();
    with (doc.documentPreferences) {
        pageWidth = CFG.pagina.w + "mm"; pageHeight = CFG.pagina.h + "mm";
        facingPages = false; pagesPerDocument = 1;
    }
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.rulerOrigin = RulerOrigin.PAGE_ORIGIN;
    doc.zeroPoint = [0, 0];
    with (doc.marginPreferences) { top = CFG.margem.top; bottom = CFG.margem.bottom; left = CFG.margem.left; right = CFG.margem.right; }

    var cMarca = cor(doc, "Nitron Marca", CFG.corMarca), cTexto = cor(doc, "Nitron Texto", CFG.corTexto),
        cSuave = cor(doc, "Nitron Suave", CFG.corSuave), cBorda = cor(doc, "Nitron Borda", CFG.corBorda),
        cSelo = cor(doc, "Nitron Selo", CFG.corSelo);

    estilo(doc, "Secao",  { size: 16, cor: cMarca, peso: "bold" });
    estilo(doc, "SecaoIdiomas", { size: 8, cor: cSuave });
    estilo(doc, "Selo",   { size: 5.5, cor: doc.swatches.itemByName("Paper"), peso: "bold", just: Justification.CENTER_ALIGN });
    estilo(doc, "Rodape", { size: 6, cor: cSuave });
    estilo(doc, "SemFoto", { size: 5.5, cor: cSuave, just: Justification.CENTER_ALIGN });
    // um jogo de estilos por grade (NomePT-3, NomePT-4, NomePT-5...): ajuste o corpo de cada um no painel
    for (var gk in CFG.grades) {
        var G = CFG.grades[gk];
        estilo(doc, "NomePT-" + gk, { size: G.nome, cor: cTexto, peso: "bold", after: 0.5 });
        estilo(doc, "NomeEN-" + gk, { size: G.idioma, cor: cSuave });
        estilo(doc, "NomeES-" + gk, { size: G.idioma, cor: cSuave, after: 0.6 });
        estilo(doc, "Specs-" + gk,  { size: G.specs, cor: cTexto });
        estilo(doc, "Preco-" + gk,  { size: G.preco, cor: cMarca, peso: "bold", just: Justification.RIGHT_ALIGN });
        estilo(doc, "EAN-" + gk,    { size: 5.5, cor: doc.colors.itemByName("Black") });
    }
    if (FONTE_FALTANDO.length &&
        !confirm("Não achei instalada: " + FONTE_FALTANDO.join(", ") + ".\nContinuar com a fonte padrão? (depois é só trocar nos estilos de parágrafo)")) return;

    var resp = prompt("Produtos por linha nas seções sem definição em linhas.csv (3, 4 ou 5):", String(CFG.gradePadrao));
    if (resp === null) return;
    var padrao = parseInt(resp, 10);
    if (!CFG.grades[padrao]) padrao = CFG.gradePadrao;

    var lyFundo = doc.layers[0]; lyFundo.name = "Fundo";
    var lyProd = doc.layers.add({ name: "Produtos" });
    var lyPreco = doc.layers.add({ name: "Preço", layerColor: UIColors.RED });

    var areaW = CFG.pagina.w - CFG.margem.left - CFG.margem.right;
    var areaH = CFG.pagina.h - CFG.margem.top - CFG.margem.bottom;

    // páginas-mestre: mesmas margens e medianiz, só muda o número de colunas (e as guias de linha)
    var mestres = {}, letras = { 3: "A", 4: "B", 5: "C" };
    for (var mk in CFG.grades) {
        var ms = doc.masterSpreads.add(1, { namePrefix: letras[mk], baseName: mk + " por linha" });
        var mp = ms.pages[0];
        with (mp.marginPreferences) {
            top = CFG.margem.top; bottom = CFG.margem.bottom; left = CFG.margem.left; right = CFG.margem.right;
            columnCount = parseInt(mk, 10); columnGutter = CFG.gutter;
        }
        var nr = CFG.grades[mk].rows, chm = (areaH - (nr - 1) * CFG.gutter) / nr;
        for (var rr = 1; rr < nr; rr++) {
            var gy = CFG.margem.top + rr * chm + (rr - 1) * CFG.gutter;
            mp.guides.add(undefined, { orientation: HorizontalOrVertical.HORIZONTAL, location: gy });
            mp.guides.add(undefined, { orientation: HorizontalOrVertical.HORIZONTAL, location: gy + CFG.gutter });
        }
        mestres[mk] = ms;
    }

    var semFoto = [], estouro = [], eanRuim = [];
    var pg = null, pos = 0, porPagina = 0, secaoAtual = null, nPag = 0, cols = padrao, G = CFG.grades[padrao], cw = 0, ch = 0;

    function novaPagina(it) {
        cols = CFG.grades[parseInt(it.POR_LINHA, 10)] ? parseInt(it.POR_LINHA, 10) : padrao;
        G = CFG.grades[cols];
        cw = (areaW - (cols - 1) * CFG.gutter) / cols;
        ch = (areaH - (G.rows - 1) * CFG.gutter) / G.rows;
        porPagina = cols * G.rows;
        pg = (nPag === 0) ? doc.pages[0] : doc.pages.add();
        pg.appliedMaster = mestres[cols];
        nPag++; pos = 0;
        // cabeçalho da seção
        pg.rectangles.add(lyFundo, undefined, undefined, { geometricBounds: [0, 0, 22, CFG.pagina.w], fillColor: cMarca, strokeWeight: 0 });
        var t = txt(pg, lyFundo, [8, CFG.margem.left, 16, CFG.pagina.w - CFG.margem.right], it.LINHA_PT, "Secao");
        t.parentStory.fillColor = doc.swatches.itemByName("Paper");
        var t2 = txt(pg, lyFundo, [16, CFG.margem.left, 21, CFG.pagina.w - CFG.margem.right],
                     juntaNaoVazios([it.LINHA_EN, it.LINHA_ES], "  ·  "), "SecaoIdiomas");
        t2.parentStory.fillColor = doc.swatches.itemByName("Paper");
        // rodapé
        txt(pg, lyFundo, [CFG.pagina.h - 9, CFG.margem.left, CFG.pagina.h - 5, CFG.pagina.w / 2], "Nitron  ·  " + nPag, "Rodape");
        txt(pg, lyPreco, [CFG.pagina.h - 9, CFG.pagina.w / 2, CFG.pagina.h - 5, CFG.pagina.w - CFG.margem.right],
            CFG.rodapePreco, "Rodape", Justification.RIGHT_ALIGN);
    }

    var PAD = 1.6, PT_MM = 0.3528;
    for (var n = 0; n < itens.length; n++) {
        var it = itens[n];
        if (it.LINHA_PT !== secaoAtual || pos >= porPagina) {
            novaPagina(it);
            secaoAtual = it.LINHA_PT;
        }
        var col = pos % cols, row = Math.floor(pos / cols);
        var x = CFG.margem.left + col * (cw + CFG.gutter), y = CFG.margem.top + row * (ch + CFG.gutter), yb = y + ch;
        pos++;

        // card estreito (4 e 5 por linha): o preço não cabe ao lado do código, vai em cima dele
        var estreito = (cw - 2 * PAD) < larguraEAN() + G.preco * PT_MM * 5.5;
        var eanH = G.ean, by = yb - PAD - (eanH + 2.6);
        var precoH = G.preco * PT_MM * 1.2;
        var textoFim = estreito ? by - precoH - 1.2 : by - 1.2;
        var textoIni = textoFim - G.texto;

        // moldura do card
        pg.rectangles.add(lyFundo, undefined, undefined, {
            geometricBounds: [y, x, yb, x + cw], fillColor: "None", strokeColor: cBorda, strokeWeight: 0.5
        });

        // foto: ocupa todo o espaço que sobra acima do texto
        var fr = pg.rectangles.add(lyProd, undefined, undefined, {
            geometricBounds: [y + PAD, x + PAD, textoIni - 1, x + cw - PAD], strokeWeight: 0, fillColor: "None", label: "foto:" + it.FOTO
        });
        var f = achaFoto(pastaFotos, it.FOTO);
        if (f) {
            try { fr.place(f); fr.fit(FitOptions.PROPORTIONALLY); fr.fit(FitOptions.CENTER_CONTENT); }
            catch (e) { semFoto.push(it.REFERENCIA + " (erro ao colocar: " + e + ")"); }
        } else {
            fr.fillColor = cBorda; fr.fillTint = 40;
            var my = (y + PAD + textoIni - 1) / 2;
            txt(pg, lyProd, [my - 2.5, x + PAD, my + 3, x + cw - PAD], "SEM FOTO\r" + it.FOTO, "SemFoto");
            semFoto.push(it.REFERENCIA);
        }
        if (it.LANCAMENTO === "S") {
            pg.rectangles.add(lyProd, undefined, undefined, { geometricBounds: [y + PAD, x + PAD, y + PAD + 3.6, x + PAD + 16], fillColor: cSelo, strokeWeight: 0 });
            txt(pg, lyProd, [y + PAD + 0.7, x + PAD, y + PAD + 3.6, x + PAD + 16], "LANÇAMENTO", "Selo");
        }

        // textos
        var specs1 = juntaNaoVazios([
            juntaNaoVazios([it.COR_PT, it.COR_EN, it.COR_ES], " / "),
            it.VOLUME, it.TAMANHO], "  ·  ");
        var specs2 = "Ref. " + it.REFERENCIA + (it.QTD_CAIXA ? " · Cx " + it.QTD_CAIXA + " un" : "");
        var conteudo = it.NOME_PT + "\r" + it.NOME_EN + "\r" + it.NOME_ES + "\r" + (specs1 ? specs1 + "\r" : "") + specs2;
        var tf = pg.textFrames.add(lyProd, undefined, undefined, {
            geometricBounds: [textoIni, x + PAD, textoFim, x + cw - PAD], contents: conteudo
        });
        tf.textFramePreferences.insetSpacing = [0, 0, 0, 0];
        tf.textFramePreferences.verticalJustification = VerticalJustification.BOTTOM_ALIGN;
        var ps = tf.parentStory.paragraphs, k, nomes = ["NomePT-", "NomeEN-", "NomeES-"];
        for (k = 0; k < ps.length; k++)
            ps[k].appliedParagraphStyle = doc.paragraphStyles.itemByName((k < 3 ? nomes[k] : "Specs-") + cols);
        if (!encaixa(tf)) estouro.push(it.REFERENCIA + " — " + it.NOME_PT);

        // código de barras: largura fixa (80%), só a altura muda por grade
        var bx = estreito ? x + (cw - larguraEAN()) / 2 : x + PAD - 0.6;
        var ean = eanCompleta(it.EAN13);
        if (ean && eanValido(ean)) {
            desenhaEAN(pg, lyProd, ean, bx, by, eanH, "EAN-" + cols);
        } else {
            txt(pg, lyProd, [by + 2, x + PAD, by + 6, x + cw - PAD], it.EAN13 ? "EAN inválido" : "EAN em cadastro", "Specs-" + cols);
            eanRuim.push(it.REFERENCIA + " — " + (it.EAN13 || "sem EAN"));
        }

        // preço (camada própria)
        if (it.PRECO) {
            var pgb = estreito ? [by - precoH - 0.8, x + PAD, by - 0.8, x + cw - PAD]
                               : [yb - PAD - precoH, x + PAD + larguraEAN(), yb - PAD, x + cw - PAD];
            txt(pg, lyPreco, pgb, it.PRECO, "Preco-" + cols);
        }
    }

    // ---------------------------------------------------- relatório
    var rel = File(csvFile.parent.fsName + "/relatorio_montagem.txt");
    rel.encoding = "UTF-8"; rel.open("w");
    rel.writeln("Itens: " + itens.length + "   Páginas: " + doc.pages.length);
    rel.writeln("\nSEM FOTO (" + semFoto.length + "):\n" + semFoto.join("\n"));
    rel.writeln("\nTEXTO NÃO COUBE (" + estouro.length + "):\n" + estouro.join("\n"));
    rel.writeln("\nSEM CÓDIGO DE BARRAS (" + eanRuim.length + "):\n" + eanRuim.join("\n"));
    rel.close();

    // ---------------------------------------------------- salvar e exportar
    var pastaSaida = csvFile.parent;
    doc.save(File(pastaSaida.fsName + "/catalogo_nitron.indd"));
    if (confirm("Montei " + doc.pages.length + " páginas.\n" +
                semFoto.length + " sem foto, " + estouro.length + " com texto apertado, " + eanRuim.length + " sem código de barras.\n" +
                "(detalhes em relatorio_montagem.txt)\n\nExportar agora os PDFs COM e SEM preço?")) {
        lyPreco.visible = true;
        doc.exportFile(ExportFormat.PDF_TYPE, File(pastaSaida.fsName + "/catalogo_nitron_COM_PRECO.pdf"), false);
        lyPreco.visible = false;
        doc.exportFile(ExportFormat.PDF_TYPE, File(pastaSaida.fsName + "/catalogo_nitron_SEM_PRECO.pdf"), false);
        lyPreco.visible = true;
        alert("PDFs salvos em:\n" + pastaSaida.fsName);
    }
}

app.scriptPreferences.enableRedraw = false;
try {
    app.doScript(main, ScriptLanguage.JAVASCRIPT, undefined, UndoModes.FAST_ENTIRE_SCRIPT, "Montar catálogo Nitron");
} catch (e) {
    alert("Erro: " + e + (e.line ? " (linha " + e.line + ")" : ""));
} finally {
    app.scriptPreferences.enableRedraw = true;
}
