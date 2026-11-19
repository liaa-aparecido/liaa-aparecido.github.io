#!/usr/bin/env python3
"""
Gera o vídeo de apresentação do Faro como sequência de frames PNG,
depois chama ffmpeg para montar o MP4.
Estilo: painel animado (frames estáticos por cena) com visual dark igual ao site.
"""

import os, math, textwrap
from PIL import Image, ImageDraw, ImageFont

# ── Fontes ──────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype"
def font(size, bold=False):
    if bold:
        try:
            return ImageFont.truetype(f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", size)
        except Exception:
            pass
    try:
        return ImageFont.truetype(f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", size)
    except Exception:
        return ImageFont.load_default()

# ── Paleta (igual ao site) ───────────────────────────────────────────────────
BG      = (7,  16,  28)
BG2     = (13, 27,  42)
CARD    = (17, 31,  51)
LINE    = (30, 48,  80)
AZUL    = (79, 145, 255)
VERDE   = (34, 214, 122)
AMAR    = (245,197, 24)
VERM    = (240, 77,  77)
ROSA    = (232,121, 249)
CZ      = (139,163, 192)
BRANCO  = (232,240, 254)

W, H = 1280, 720
FRAMES_DIR = "/tmp/faro_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def new_frame():
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)
    # grade de fundo sutil
    for x in range(0, W, 80):
        d.line([(x, 0), (x, H)], fill=(30, 48, 80, 20), width=1)
    for y in range(0, H, 80):
        d.line([(0, y), (W, y)], fill=(30, 48, 80, 20), width=1)
    return img, d

def logo_bar(d):
    """Barra de topo com logo."""
    d.rectangle([(0, 0), (W, 52)], fill=(10, 20, 36))
    d.rectangle([(0, 52), (W, 54)], fill=AZUL)
    d.text((22, 12), "🛡 Faro: Regras de Firewall com IA", font=font(20, bold=True), fill=AZUL)
    d.text((W-320, 15), "LIAA 2026 · UNIPAMPA", font=font(16), fill=CZ)

def bottom_bar(d, scene_n, total=8):
    """Barra inferior com número de cena."""
    d.rectangle([(0, H-38), (W, H)], fill=(10, 20, 36))
    d.text((22, H-27), f"Cena {scene_n}/{total}  ·  Aparecido de Souza Vieira Junior", font=font(14), fill=CZ)
    # barra de progresso
    pw = int((scene_n/total)*(W-44))
    d.rectangle([(22, H-10), (W-22, H-5)], fill=LINE)
    d.rectangle([(22, H-10), (22+pw, H-5)], fill=AZUL)

def card_box(d, x, y, w, h, color=AZUL, title="", body_lines=None, icon=""):
    """Desenha um card com borda colorida no topo."""
    d.rectangle([(x, y), (x+w, y+h)], fill=CARD, outline=LINE, width=1)
    d.rectangle([(x, y), (x+w, y+4)], fill=color)
    tx = x + 14
    ty = y + 14
    if icon:
        d.text((tx, ty), icon, font=font(28), fill=color)
        tx += 42
    if title:
        d.text((tx, ty+2), title, font=font(18, bold=True), fill=BRANCO)
    if body_lines:
        for i, line in enumerate(body_lines):
            d.text((x+14, ty+36+i*24), line, font=font(14), fill=CZ)

def arrow_right(d, x, y, color=AZUL):
    pts = [(x, y-6), (x+22, y), (x, y+6)]
    d.polygon(pts, fill=color)

def save_scene(img, frame_id, duration_s=4, fps=25):
    """Salva N frames iguais para simular duração."""
    n = int(duration_s * fps)
    for i in range(n):
        img.save(f"{FRAMES_DIR}/frame_{frame_id:04d}_{i:03d}.png")

# ═══════════════════════════════════════════════════════════════════
# CENA 0 — ABERTURA (título)
# ═══════════════════════════════════════════════════════════════════
def cena_0():
    img, d = new_frame()
    # gradiente simulado com retângulos
    for i in range(H):
        t = i / H
        r = int(7 + t*6)
        g = int(16 + t*10)
        b = int(28 + t*20)
        d.line([(0, i), (W, i)], fill=(r, g, b))

    # Círculo decorativo central
    cx, cy = W//2, H//2 - 30
    for r in range(180, 0, -20):
        alpha = int(255 * (1 - r/200) * 0.15)
        d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=(*AZUL, alpha), width=1)

    d.text((W//2, cy - 60), "🛡", font=font(72), fill=AZUL, anchor="mm")
    d.text((W//2, cy + 50), "FARO", font=font(68, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, cy + 115), "Regras de Firewall com IA", font=font(28), fill=AZUL, anchor="mm")
    d.text((W//2, cy + 160), "Como a IA identifica o risco real em 48.915 alertas", font=font(18), fill=CZ, anchor="mm")
    d.text((W//2, cy + 200), "Aparecido de Souza Vieira Junior · LIAA 2026/2 · UNIPAMPA", font=font(16), fill=CZ, anchor="mm")
    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 1 — O CENÁRIO
# ═══════════════════════════════════════════════════════════════════
def cena_1():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 1)

    d.text((W//2, 95), "O cenário: um firewall real em produção", font=font(30, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 135), "Rede real · OPNsense · Suricata · Alertas reais", font=font(18), fill=CZ, anchor="mm")

    # Nós: Internet → Suricata / PF
    nodes = [
        (110, 320, "🌐", "Internet", "Tráfego WAN", CZ),
        (340, 240, "📡", "Suricata 8.0.8", "IDS wire/pcap", AMAR),
        (340, 400, "🔒", "OPNsense PF", "26.7.8_2", VERDE),
        (590, 320, "🔗", "Community ID", "Junção exata", AZUL),
        (820, 320, "🤖", "Pipeline IA", "propor_regra.py", ROSA),
        (1070,320, "📋", "5 Regras", "bloqueadas via API", VERDE),
    ]
    for (x, y, ico, title, sub, col) in nodes:
        card_box(d, x-80, y-55, 160, 100, color=col, title=title, icon=ico)
        d.text((x, y+20), sub, font=font(13), fill=col, anchor="mm")

    # Setas
    arrow_right(d, 190, 265, AMAR)
    arrow_right(d, 190, 405, VERDE)
    # setas de Suricata e PF para Community ID
    d.line([(340, 285), (510, 320)], fill=AZUL, width=2)
    d.line([(340, 445), (510, 340)], fill=AZUL, width=2)
    arrow_right(d, 510, 320, AZUL)
    arrow_right(d, 670, 320, AZUL)
    arrow_right(d, 900, 320, VERDE)

    # Stat
    d.rectangle([(30, 540), (380, 640)], fill=BG2, outline=LINE)
    d.text((205, 560), "48.915", font=font(36, bold=True), fill=AZUL, anchor="mm")
    d.text((205, 605), "alertas do Suricata", font=font(16), fill=CZ, anchor="mm")

    d.rectangle([(410, 540), (760, 640)], fill=BG2, outline=LINE)
    d.text((585, 560), "473.304", font=font(36, bold=True), fill=VERDE, anchor="mm")
    d.text((585, 605), "linhas de filterlog", font=font(16), fill=CZ, anchor="mm")

    d.rectangle([(790, 540), (1140, 640)], fill=BG2, outline=LINE)
    d.text((965, 560), "31 dias", font=font(36, bold=True), fill=AMAR, anchor="mm")
    d.text((965, 605), "de coleta em produção", font=font(16), fill=CZ, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 2 — O PROBLEMA
# ═══════════════════════════════════════════════════════════════════
def cena_2():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 2)

    d.text((W//2, 95), "O problema: 48.915 alertas. Qual é o risco real?", font=font(28, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 130), "O Suricata vê o pacote antes do PF decidir — volume ≠ risco.", font=font(17), fill=CZ, anchor="mm")

    # Funil
    funil = [
        (900, AZUL,  "48.915",   "alertas Suricata (100%)"),
        (730, VERDE, "42.804",   "PF já tratou (87,3%)"),
        (500, AMAR,  "6.012",    "passaram (12,3%)"),
        (250, ROSA,  "18",       "externos reais"),
        (140, VERDE, "LEGÍTIMOS","todos legítimos ✓"),
    ]
    y = 175
    for w_bar, col, num, label in funil:
        x0 = (W - w_bar) // 2
        d.rectangle([(x0, y), (x0+w_bar, y+62)], fill=(*col, 30), outline=col, width=1)
        d.text((W//2, y+20), num, font=font(22, bold=True), fill=col, anchor="mm")
        d.text((W//2, y+44), label, font=font(13), fill=CZ, anchor="mm")
        y += 70
        if y < 580:
            d.text((W//2, y-4), "▼", font=font(14), fill=LINE, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 3 — COMMUNITY ID: a chave que une os logs
# ═══════════════════════════════════════════════════════════════════
def cena_3():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 3)

    d.text((W//2, 95), "A chave que une os dois sistemas: Community ID", font=font(28, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 130), "Mesmo fluxo em eve.json e filterlog → junção exata sem heurística", font=font(17), fill=CZ, anchor="mm")

    # Dois logs lado a lado
    # eve.json
    card_box(d, 60, 170, 530, 220, color=AMAR, title="eve.json  (Suricata)", icon="📡")
    lines_eve = [
        '{ "timestamp": "2026-10-13T14:22:08",',
        '  "community_id": "1:abc123xyz==",',
        '  "src_ip": "185.220.101.42",',
        '  "alert": {"signature": "ET EXPLOIT Realtek",',
        '            "severity": 1 } }',
    ]
    for i, l in enumerate(lines_eve):
        d.text((74, 265+i*26), l, font=font(13), fill=CZ)

    # filterlog
    card_box(d, 690, 170, 530, 220, color=VERDE, title="filterlog  (OPNsense PF)", icon="🔒")
    lines_pf = [
        "Nov  3 14:22:08 OPNsense filterlog:",
        "  rule=12,interface=igb0,reason=block,",
        "  action=block,proto=tcp,",
        "  community_id=1:abc123xyz==,",
        "  src=185.220.101.42,dst=192.168.1.1",
    ]
    for i, l in enumerate(lines_pf):
        d.text((704, 265+i*26), l, font=font(13), fill=CZ)

    # Seta de junção
    d.rectangle([(460, 260), (690, 310)], fill=BG2, outline=AZUL, width=2)
    d.text((575, 285), "🔗 Community ID", font=font(16, bold=True), fill=AZUL, anchor="mm")

    # Resultado
    d.rectangle([(60, 420), (1220, 490)], fill=(*VERDE, 15), outline=VERDE, width=1)
    d.text((W//2, 445), "Resultado da junção:", font=font(16, bold=True), fill=VERDE, anchor="mm")
    d.text((W//2, 470), "Desfecho: BLOCK  ·  IP: 185.220.101.42  ·  SIG: ET EXPLOIT Realtek SDK  ·  Candidato a bloqueio ✅", font=font(15), fill=BRANCO, anchor="mm")

    # 3 desfechos
    card_box(d, 60,  508, 360, 150, color=CZ,   title="SEM REGISTRO", icon="⬜", body_lines=["42.639 alertas","default deny ativo"])
    card_box(d, 460, 508, 360, 150, color=VERM,  title="BLOCK",        icon="🚫", body_lines=["165 alertas","bloqueio explícito"])
    card_box(d, 860, 508, 360, 150, color=AMAR,  title="PASS",         icon="✅", body_lines=["6.012 alertas","passaram pelo PF"])

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 4 — AS 3 TRILHAS
# ═══════════════════════════════════════════════════════════════════
def cena_4():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 4)

    d.text((W//2, 95), "O funil separa 3 trilhas com causas distintas", font=font(28, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 130), "Cada trilha tem um tratamento diferente — sem generalizar o problema", font=font(17), fill=CZ, anchor="mm")

    cards = [
        (60,  180, 360, 460, CZ,   "⬜", "Trilha Interna",
         ["6.495 alertas", "Host 192.168.15.200", "STUN, Discord, DNS .biz", "Falso positivo legítimo", "→ suppress no Suricata"]),
        (460, 180, 360, 460, AMAR, "📋", "Trilha Reputação",
         ["1.377 alertas", "IP nas listas, não no PF", "ET CINS / DShield", "Divergência entre feeds", "→ medir latência de listas"]),
        (860, 180, 360, 460, VERM, "🚨", "Trilha Comportamento",
         ["20 alertas", "Realtek CVE-2021-35394", "Exploit ativo detectado", "5 IPs → API OPNsense", "→ 5 regras ativas ✅"]),
    ]
    for (x, y, w, h, col, ico, title, lines) in cards:
        card_box(d, x, y, w, h, color=col, title=title, icon=ico, body_lines=lines)

    # Destaque resultado
    d.rectangle([(60, 650), (1220, 695)], fill=(*VERDE, 15), outline=VERDE, width=1)
    d.text((W//2, 672), "🎯  5 regras IA-aparecido ativas no OPNsense  ·  0% falso positivo  ·  100% cobertura Realtek",
           font=font(16, bold=True), fill=VERDE, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 5 — O RESULTADO DO SPLIT TEMPORAL
# ═══════════════════════════════════════════════════════════════════
def cena_5():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 5)

    d.text((W//2, 95), "Split temporal: a IA prova que não mente", font=font(28, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 130), "Treino em Período A → teste em Período B, sem vazamento de dados", font=font(17), fill=CZ, anchor="mm")

    # Linha do tempo
    d.rectangle([(100, 220), (1150, 280)], fill=BG2, outline=LINE)
    d.rectangle([(100, 220), (620, 280)], fill=(*AZUL, 40), outline=AZUL, width=2)
    d.rectangle([(620, 220), (1150, 280)], fill=(*VERDE, 30), outline=VERDE, width=2)
    d.text((360, 250), "Período A — Treino  09/10 → 25/10", font=font(15, bold=True), fill=AZUL, anchor="mm")
    d.text((885, 250), "Período B — Teste  26/10 → 08/11", font=font(15, bold=True), fill=VERDE, anchor="mm")
    d.line([(620, 200), (620, 300)], fill=AMAR, width=3)
    d.text((620, 190), "Corte temporal", font=font(13), fill=AMAR, anchor="mm")

    # Stats
    stats = [
        (200,  360, AZUL,  "509",   "IPs únicos  (A)"),
        (200,  480, AZUL,  "5,8M",  "fluxos PF (A)"),
        (640,  360, VERDE, "416",   "IPs únicos  (B)"),
        (640,  480, VERDE, "4,8M",  "fluxos PF (B)"),
        (1050, 360, AMAR,  "308",   "IPs recorrentes"),
        (1050, 480, VERM,  "195",   "IPs resíduo (A→B)"),
    ]
    for x, y, col, val, lbl in stats:
        d.rectangle([(x-110, y-40), (x+110, y+50)], fill=CARD, outline=col, width=1)
        d.text((x, y),    val, font=font(28, bold=True), fill=col, anchor="mm")
        d.text((x, y+28), lbl, font=font(13),            fill=CZ,  anchor="mm")

    # Resultado final
    d.rectangle([(60, 560), (1220, 650)], fill=(*VERDE, 15), outline=VERDE, width=1)
    d.text((W//2, 585), "Resultado:", font=font(17, bold=True), fill=VERDE, anchor="mm")
    d.text((W//2, 615), "Família IP individual (4.945 regras): 0% colateral  ·  Família comportamento (169 regras): 0% colateral",
           font=font(15), fill=BRANCO, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 6 — A REGRA EM AÇÃO (CVE-2021-35394 Realtek)
# ═══════════════════════════════════════════════════════════════════
def cena_6():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 6)

    d.text((W//2, 95), "A regra em ação: CVE-2021-35394 (Realtek SDK)", font=font(28, bold=True), fill=BRANCO, anchor="mm")
    d.text((W//2, 130), "8 alertas de exploit real → 5 IPs bloqueados via API REST no OPNsense", font=font(17), fill=CZ, anchor="mm")

    # Fluxo passo a passo
    passos = [
        (120, 210, AMAR,  "1", "Suricata detecta\nET EXPLOIT Realtek\n(SID 2034037)"),
        (340, 210, AZUL,  "2", "Community ID\nune com filterlog\ndesfecho: PASS"),
        (560, 210, VERM,  "3", "Filtro camadas:\nnão está em\nAbuseIPDB"),
        (780, 210, ROSA,  "4", "IA analisa\ncomportamento\n→ candidato"),
        (1000,210, VERDE, "5", "API REST\nOPNsense\nbloqueio aplicado"),
    ]
    for x, y, col, n, txt in passos:
        d.ellipse([(x-45, y-45), (x+45, y+45)], fill=(*col, 30), outline=col, width=2)
        d.text((x, y-5), n, font=font(28, bold=True), fill=col, anchor="mm")
        for i, l in enumerate(txt.split("\n")):
            d.text((x, y+55+i*22), l, font=font(13), fill=CZ, anchor="mm")
        if x < 1000:
            d.text((x+118, y), "→", font=font(26, bold=True), fill=LINE, anchor="mm")

    # Código da API
    d.rectangle([(60, 390), (1220, 580)], fill=BG2, outline=LINE)
    d.text((80, 405), "# propor_regra.py — chamada à API REST do OPNsense", font=font(14), fill=CZ)
    code_lines = [
        "regra = {",
        '  "descricao":  "IA-aparecido: Realtek CVE-2021-35394",',
        '  "interface":  "wan",',
        '  "protocol":  "udp",',
        '  "src":        "185.220.101.42",',
        '  "action":     "block"',
        "}",
        'resp = requests.post(f"{OPNSENSE}/api/firewall/rules/add", json=regra)',
        '# → HTTP 200  {"result": "saved"}  ✅',
    ]
    for i, l in enumerate(code_lines):
        col = VERDE if "HTTP 200" in l else (AZUL if "IA-aparecido" in l else CZ)
        d.text((80, 428+i*17), l, font=font(13), fill=col)

    # Resultado
    d.rectangle([(60, 590), (1220, 650)], fill=(*VERDE, 15), outline=VERDE, width=1)
    d.text((W//2, 620), "5 regras IA-aparecido ativas · 336.049 fluxos benignos testados · 0% falso positivo", font=font(16, bold=True), fill=VERDE, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 7 — CONCLUSÃO / RESPOSTA À PERGUNTA
# ═══════════════════════════════════════════════════════════════════
def cena_7():
    img, d = new_frame()
    logo_bar(d)
    bottom_bar(d, 7)

    d.text((W//2, 95), "Resposta à pergunta de pesquisa", font=font(30, bold=True), fill=BRANCO, anchor="mm")

    d.rectangle([(60, 150), (1220, 300)], fill=(*VERDE, 12), outline=VERDE, width=2)
    d.text((W//2, 185), "🎯  Conclusão", font=font(22, bold=True), fill=VERDE, anchor="mm")
    d.text((W//2, 225),
           "Dada a política blacklist + default deny do OPNsense,",
           font=font(17), fill=BRANCO, anchor="mm")
    d.text((W//2, 255),
           "os fluxos que passam são tráfego legítimo. O firewall já funciona corretamente.",
           font=font(17), fill=BRANCO, anchor="mm")
    d.text((W//2, 282),
           "O volume de alertas do Suricata superestima o risco em 87%.",
           font=font(16), fill=CZ, anchor="mm")

    # 4 métricas finais
    metricas = [
        (200,  420, VERDE, "0%",    "Falso positivo"),
        (520,  420, VERDE, "87,3%", "Alertas já tratados"),
        (840,  420, VERDE, "100%",  "Cobertura Realtek"),
        (1120, 420, VERDE, "5",     "Regras ativas"),
    ]
    for x, y, col, val, lbl in metricas:
        d.rectangle([(x-110, y-50), (x+110, y+55)], fill=CARD, outline=col, width=2)
        d.text((x, y),    val, font=font(34, bold=True), fill=col,  anchor="mm")
        d.text((x, y+32), lbl, font=font(13),            fill=CZ,   anchor="mm")

    # CrowdSec baseline
    d.rectangle([(60, 540), (1220, 600)], fill=BG2, outline=LINE)
    d.text((W//2, 570),
           "Baseline independente: CrowdSec (8.328 IPs) concorda — 0% cobertura incremental. Ambos chegam à mesma conclusão.",
           font=font(14), fill=CZ, anchor="mm")

    # Próximos passos
    d.text((W//2, 630), "Próximos passos: comparação de modelos LLM · colaboração com ModSecurity · publicação SBSeg",
           font=font(14), fill=AZUL, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# CENA 8 — ENCERRAMENTO
# ═══════════════════════════════════════════════════════════════════
def cena_8():
    img, d = new_frame()

    # gradiente
    for i in range(H):
        t = i / H
        r = int(7 + t*6)
        g = int(16 + t*10)
        b = int(28 + t*22)
        d.line([(0, i), (W, i)], fill=(r, g, b))

    cx, cy = W//2, H//2 - 20
    for r in range(220, 0, -25):
        d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=(*VERDE, 15), width=1)

    d.text((cx, cy-80),  "🛡",                                     font=font(72), fill=VERDE, anchor="mm")
    d.text((cx, cy+20),  "FARO",                                   font=font(60, bold=True), fill=BRANCO, anchor="mm")
    d.text((cx, cy+78),  "Regras de Firewall com IA",              font=font(26), fill=AZUL,  anchor="mm")
    d.text((cx, cy+120), "liaa-aparecido.github.io",               font=font(20), fill=CZ,   anchor="mm")
    d.text((cx, cy+160), "Aparecido de Souza Vieira Junior · LIAA 2026/2 · UNIPAMPA",
                                                                    font=font(16), fill=CZ,   anchor="mm")
    d.text((cx, cy+200), "github.com/liaa-aparecido/firewall-ia",  font=font(16), fill=AZUL, anchor="mm")

    return img

# ═══════════════════════════════════════════════════════════════════
# RENDERIZAR TODAS AS CENAS
# ═══════════════════════════════════════════════════════════════════
print("Gerando frames…")

cenas = [
    (cena_0(), 0, 5.0),
    (cena_1(), 1, 7.0),
    (cena_2(), 2, 7.0),
    (cena_3(), 3, 8.0),
    (cena_4(), 4, 7.0),
    (cena_5(), 5, 7.0),
    (cena_6(), 6, 8.0),
    (cena_7(), 7, 7.0),
    (cena_8(), 8, 5.0),
]

frame_counter = 0
FPS = 25

for (img, scene_id, dur) in cenas:
    n_frames = int(dur * FPS)
    for fi in range(n_frames):
        img.save(f"{FRAMES_DIR}/f{frame_counter:06d}.png")
        frame_counter += 1
    print(f"  Cena {scene_id}: {n_frames} frames ({dur}s)")

print(f"\nTotal: {frame_counter} frames")
print("Montando MP4 com ffmpeg…")

out = "/home/aparecido/Documentos/MESTRADO/liaa-aparecido.github.io/assets/faro_video.mp4"
os.makedirs(os.path.dirname(out), exist_ok=True)

cmd = (
    f"ffmpeg -y -framerate {FPS} "
    f"-pattern_type glob -i '{FRAMES_DIR}/f*.png' "
    f"-c:v libx264 -preset slow -crf 18 "
    f"-pix_fmt yuv420p -movflags +faststart "
    f'"{out}"'
)
ret = os.system(cmd)
if ret == 0:
    size = os.path.getsize(out) // 1024
    print(f"\n✅  Vídeo gerado: {out}  ({size} KB)")
else:
    print(f"\n❌  ffmpeg falhou (código {ret})")
