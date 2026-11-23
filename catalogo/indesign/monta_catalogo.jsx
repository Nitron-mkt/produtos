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
    grade:    { cols: 3, rows: 3, gutter: 4 },
    // cores da marca (CMYK) — ajuste para o manual da Nitron
    corMarca: [100, 70, 0, 30],
    corTexto: [0, 0, 0, 90],
    corSuave: [0, 0, 0, 55],
    corBorda: [0, 0, 0, 15],
    corSelo:  [0, 90, 100, 0],
    fonte:    "Arial",                        // troque pela fonte da marca
    fonteEAN: "OCR-B",                        // se não existir, usa a fonte acima
    eanModulo: 0.264,                          // mm (80% do tamanho nominal EAN-13)
    eanAltura: 14,                             // mm
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
function desenhaEAN(pg, camada, ean, x, y) {
    var m = CFG.eanModulo, h = CFG.eanAltura, bits = eanBits(ean);
    var quiet = 9 * m, itens = [], i = 0, ini, guarda, r;
    while (i < 95) {
        if (bits.charAt(i) === "1") {
            ini = i;
            while (i < 95 && bits.charAt(i) === "1") i++;
            guarda = (ini <= 2) || (ini >= 45 && ini <= 49) || (ini >= 92);
            r = pg.rectangles.add(camada, undefined, undefined, {
                geometricBounds: [y, x + quiet + ini * m, y + h + (guarda ? 1.6 : 0), x + quiet + i * m],
                fillColor: "Black", strokeWeight: 0
            });
            itens.push(r);
        } else i++;
    }
    // dígitos legíveis
    var ty = y + h + 0.2, th = 2.6;
    itens.push(txt(pg, camada, [ty, x, ty + th, x + quiet - 0.3], ean.charAt(0), "EAN", Justification.RIGHT_ALIGN));
    itens.push(txt(pg, camada, [ty, x + quiet + 3 * m, ty + th, x + quiet + 45 * m], ean.substr(1, 6), "EAN", Justification.CENTER_ALIGN));
    itens.push(txt(pg, camada, [ty, x + quiet + 50 * m, ty + th, x + quiet + 92 * m], ean.substr(7, 6), "EAN", Justification.CENTER_ALIGN));
    return pg.groups.add(itens, camada);
}

// ------------------------------------------------------------------ helpers
function cor(doc, nome, cmyk) {
    var c = doc.colors.itemByName(nome);
    if (!c.isValid) c = doc.colors.add({ name: nome, model: ColorModel.PROCESS, space: ColorSpace.CMYK, colorValue: cmyk });
    return c;
}

function estilo(doc, nome, props) {
    var s = doc.paragraphStyles.itemByName(nome);
    if (!s.isValid) s = doc.paragraphStyles.add({ name: nome });
    try { s.appliedFont = props.fonte || CFG.fonte; } catch (e) {}
    try { if (props.fontStyle) s.fontStyle = props.fontStyle; } catch (e) {}
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

function fonteExiste(familia) {
    var fs = app.fonts.everyItem().fontFamily;
    for (var i = 0; i < fs.length; i++) if (fs[i] === familia) return true;
    return false;
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

    estilo(doc, "Secao",  { size: 16, cor: cMarca, fontStyle: "Bold" });
    estilo(doc, "SecaoIdiomas", { size: 8, cor: cSuave, fontStyle: "Italic" });
    estilo(doc, "NomePT", { size: 8, cor: cTexto, fontStyle: "Bold", after: 0.6 });
    estilo(doc, "NomeEN", { size: 6.2, cor: cSuave, fontStyle: "Italic" });
    estilo(doc, "NomeES", { size: 6.2, cor: cSuave, fontStyle: "Italic", after: 0.8 });
    estilo(doc, "Specs",  { size: 6.2, cor: cTexto });
    estilo(doc, "Preco",  { size: 11, cor: cMarca, fontStyle: "Bold", just: Justification.RIGHT_ALIGN });
    estilo(doc, "EAN",    { size: 6.5, cor: doc.colors.itemByName("Black"), fonte: CFG.fonteEAN });
    estilo(doc, "Selo",   { size: 6, cor: doc.swatches.itemByName("Paper"), fontStyle: "Bold", just: Justification.CENTER_ALIGN });
    estilo(doc, "Rodape", { size: 6, cor: cSuave });
    estilo(doc, "SemFoto", { size: 6, cor: cSuave, just: Justification.CENTER_ALIGN });
    // se a fonte do EAN não existir, cai na fonte padrão sem quebrar
    if (!fonteExiste(CFG.fonteEAN)) doc.paragraphStyles.itemByName("EAN").appliedFont = CFG.fonte;

    var lyFundo = doc.layers[0]; lyFundo.name = "Fundo";
    var lyProd = doc.layers.add({ name: "Produtos" });
    var lyPreco = doc.layers.add({ name: "Preço", layerColor: UIColors.RED });

    var areaW = CFG.pagina.w - CFG.margem.left - CFG.margem.right;
    var areaH = CFG.pagina.h - CFG.margem.top - CFG.margem.bottom;
    var g = CFG.grade, cw = (areaW - (g.cols - 1) * g.gutter) / g.cols, ch = (areaH - (g.rows - 1) * g.gutter) / g.rows;
    var porPagina = g.cols * g.rows;

    var semFoto = [], estouro = [], eanRuim = [];
    var pg = null, pos = porPagina, secaoAtual = null, nPag = 0;

    function novaPagina(it) {
        pg = (nPag === 0) ? doc.pages[0] : doc.pages.add();
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

    for (var n = 0; n < itens.length; n++) {
        var it = itens[n];
        if (it.LINHA_PT !== secaoAtual || pos >= porPagina) {
            novaPagina(it);
            secaoAtual = it.LINHA_PT;
        }
        var col = pos % g.cols, row = Math.floor(pos / g.cols);
        var x = CFG.margem.left + col * (cw + g.gutter), y = CFG.margem.top + row * (ch + g.gutter);
        pos++;

        // moldura do card
        pg.rectangles.add(lyFundo, undefined, undefined, {
            geometricBounds: [y, x, y + ch, x + cw], fillColor: "None", strokeColor: cBorda, strokeWeight: 0.5
        });

        // foto
        var fotoH = ch * 0.47;
        var fr = pg.rectangles.add(lyProd, undefined, undefined, {
            geometricBounds: [y + 2, x + 2, y + fotoH, x + cw - 2], strokeWeight: 0, fillColor: "None", label: "foto:" + it.FOTO
        });
        var f = achaFoto(pastaFotos, it.FOTO);
        if (f) {
            try { fr.place(f); fr.fit(FitOptions.PROPORTIONALLY); fr.fit(FitOptions.CENTER_CONTENT); }
            catch (e) { semFoto.push(it.REFERENCIA + " (erro ao colocar: " + e + ")"); }
        } else {
            fr.fillColor = cBorda; fr.fillTint = 40;
            txt(pg, lyProd, [y + fotoH / 2 - 3, x + 2, y + fotoH / 2 + 4, x + cw - 2], "SEM FOTO\r" + it.FOTO, "SemFoto");
            semFoto.push(it.REFERENCIA);
        }
        if (it.LANCAMENTO === "S") {
            pg.rectangles.add(lyProd, undefined, undefined, { geometricBounds: [y + 2, x + 2, y + 6, x + 20], fillColor: cSelo, strokeWeight: 0 });
            txt(pg, lyProd, [y + 2.7, x + 2, y + 6, x + 20], "LANÇAMENTO", "Selo");
        }

        // textos
        var specs1 = juntaNaoVazios([
            juntaNaoVazios([it.COR_PT, it.COR_EN, it.COR_ES], " / "),
            it.VOLUME, it.TAMANHO], "  ·  ");
        var specs2 = "Ref. " + it.REFERENCIA + (it.QTD_CAIXA ? "   ·   Cx " + it.QTD_CAIXA + " un" : "");
        var conteudo = it.NOME_PT + "\r" + it.NOME_EN + "\r" + it.NOME_ES + "\r" + (specs1 ? specs1 + "\r" : "") + specs2;
        var tf = pg.textFrames.add(lyProd, undefined, undefined, {
            geometricBounds: [y + fotoH + 1.5, x + 3, y + ch - CFG.eanAltura - 6, x + cw - 3], contents: conteudo
        });
        tf.textFramePreferences.insetSpacing = [0, 0, 0, 0];
        var ps = tf.parentStory.paragraphs, k, nomes = ["NomePT", "NomeEN", "NomeES"];
        for (k = 0; k < ps.length; k++)
            ps[k].appliedParagraphStyle = doc.paragraphStyles.itemByName(k < 3 ? nomes[k] : "Specs");
        if (!encaixa(tf)) estouro.push(it.REFERENCIA + " — " + it.NOME_PT);

        // código de barras
        var by = y + ch - CFG.eanAltura - 5;
        if (it.EAN13 && eanValido(it.EAN13)) {
            desenhaEAN(pg, lyProd, it.EAN13, x + 1, by);
        } else {
            txt(pg, lyProd, [by + 4, x + 3, by + 9, x + cw / 2], it.EAN13 ? "EAN inválido" : "EAN em cadastro", "Specs");
            eanRuim.push(it.REFERENCIA + " — " + (it.EAN13 || "sem EAN"));
        }

        // preço (camada própria)
        if (it.PRECO) txt(pg, lyPreco, [y + ch - 9, x + cw / 2, y + ch - 2, x + cw - 3], it.PRECO, "Preco");
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
