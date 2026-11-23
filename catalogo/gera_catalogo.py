#!/usr/bin/env python3
"""
Monta a base do catálogo Nitron a partir da extração do Sankhya.

Entrada (nesta pasta):
  dados/sankhya_raw.txt   extração da tabela padrão (CODTAB 0), ativos e não suspensos — ver sql/extrai_tabela_padrao.sql
  traducoes.csv           nome-base -> PT / EN / ES   (o marketing edita)
  cores.csv               cor escrita no nome -> PT / EN / ES
  cores_codigo.csv        3ª parte da referência (REF.EMB.COR) -> cor; usado quando o nome não diz a cor
  linhas.csv              grupo do Sankhya -> seção do catálogo, ordem e tradução
  lancamentos.csv         produtos ainda não cadastrados (o marketing preenche)
  excluir.csv             (opcional) CODPROD ou REFERENCIA a tirar do catálogo

Saída (pasta saida/):
  catalogo_indesign.csv   o arquivo que o script do InDesign lê (UTF-8, separador ;)
  catalogo_mestre.xlsx    para revisão: abas Catálogo, Pendências, Traduções faltando
"""
import csv, re, unicodedata, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "saida"; OUT.mkdir(exist_ok=True)

def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def ler_csv(nome):
    p = BASE / nome
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))

def ean_dv(doze):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(doze))
    return str((10 - s % 10) % 10)

def ean_completa(e):
    """Aceita 12 dígitos (calcula o verificador) ou 13 (devolve como veio). Ignora espaços e pontos."""
    e = re.sub(r"\D", "", e or "")
    return e + ean_dv(e) if len(e) == 12 else e

def ean_ok(e):
    if not (len(e) == 13 and e.isdigit()):
        return False
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(e[:12]))
    return (10 - s % 10) % 10 == int(e[12])

CORES = {sem_acento(r["CHAVE"]).upper(): r for r in ler_csv("cores.csv")}
COR_RE = "|".join(sorted(map(re.escape, CORES), key=len, reverse=True))
TRAD = {sem_acento(r["CHAVE"]).upper(): r for r in ler_csv("traducoes.csv")}
LINHAS = {r["GRUPO"]: r for r in ler_csv("linhas.csv")}
COR_COD = {r["CODIGO_COR"]: r for r in ler_csv("cores_codigo.csv")}
EXCLUIR = {r.get("CHAVE", "").strip() for r in ler_csv("excluir.csv")}

def formata_volume(qtd, uni):
    uni = uni.upper()
    n = qtd.replace(".", ",")
    if uni in ("L", "LT"):
        return f"{n} L"
    if uni == "ML":
        return f"{n} ml"
    if uni == "KG":
        return f"{n} kg"
    return f"{n} g"

def decompor(nome):
    """Separa nome do Sankhya em: chave do nome-base, cor, volume, tamanho."""
    n = sem_acento(nome).upper().strip()
    n = re.sub(r"\s*\([^)]*\)\s*$", "", n)                     # (018/B), (0307.012.001) no fim
    tam = ""
    m = re.search(r"(\d+)\s*X\s*(\d+)\s*X\s*(\d+)\s*MM", n)
    if m:
        tam = f"{m.group(1)} x {m.group(2)} x {m.group(3)} mm"
        n = n[:m.start()] + n[m.end():]
    vol = ""
    m = re.search(r"(\d+(?:[,.]\d+)?)\s*(ML|LT|L|KG|G)\b", n)
    if m:
        vol = formata_volume(m.group(1), m.group(2))
        n = n[:m.start()] + n[m.end():]
    cor = ""
    m = re.search(r"\b(" + COR_RE + r")\b", n)
    if m:
        cor = m.group(1)
        n = n[:m.start()] + n[m.end():]
    n = re.sub(r"[\s-]+$", "", n)
    n = re.sub(r"\s+-\s+-\s+", " - ", n)
    n = re.sub(r"\s+", " ", n).strip(" -")
    return n, cor, vol, tam

REF_RE = re.compile(r"^(\d{3,4})\.(\d{3})\.([0-9A-Z]{3})$")

def partes_ref(ref):
    """REF.EMB.COR -> (macro, embalagem master, código de cor) ou None."""
    m = REF_RE.match(ref)
    return m.groups() if m else None

def volume_ml(v):
    m = re.match(r"([\d,]+)\s*(ml|L|kg|g)", v or "")
    if not m:
        return 0
    n = float(m.group(1).replace(",", "."))
    return n * 1000 if m.group(2) in ("L", "kg") else n

def preco_br(v):
    if v in ("", None):
        return ""
    return "R$ " + f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

linhas_saida, pend = [], []

def pendencia(item, campo, problema):
    pend.append({"CODPROD": item.get("CODPROD", ""), "REFERENCIA": item["REFERENCIA"],
                 "PRODUTO": item.get("PRODUTO_SANKHYA", item.get("NOME_PT", "")),
                 "CAMPO": campo, "PROBLEMA": problema})

# ---------- 1. produtos do Sankhya
for l in open(BASE / "dados" / "sankhya_raw.txt", encoding="utf-8"):
    cod, ref, prod, grupo, ean, ean_sit, cx, mult, preco = l.rstrip("\n").split("|")
    if cod in EXCLUIR or ref in EXCLUIR:
        continue
    chave, cor, vol, tam = decompor(prod)
    t = TRAD.get(chave)
    c = CORES.get(cor, {})
    pr = partes_ref(ref)
    cor_do_codigo = COR_COD.get(pr[2], {}) if pr else {}
    cor_inferida = False
    if not c and cor_do_codigo:
        c, cor_inferida = cor_do_codigo, True
    ln = LINHAS.get(grupo, {})
    item = {
        "TIPO": "CATALOGO", "CODPROD": cod, "REFERENCIA": ref, "PRODUTO_SANKHYA": prod,
        "REF_MACRO": pr[0] if pr else ref, "REF_EMB": pr[1] if pr else "", "REF_COR": pr[2] if pr else "",
        "ORDEM_LINHA": ln.get("ORDEM", "999"), "LINHA_PT": ln.get("LINHA_PT", grupo),
        "LINHA_EN": ln.get("LINHA_EN", ""), "LINHA_ES": ln.get("LINHA_ES", ""), "POR_LINHA": ln.get("POR_LINHA", ""),
        "NOME_PT": t["NOME_PT"] if t else prod.title(),
        "NOME_EN": t["NOME_EN"] if t else "", "NOME_ES": t["NOME_ES"] if t else "",
        "COR_PT": c.get("COR_PT", ""), "COR_EN": c.get("COR_EN", ""), "COR_ES": c.get("COR_ES", ""),
        "VOLUME": vol, "TAMANHO": tam, "QTD_CAIXA": cx, "EAN13": ean,
        "PRECO": preco_br(preco), "LANCAMENTO": "",
        "FOTO": ref,  # o InDesign procura <REFERENCIA>.png/.jpg/.psd/.tif na pasta de fotos
    }
    if not t:
        pendencia(item, "TRADUCAO", f"nome-base sem tradução: '{chave}' — incluir em traducoes.csv")
    elif t.get("REVISAR") == "S":
        pendencia(item, "TRADUCAO", "tradução marcada para revisão (nome ambíguo no cadastro)")
    if not ean:
        pendencia(item, "EAN13", f"sem EAN no Sankhya ({ean_sit})")
    elif not ean_ok(ean):
        pendencia(item, "EAN13", f"EAN com dígito verificador inválido: {ean}")
    if not pr:
        pendencia(item, "REFERENCIA", "referência fora do padrão REF.EMB.COR — conferir se é duplicata ou private label")
    else:
        if pr[1].isdigit() and cx and int(pr[1]) != int(cx):
            pendencia(item, "EMBALAGEM", f"referência diz {int(pr[1])} por caixa (…{pr[1]}…), cadastro diz QTD_CAIXA={cx}")
        if cor_do_codigo and c and not cor_inferida and cor_do_codigo["COR_PT"] not in c["COR_PT"]:
            pendencia(item, "COR", f"nome diz '{c['COR_PT']}', código de cor {pr[2]} diz '{cor_do_codigo['COR_PT']}'")
        if cor_inferida:
            pendencia(item, "COR", f"nome sem cor — usei o código {pr[2]} = {c['COR_PT']}; confirmar")
    if not cx or cx == "0":
        pendencia(item, "QTD_CAIXA", "sem quantidade por caixa")
    if not ln:
        pendencia(item, "LINHA", f"grupo '{grupo}' sem seção em linhas.csv")
    linhas_saida.append(item)

# ---------- 2. lançamentos (ainda sem cadastro)
for r in ler_csv("lancamentos.csv"):
    ref = (r.get("REFERENCIA_PROVISORIA") or "").strip()
    if not ref or ref.startswith("EXEMPLO"):
        continue
    ln = LINHAS.get(r.get("LINHA_SANKHYA", ""), {})
    ean_digitado = re.sub(r"\D", "", r.get("EAN13") or "")
    ean = ean_completa(ean_digitado)
    pr = partes_ref(ref)
    item = {
        "TIPO": "LANCAMENTO", "CODPROD": "", "REFERENCIA": ref, "PRODUTO_SANKHYA": "",
        "REF_MACRO": pr[0] if pr else ref, "REF_EMB": pr[1] if pr else "", "REF_COR": pr[2] if pr else "",
        "ORDEM_LINHA": ln.get("ORDEM", "999"), "LINHA_PT": ln.get("LINHA_PT", r.get("LINHA_SANKHYA", "")),
        "LINHA_EN": ln.get("LINHA_EN", ""), "LINHA_ES": ln.get("LINHA_ES", ""), "POR_LINHA": ln.get("POR_LINHA", ""),
        "NOME_PT": r["NOME_PT"], "NOME_EN": r["NOME_EN"], "NOME_ES": r["NOME_ES"],
        "COR_PT": r["COR_PT"], "COR_EN": r["COR_EN"], "COR_ES": r["COR_ES"],
        "VOLUME": r["VOLUME"], "TAMANHO": r["TAMANHO"], "QTD_CAIXA": r["QTD_CAIXA"],
        "EAN13": ean, "PRECO": preco_br(r["PRECO"].replace(",", ".")) if r.get("PRECO") else "",
        "LANCAMENTO": "S", "FOTO": ref,
    }
    if len(ean_digitado) == 12:
        pendencia(item, "EAN13", f"digitaram 12 dígitos — calculei o verificador: {ean}")
    if ean and not ean_ok(ean):
        pendencia(item, "EAN13", f"EAN do lançamento inválido (dígito verificador não confere): {ean}")
    if not ean:
        pendencia(item, "EAN13", "lançamento sem EAN — o card sai com 'EAN em cadastro'")
    linhas_saida.append(item)

# ---------- 3. ordenação: seção, depois referência-mãe, depois cor
def chave_ord(i):
    # seção > produto > tamanho (ml crescente) > macro da referência > cor: as cores do mesmo SKU ficam lado a lado
    return (int(i["ORDEM_LINHA"]), i["NOME_PT"], volume_ml(i["VOLUME"]), i["REF_MACRO"].zfill(4), i["REF_COR"])
linhas_saida.sort(key=chave_ord)

for i in linhas_saida:
    if not i["TAMANHO"]:
        pendencia(i, "TAMANHO", "dimensões não existem na view do Sankhya — preencher ou pedir ao TI")

CAMPOS = ["TIPO", "LINHA_PT", "LINHA_EN", "LINHA_ES", "POR_LINHA", "REFERENCIA", "REF_MACRO", "REF_EMB", "REF_COR", "CODPROD", "NOME_PT", "NOME_EN",
          "NOME_ES", "COR_PT", "COR_EN", "COR_ES", "VOLUME", "TAMANHO", "QTD_CAIXA", "EAN13", "PRECO",
          "LANCAMENTO", "FOTO", "PRODUTO_SANKHYA"]
with open(OUT / "catalogo_indesign.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, CAMPOS, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(linhas_saida)

# ---------- 4. planilha de revisão
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active; ws.title = "Catálogo"
    ws.append(CAMPOS)
    for i in linhas_saida:
        ws.append([i.get(c, "") for c in CAMPOS])
    ws2 = wb.create_sheet("Pendências")
    pc = ["CAMPO", "REFERENCIA", "CODPROD", "PRODUTO", "PROBLEMA"]
    ws2.append(pc)
    for p in sorted(pend, key=lambda p: (p["CAMPO"], p["REFERENCIA"])):
        ws2.append([p[c] for c in pc])
    ws3 = wb.create_sheet("Resumo")
    from collections import Counter
    ws3.append(["Itens no catálogo", len(linhas_saida)])
    ws3.append(["  do Sankhya", sum(1 for i in linhas_saida if i["TIPO"] == "CATALOGO")])
    ws3.append(["  lançamentos", sum(1 for i in linhas_saida if i["TIPO"] == "LANCAMENTO")])
    for k, v in Counter(p["CAMPO"] for p in pend).most_common():
        ws3.append([f"Pendências: {k}", v])
    for s in (ws, ws2, ws3):
        for cell in s[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F3A5F")
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = min(60, max(10, max(len(str(c.value or "")) for c in col) + 2))
        s.freeze_panes = "A2"
    wb.save(OUT / "catalogo_mestre.xlsx")
except ImportError:
    print("openpyxl não instalado — gerei só o CSV", file=sys.stderr)

from collections import Counter
print(f"{len(linhas_saida)} itens -> saida/catalogo_indesign.csv")
for k, v in Counter(p["CAMPO"] for p in pend).most_common():
    print(f"  pendência {k}: {v}")
