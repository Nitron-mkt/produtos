// =====================================================================
//  CÓDIGO DE BARRAS EAN-13 — avulso
//  Digite um ou vários números (12 ou 13 dígitos, separados por vírgula
//  ou espaço/linha) e o script desenha cada código em VETOR na página
//  aberta, um embaixo do outro. Com 12 dígitos ele calcula o verificador.
//  Fonte dos números: Gotham Book.
// =====================================================================
#target indesign

var MODULO = 0.33;   // mm — 100% do tamanho nominal (0,264 = 80%; mínimo recomendado GS1)
var ALTURA = 22.85;  // mm — altura nominal das barras a 100%

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


function fonteBook() {
    var t = ["Gotham\tBook", "Gotham Book\tRegular", "Gotham Book\tBook"];
    for (var i = 0; i < t.length; i++) { var f = app.fonts.itemByName(t[i]); if (f.isValid) return f; }
    return null;
}

function desenha(pg, ean, x, y) {
    var m = MODULO, h = ALTURA, bits = eanBits(ean), q = 11 * m, itens = [], i = 0, ini, g;
    while (i < 95) {
        if (bits.charAt(i) === "1") {
            ini = i; while (i < 95 && bits.charAt(i) === "1") i++;
            g = (ini <= 2) || (ini >= 45 && ini <= 49) || (ini >= 92);
            itens.push(pg.rectangles.add({ geometricBounds: [y, x + q + ini * m, y + h + (g ? 5 * m : 0), x + q + i * m],
                                           fillColor: "Black", strokeWeight: 0 }));
        } else i++;
    }
    var fb = fonteBook(), ty = y + h + 0.3, th = 9 * m, partes = [
        [x, x + q - m, ean.charAt(0), Justification.RIGHT_ALIGN],
        [x + q + 3 * m, x + q + 45 * m, ean.substr(1, 6), Justification.CENTER_ALIGN],
        [x + q + 50 * m, x + q + 92 * m, ean.substr(7, 6), Justification.CENTER_ALIGN]];
    for (var k = 0; k < 3; k++) {
        var t = pg.textFrames.add({ geometricBounds: [ty, partes[k][0], ty + th, partes[k][1]], contents: partes[k][2] });
        t.textFramePreferences.insetSpacing = [0, 0, 0, 0];
        t.parentStory.pointSize = 8 * (MODULO / 0.33);
        t.parentStory.justification = partes[k][3];
        if (fb) t.parentStory.appliedFont = fb;
        itens.push(t);
    }
    var grp = pg.groups.add(itens);
    grp.name = "EAN " + ean;
    return h + th + 4;
}

(function () {
    if (!app.documents.length) { alert("Abra um documento antes."); return; }
    var entrada = prompt("Números do EAN-13 (12 ou 13 dígitos). Vários: separe por vírgula.", "");
    if (!entrada) return;
    var doc = app.activeDocument, pg = app.activeWindow.activePage;
    var hu = doc.viewPreferences.horizontalMeasurementUnits, vu = doc.viewPreferences.verticalMeasurementUnits;
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.MILLIMETERS;
    var lista = entrada.split(/[,;\n]+/), y = 15, erros = [], feitos = [];
    for (var i = 0; i < lista.length; i++) {
        var bruto = lista[i].replace(/\D/g, "");
        if (!bruto) continue;
        var ean = eanCompleta(bruto);
        if (!eanValido(ean)) { erros.push(lista[i] + (bruto.length === 13 ? " (dígito verificador não confere)" : " (precisa de 12 ou 13 dígitos)")); continue; }
        y += desenha(pg, ean, 15, y);
        feitos.push(ean + (bruto.length === 12 ? "  ← verificador calculado" : ""));
    }
    doc.viewPreferences.horizontalMeasurementUnits = hu;
    doc.viewPreferences.verticalMeasurementUnits = vu;
    alert("Desenhados: " + feitos.length + (feitos.length ? "\n" + feitos.join("\n") : "") +
          (erros.length ? "\n\nRECUSADOS (" + erros.length + "):\n" + erros.join("\n") : ""));
})();
