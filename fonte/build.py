#!/usr/bin/env python3
"""Gera o site da AF Fitness Academia na raiz do repositório.
Uso: python3 fonte/build.py
Todos os arquivos ficam soltos na raiz (sem subpastas), para que o envio pelo
navegador ao GitHub não quebre os caminhos."""
import json
import re
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent.parent
HOJE = "2026-11-11"

# ───────────────────────────── DADOS ─────────────────────────────
DOMINIO = "https://SEU-DOMINIO.com.br"   # trocar pelo endereço final antes de divulgar
NOME = "AF Fitness Academia"
FONE_EXIBE = "(85) 98187-6641"
FONE_TEL = "+5585981876641"
WHATS = "5585981876641"                  # confirmar se este número é o WhatsApp
RUA = "R. 15, 190"
BAIRRO_NOME = "Parque Dois Irmãos"
BAIRRO = "Parque Dois Irmãos, Fortaleza - CE"
CEP = "60761-390"
NOTA, N_AVAL = "4,2", 12
VIZINHOS = ["Passaré", "Itaperi", "Dias Macedo"]   # bairros próximos: confirmar
MAPS_Q = "AF Fitness Academia, R. 15, 190 - Parque Dois Irmãos, Fortaleza - CE, 60761-390"
MAPS_ROTA = "https://www.google.com/maps/dir/?api=1&destination=" + quote(MAPS_Q)
MAPS_VER = "https://www.google.com/maps/search/?api=1&query=" + quote(MAPS_Q)
MAPS_EMBED = "https://www.google.com/maps?q=" + quote(MAPS_Q) + "&z=16&output=embed"
SERVICOS = [  # nome, página
    ("Musculação", "musculacao.html"),
    ("Aulas de artes marciais", "aulas.html#artes-marciais"),
    ("Treino funcional", "aulas.html#funcional"),
    ("Exercícios aeróbicos", "aulas.html#aerobico"),
    ("Aulas para jovens", "aulas.html#jovens"),
    ("Personal trainer", "personal-e-nutricao.html#personal"),
    ("Aulas particulares", "personal-e-nutricao.html#aulas-particulares"),
    ("Nutricionista e consultoria em nutrição", "personal-e-nutricao.html#nutricao"),
]
# ─────────────────────────────────────────────────────────────────

WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.46 15.03L2 22l5.1-1.54A9.9 9.9 0 1 0 12.04 2Zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.03.92.94-2.94-.2-.31A8.1 8.1 0 0 1 12.04 3.8Zm-3.4 3.9c-.2 0-.5.07-.76.36-.26.28-1 .98-1 2.38 0 1.4 1.02 2.76 1.17 2.95.14.19 2 3.06 4.86 4.29 2.38 1.02 2.87.82 3.39.77.51-.05 1.66-.68 1.9-1.33.23-.66.23-1.22.16-1.34-.07-.12-.26-.19-.54-.33-.29-.14-1.67-.82-1.93-.92-.26-.09-.45-.14-.64.14-.19.29-.73.92-.9 1.11-.16.19-.33.21-.61.07-.29-.14-1.2-.44-2.29-1.41a8.6 8.6 0 0 1-1.58-1.97c-.17-.28-.02-.44.12-.58.13-.12.29-.33.43-.49.14-.17.19-.29.28-.48.1-.19.05-.35-.02-.5-.07-.13-.63-1.55-.88-2.12-.22-.52-.45-.53-.64-.54l-.52-.06Z"/></svg>')

# Logotipo redesenhado a partir da fachada: seta amarela com "AF" e "FITNESS".
LOGO = ('<svg class="brand-logo" viewBox="0 0 98 60" role="img" aria-label="AF Fitness">'
        '<path d="M0 0h64l34 30-34 30H0z" fill="#f7b90b"/>'
        '<text x="10" y="37" font-family="Archivo, Arial Narrow, Arial, sans-serif" font-weight="900" font-stretch="68%" font-size="36" letter-spacing="-1" fill="#121212">AF</text>'
        '<text x="11" y="51" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="8.5" letter-spacing="2.6" fill="#121212">FITNESS</text></svg>')

ALT = {
    "af-musculacao": "Salão de musculação da AF Fitness com aparelhos e alunos treinando",
    "af-salao": "Área de musculação com aparelhos e piso emborrachado",
    "af-pesos": "Bancos, halteres e aparelhos de musculação vistos de cima",
    "af-aparelhos": "Aparelhos de musculação amarelos e pretos",
    "af-lutas": "Alunos em aula de artes marciais no tatame, em frente ao espelho",
    "af-kimono": "Três praticantes de kimono no tatame da academia",
    "af-turma": "Turma de artes marciais reunida no tatame",
    "af-funcional": "Espaço com piso de madeira, bancos e equipamentos",
    "af-aerobico": "Turma em aula aeróbica na sala de piso de madeira",
    "af-equipe": "Três homens posam na área de musculação da academia",
    "af-suplementos": "Mesa com suplementos alimentares na academia",
    "af-fachada": "Fachada preta com seta amarela da AF Fitness, no Parque Dois Irmãos",
    "af-academia": "Vista ampla do salão de musculação da AF Fitness, com aparelhos e iluminação em LED",
}


def wa(msg):
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


def thumb(name, eager=False, caption=""):
    load = 'loading="eager"' if eager else 'loading="lazy" decoding="async"'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="thumb"><picture><source srcset="{name}.webp" type="image/webp">'
            f'<img src="{name}.jpg" alt="{ALT[name]}" width="640" height="640" {load}></picture>{cap}</figure>')


def photo(name, eager=False):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<figure class="photo"><picture><source srcset="{name}.webp" type="image/webp">'
            f'<img src="{name}.jpg" alt="{ALT[name]}" width="900" height="600" {load}></picture></figure>')


NAV = [("index.html", "Início"), ("musculacao.html", "Musculação"), ("aulas.html", "Aulas"),
       ("personal-e-nutricao.html", "Personal e nutrição"), ("contato.html", "Contato")]


def nav_items(current, skip_home=False):
    out = []
    for h, l in NAV:
        if skip_home and h == "index.html":
            continue
        cur = ' aria-current="page"' if h == current else ""
        out.append(f'<li><a href="{h}"{cur}>{l}</a></li>')
    return "".join(out)


def url_of(page):
    return f"{DOMINIO}/{'' if page == 'index.html' else page}"


def json_ld(page, title, desc, crumb, faq):
    gym = {
        "@type": "ExerciseGym", "@id": DOMINIO + "/#academia",
        "name": NOME, "alternateName": "AF Fitness",
        "description": "Academia no Parque Dois Irmãos, em Fortaleza, com musculação, aulas de artes marciais, treino funcional, exercícios aeróbicos, personal trainer e nutricionista.",
        "url": DOMINIO + "/", "telephone": FONE_TEL,
        "image": [f"{DOMINIO}/af-capa.jpg", f"{DOMINIO}/af-academia.jpg", f"{DOMINIO}/af-fachada.jpg"],
        "logo": f"{DOMINIO}/logo-af-fitness.svg",
        "address": {"@type": "PostalAddress", "streetAddress": RUA, "addressLocality": "Fortaleza",
                    "addressRegion": "CE", "postalCode": CEP, "addressCountry": "BR"},
        "areaServed": [{"@type": "Place", "name": n + ", Fortaleza"} for n in [BAIRRO_NOME] + VIZINHOS],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.2", "bestRating": "5", "ratingCount": N_AVAL},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Modalidades e serviços", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": f"{DOMINIO}/{h}",
                                               "provider": {"@id": DOMINIO + "/#academia"}, "areaServed": "Fortaleza, CE"}}
            for n, h in SERVICOS]},
        "contactPoint": {"@type": "ContactPoint", "telephone": FONE_TEL, "contactType": "customer service", "availableLanguage": "pt-BR"},
        "hasMap": MAPS_VER,
        # Completar quando confirmado: "openingHoursSpecification", "geo" (latitude/longitude), "priceRange" e "sameAs" (Instagram).
    }
    site = {"@type": "WebSite", "@id": DOMINIO + "/#site", "url": DOMINIO + "/", "name": NOME, "inLanguage": "pt-BR",
            "publisher": {"@id": DOMINIO + "/#academia"}}
    web = {"@type": "WebPage", "@id": url_of(page) + "#pagina", "url": url_of(page), "name": title, "description": desc,
           "inLanguage": "pt-BR", "isPartOf": {"@id": DOMINIO + "/#site"}, "about": {"@id": DOMINIO + "/#academia"},
           "primaryImageOfPage": f"{DOMINIO}/af-capa.jpg", "dateModified": HOJE}
    graph = [gym, site, web]
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url_of(page)}]})
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}} for q, r in faq]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def layout(page, title, desc, body, wa_msg, crumb=None, faq=None, robots="index, follow, max-image-preview:large"):
    w = wa(wa_msg)
    servicos = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in SERVICOS)
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url_of(page)}">
<meta name="theme-color" content="#0d0d0e">
<meta name="geo.region" content="BR-CE">
<meta name="geo.placename" content="Parque Dois Irmãos, Fortaleza">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NOME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url_of(page)}">
<meta property="og:image" content="{DOMINIO}/af-capa.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Salão de musculação da AF Fitness Academia">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">
{json_ld(page, title, desc, crumb, faq)}
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header" data-header>
  <div class="progress" data-progress aria-hidden="true"></div>
  <div class="wrap header-in">
    <a class="brand" href="index.html">{LOGO}<span class="brand-text">Academia</span></a>
    <nav class="nav" aria-label="Principal"><ul>{nav_items(page, skip_home=True)}</ul></nav>
    <a class="btn btn--yellow btn--sm header-cta" href="{w}" target="_blank" rel="noopener">Quero treinar</a>
    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu"><span data-menu-label>Menu</span><i aria-hidden="true"></i></button>
  </div>
</header>

<div class="menu" id="menu">
  <nav aria-label="Menu"><ul class="menu-links">{nav_items(page)}</ul></nav>
  <div class="menu-foot">
    <a class="btn btn--yellow" href="{w}" target="_blank" rel="noopener">{WA_ICON}Chamar no WhatsApp</a>
    <p>{RUA}, {BAIRRO}<br><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></p>
  </div>
</div>

<main id="conteudo">
{body}
</main>

<footer class="site-footer">
  <div class="wrap grid">
    <div class="footer-brand">
      {LOGO}
      <p>Academia no Parque Dois Irmãos, em Fortaleza: musculação, artes marciais, funcional, aeróbico, personal trainer e nutricionista.</p>
    </div>
    <div class="footer-col">
      <h2>Onde estamos</h2>
      <address>{NOME}<br>{RUA}<br>{BAIRRO}<br>CEP {CEP}</address>
      <ul style="margin-top:.5rem">
        <li><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></li>
        <li><a href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota no mapa</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h2>Modalidades</h2>
      <ul>{servicos}</ul>
    </div>
    <div class="footer-col">
      <h2>Páginas</h2>
      <ul>{nav_items(page)}</ul>
    </div>
  </div>
  <div class="wrap"><p class="footer-legal">© 2026 {NOME}. {RUA}, {BAIRRO}.</p></div>
</footer>

<div class="dock" data-dock>
  <a class="btn btn--yellow" href="{w}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>
  <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
</div>

<script src="main.js" defer></script>
</body>
</html>
"""
    head, rest = html.split("</head>", 1)

    def tidy(m):  # sem quebras ruins no endereço; só em texto visível, nunca em atributos
        t = m.group(0)
        return t.replace("R. 15, 190", "R.&nbsp;15,&nbsp;190").replace("Fortaleza - CE", "Fortaleza&nbsp;-&nbsp;CE").replace(CEP, f'<span class="nw">{CEP}</span>')
    return head + "</head>" + re.sub(r">[^<]+<", tidy, rest)


# ───────────────────────── blocos reutilizados ─────────────────────────
def band(titulo, texto, msg):
    return f"""
<section class="band" id="agendar" aria-labelledby="band-t">
  <div class="wrap grid">
    <div class="band-main reveal">
      <h2 id="band-t">{titulo}</h2>
      <p>{texto}</p>
      <div class="actions">
        <a class="btn btn--dark" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Chamar no WhatsApp</a>
        <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar {FONE_EXIBE}</a>
      </div>
    </div>
    <ul class="band-side reveal">
      <li>Musculação, lutas, funcional e aeróbico</li>
      <li>Personal trainer e nutricionista</li>
      <li>{RUA}, Parque Dois Irmãos, Fortaleza</li>
    </ul>
  </div>
</section>"""


def crumbs(label):
    return f'<nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'


def faq_block(items, titulo="Perguntas frequentes"):
    lis = "".join(f'<details><summary>{q}</summary><div class="answer"><p>{r}</p></div></details>' for q, r in items)
    return f"""
<section class="section" aria-labelledby="faq-t">
  <div class="wrap grid">
    <div class="faq-head reveal">
      <span class="eyebrow">Dúvidas</span>
      <h2 id="faq-t">{titulo}</h2>
    </div>
    <div class="faq-list reveal">{lis}</div>
  </div>
</section>"""


def onde(surface=True):
    viz = ", ".join(VIZINHOS[:-1]) + " e " + VIZINHOS[-1]
    return f"""
<section class="section{' section--surface' if surface else ''}" id="como-chegar" aria-labelledby="onde-t">
  <div class="wrap grid">
    <div class="where-body reveal">
      <span class="eyebrow">Como chegar</span>
      <h2 id="onde-t">Na R. 15, no <em>Parque Dois Irmãos</em></h2>
      <p class="muted" style="margin-top:1rem">Procure a fachada preta com a seta amarela. A academia fica perto para quem mora no Parque Dois Irmãos e em bairros próximos de Fortaleza, como {viz}.</p>
      <dl class="info">
        <div><dt>Endereço</dt><dd><address>{RUA}<br>{BAIRRO}, {CEP}</address></dd></div>
        <div><dt>Telefone</dt><dd><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></dd></div>
      </dl>
      <div class="actions">
        <a class="btn btn--yellow" href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota</a>
        <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
      </div>
      <div class="duo" style="margin-top:2rem">{thumb("af-fachada", caption="A fachada, vista da rua.")}{thumb("af-salao", caption="O salão por dentro.")}</div>
    </div>
    <div class="map reveal">
      <a class="map-alt" href="{MAPS_VER}" target="_blank" rel="noopener">Ver a AF Fitness no Google Maps</a>
      <iframe src="{MAPS_EMBED}" title="Mapa com a localização da AF Fitness Academia na R. 15, Parque Dois Irmãos, Fortaleza" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>"""


def block(id_, titulo, resumo, thumbs, oque, quem, como, msg):
    imgs = f'<div class="duo">{"".join(thumb(t) for t in thumbs)}</div>' if thumbs else ""
    return f"""
    <article class="block grid" id="{id_}">
      <header class="block-head reveal">
        <h2>{titulo}</h2>
        <p>{resumo}</p>
        <a class="link" href="{wa(msg)}" target="_blank" rel="noopener">Perguntar no WhatsApp</a>
        {imgs}
      </header>
      <div class="block-body reveal">
        <dl>
          <div><dt>O que é</dt><dd>{oque}</dd></div>
          <div><dt>Para quem</dt><dd>{quem}</dd></div>
          <div><dt>Como funciona</dt><dd>{como}</dd></div>
        </dl>
      </div>
    </article>"""


FAQ_HOME = [
    ("Onde fica a AF Fitness Academia?", f"Na {RUA}, no Parque Dois Irmãos, em Fortaleza - CE, CEP {CEP}. A fachada é preta com uma seta amarela."),
    ("Quais modalidades a academia oferece?", "Musculação, aulas de artes marciais, treino funcional, exercícios aeróbicos e aulas para jovens. Também há personal trainer, aulas particulares e nutricionista."),
    ("A AF Fitness tem personal trainer?", "Sim. Você pode treinar com acompanhamento de personal trainer ou fazer aulas particulares. Combine pelo WhatsApp."),
    ("A academia tem nutricionista?", "Sim. A AF Fitness oferece consultoria em nutrição com nutricionista, para alinhar a alimentação ao seu treino."),
    ("Tem aula para jovens?", "Sim, a academia tem aulas voltadas para jovens. Pergunte pelo WhatsApp sobre idades e horários das turmas."),
    ("Quanto custa a mensalidade?", f"Os planos e valores são informados pelo WhatsApp ou por telefone, no {FONE_EXIBE}."),
    ("Qual o horário de funcionamento?", "Confirme o horário do dia pelo WhatsApp ou no perfil da AF Fitness no Google."),
]


# ───────────────────────────── INÍCIO ─────────────────────────────
def page_index():
    msg = "Olá! Vi o site da AF Fitness e quero saber sobre planos e horários."
    mods = [  # nome, descrição, link, foto
        ("Artes marciais", "Aulas no tatame, com treino em pé e de kimono.", "aulas.html#artes-marciais", "af-lutas"),
        ("Treino funcional", "Corpo inteiro em movimento, em circuito.", "aulas.html#funcional", "af-funcional"),
        ("Exercícios aeróbicos", "Aulas em grupo para fôlego e gasto calórico.", "aulas.html#aerobico", "af-aerobico"),
        ("Aulas para jovens", "Turmas para quem está começando cedo.", "aulas.html#jovens", "af-turma"),
        ("Personal trainer", "Treino montado e acompanhado de perto.", "personal-e-nutricao.html#personal", "af-pesos"),
        ("Aulas particulares", "Uma sessão individual, no seu ritmo.", "personal-e-nutricao.html#aulas-particulares", "af-kimono"),
        ("Nutricionista", "Alimentação alinhada ao seu treino.", "personal-e-nutricao.html#nutricao", "af-suplementos"),
    ]

    def mcard(n, nome, desc, href, foto, grande=False):
        w, h = (900, 600) if grande else (320, 320)
        return (f'<a class="mcard{" mcard--big" if grande else ""} reveal" href="{href}">'
                f'<picture><source srcset="{foto}.webp" type="image/webp"><img src="{foto}.jpg" alt="{ALT[foto]}" width="{w}" height="{h}" loading="lazy" decoding="async"></picture>'
                f'<span class="mcard-n" aria-hidden="true">{n:02d}</span>'
                f'<span class="mcard-body"><h3>{nome}</h3><span class="mcard-d">{desc}</span><span class="mcard-go">Saiba mais</span></span></a>')

    mods_html = mcard(1, "Musculação", "Salão com aparelhos, bancos e pesos livres, para todos os níveis. É o coração da academia.", "musculacao.html", "af-academia", grande=True)
    mods_html += "".join(mcard(i, n, d, h, t) for i, (n, d, h, t) in enumerate(mods, start=2))
    mods_html += (f'<a class="mcard mcard--cta reveal" href="{wa("Olá! Vi o site da AF Fitness e quero ajuda para escolher uma modalidade.")}" target="_blank" rel="noopener">'
                  f'<span class="mcard-body"><h3>Não sabe por onde começar?</h3><span class="mcard-d">Conte o seu objetivo e a gente indica a modalidade.</span><span class="mcard-go">Chamar no WhatsApp</span></span></a>')
    faixa = "".join(f"<span>{n}</span>" for n, _ in SERVICOS[:7]) * 2
    gal = "".join(f'<div class="reveal">{thumb(t)}</div>' for t in ["af-salao", "af-aparelhos", "af-lutas", "af-kimono", "af-aerobico", "af-equipe"])
    body = f"""
<section class="hero" aria-labelledby="hero-t">
  <svg class="hero-arrow" viewBox="0 0 98 60" aria-hidden="true" focusable="false"><path d="M1 1h62.6L96.5 30 63.6 59H1z" pathLength="1"/></svg>
  <div class="wrap">
    <span class="eyebrow">Academia · Parque Dois Irmãos · Fortaleza</span>
    <h1 id="hero-t"><span class="ln"><span>Academia no</span></span> <span class="ln"><span>Parque Dois Irmãos:</span></span> <span class="ln"><span><em>musculação, lutas</em></span></span> <span class="ln"><span><em>e funcional</em></span></span></h1>
    <p class="lead">Tudo num só lugar: treine musculação, faça aulas de artes marciais, funcional e aeróbico e conte com personal trainer e nutricionista. Em Fortaleza, na {RUA}.</p>
    <div class="actions">
      <a class="btn btn--yellow" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Quero treinar na AF</a>
      <a class="btn btn--ghost" href="#modalidades">Ver modalidades</a>
    </div>
    <dl class="facts">
      <div><dt>No Google</dt><dd>{NOTA} de 5 · {N_AVAL} avaliações</dd></div>
      <div><dt>Endereço</dt><dd><a href="#como-chegar">{RUA}, Parque Dois Irmãos</a></dd></div>
      <div><dt>Telefone</dt><dd><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></dd></div>
    </dl>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{faixa}</div></div>

<section class="section" id="modalidades" aria-labelledby="mod-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">Modalidades</span>
        <h2 id="mod-t">Modalidades da <em>AF Fitness</em></h2>
      </div>
      <p class="head-b lead">Oito formas de treinar no mesmo endereço. Dá para combinar musculação com aulas e acompanhamento.</p>
    </div>
    <div class="mods">{mods_html}</div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="est-t">
  <div class="wrap grid split">
    <div class="split-media reveal">{photo("af-academia")}</div>
    <div class="split-body reveal">
      <span class="eyebrow">Estrutura</span>
      <h2 id="est-t">Espaço para treinar <em>de verdade</em></h2>
      <ul class="checks">
        <li>Salão de musculação com aparelhos, bancos e pesos livres</li>
        <li>Tatame para as aulas de artes marciais</li>
        <li>Sala com piso de madeira para aulas em grupo</li>
        <li>Fachada preta e amarela, fácil de achar na R. 15</li>
      </ul>
      <a class="link" href="musculacao.html">Ver a musculação</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="gal-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">Por dentro</span>
        <h2 id="gal-t">A academia em <em>fotos</em></h2>
      </div>
    </div>
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="pas-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">Como começar</span>
        <h2 id="pas-t">Três passos até o <em>primeiro treino</em></h2>
      </div>
    </div>
    <ol class="steps">
      <li class="step reveal"><h3>Chame no WhatsApp</h3><p>Pergunte sobre planos, horários e modalidades. É rápido e sem compromisso.</p></li>
      <li class="step reveal"><h3>Venha conhecer</h3><p>Passe na {RUA}, veja o salão, o tatame e a sala de aulas.</p></li>
      <li class="step reveal"><h3>Comece a treinar</h3><p>Escolha entre musculação, aulas ou os dois, e ajuste o treino ao seu objetivo.</p></li>
    </ol>
    <div class="actions reveal"><a class="btn btn--yellow" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Dar o primeiro passo</a></div>
  </div>
</section>

{onde(surface=False)}

{faq_block(FAQ_HOME).replace('<section class="section"', '<section class="section section--surface"', 1)}

{band("Bora treinar?", "Chame no WhatsApp, tire suas dúvidas sobre planos e horários e venha conhecer a academia.", msg)}
"""
    return layout("index.html",
                  "Academia no Parque Dois Irmãos, Fortaleza | AF Fitness",
                  "Academia no Parque Dois Irmãos, Fortaleza: musculação, artes marciais, treino funcional, aeróbico, personal trainer e nutricionista. Chame no WhatsApp.",
                  body, msg, faq=FAQ_HOME)


# ─────────────────────────── MUSCULAÇÃO ───────────────────────────
def page_musculacao():
    msg = "Olá! Vi o site da AF Fitness e quero saber sobre a musculação."
    faq = [
        ("Nunca treinei. Posso começar na musculação?", "Pode. O treino começa com cargas leves e exercícios simples, e avança conforme você ganha força e técnica."),
        ("A academia tem pesos livres?", "Sim. Além dos aparelhos, o salão tem bancos, halteres e barras."),
        ("Posso treinar com personal trainer?", 'Sim. A AF Fitness tem <a href="personal-e-nutricao.html#personal">personal trainer e aulas particulares</a>.'),
        ("Posso combinar musculação com aulas?", 'Sim. Muita gente junta a musculação com <a href="aulas.html">artes marciais, funcional ou aeróbico</a>.'),
    ]
    gal = "".join(f'<div class="reveal">{thumb(t)}</div>' for t in ["af-musculacao", "af-salao", "af-pesos", "af-aparelhos", "af-funcional", "af-equipe"])
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Musculação")}
    <div class="grid">
      <div class="page-hero-text">
        <h1>Musculação no <em>Parque Dois Irmãos</em>, em Fortaleza</h1>
        <p class="lead">Um salão com aparelhos, bancos e pesos livres para ganhar força, definir ou simplesmente sair do sedentarismo.</p>
        <div class="actions"><a class="btn btn--yellow" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Quero treinar musculação</a></div>
      </div>
      <div class="page-hero-media">{photo("af-academia", eager=True)}</div>
    </div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="mus-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="eyebrow">O treino</span><h2 id="mus-t">Como é treinar <em>musculação</em> aqui</h2></div></div>
    <div class="rows">
      <div class="row grid reveal"><h3>Para todos os níveis</h3><p>Do primeiro treino ao avançado. A carga e os exercícios acompanham o seu momento.</p></div>
      <div class="row grid reveal"><h3>Aparelhos e pesos livres</h3><p>Máquinas para cada grupo muscular, além de bancos, halteres e barras para os exercícios livres.</p></div>
      <div class="row grid reveal"><h3>Treino com objetivo</h3><p>Hipertrofia, emagrecimento, condicionamento ou saúde. Diga o que você busca e o treino é montado em cima disso.</p></div>
      <div class="row grid reveal"><h3>Com ou sem personal</h3><p>Treine por conta própria ou com <a href="personal-e-nutricao.html#personal">personal trainer</a>, e alinhe a alimentação com a <a href="personal-e-nutricao.html#nutricao">nutricionista</a>.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="sal-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="eyebrow">O salão</span><h2 id="sal-t">A área de <em>musculação</em></h2></div></div>
    <div class="gallery">{gal}</div>
  </div>
</section>

{faq_block(faq, "Dúvidas sobre musculação").replace('<section class="section"', '<section class="section section--surface"', 1)}

{band("Seu treino começa aqui", "Chame no WhatsApp, conte o seu objetivo e venha conhecer o salão.", msg)}
"""
    return layout("musculacao.html",
                  "Musculação no Parque Dois Irmãos, Fortaleza | AF Fitness",
                  "Academia de musculação no Parque Dois Irmãos, Fortaleza: aparelhos, pesos livres e treino para todos os níveis, com opção de personal. Chame no WhatsApp.",
                  body, msg, crumb="Musculação", faq=faq)


# ───────────────────────────── AULAS ─────────────────────────────
def page_aulas():
    msg = "Olá! Vi o site da AF Fitness e quero saber sobre as aulas."
    m = lambda s: f"Olá! Vi o site da AF Fitness e quero saber sobre {s}."
    faq = [
        ("Preciso ter experiência para fazer as aulas?", "Não. As turmas recebem iniciantes, e a intensidade é ajustada ao seu ritmo."),
        ("Quais são os horários das aulas?", f"Os horários de cada turma são informados pelo WhatsApp, no {FONE_EXIBE}."),
        ("O que levar para a aula de artes marciais?", "Roupa confortável e água. Pergunte pelo WhatsApp se a turma usa kimono ou equipamento de proteção."),
        ("Posso fazer aulas e musculação?", 'Sim. Dá para combinar as aulas com a <a href="musculacao.html">musculação</a> na mesma academia.'),
    ]
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Aulas")}
    <div class="grid">
      <div class="page-hero-text">
        <h1>Artes marciais, funcional e aeróbico em <em>Fortaleza</em></h1>
        <p class="lead">Aulas em grupo na AF Fitness, no Parque Dois Irmãos: lutas no tatame, treino funcional, exercícios aeróbicos e turmas para jovens.</p>
        <div class="actions"><a class="btn btn--yellow" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Quero fazer uma aula</a></div>
      </div>
      <div class="page-hero-media"><div class="duo" style="max-width:none">{thumb("af-lutas", eager=True)}{thumb("af-aerobico", eager=True)}</div></div>
    </div>
  </div>
</section>

<section class="section--surface" aria-label="Aulas da academia">
  <div class="wrap">
    {block("artes-marciais", "Aulas de <em>artes marciais</em>", "Treino de luta no tatame, em turma.", ["af-kimono", "af-turma"],
           "Aulas de luta com aquecimento, técnica e condicionamento. As fotos mostram turmas treinando em pé e de kimono.",
           "Para quem quer aprender a lutar, ganhar condicionamento, disciplina e confiança. Iniciantes são bem-vindos.",
           "A aula acontece no tatame, em frente ao espelho, com exercícios em dupla e em grupo.", m("as aulas de artes marciais"))}
    {block("funcional", "Treino <em>funcional</em>", "Corpo inteiro em movimento.", ["af-funcional", "af-pesos"],
           "Exercícios que combinam força, equilíbrio e resistência, usando o peso do corpo e acessórios.",
           "Para quem quer condicionamento geral, emagrecer ou variar o treino da musculação.",
           "Circuitos com estações de exercícios, em ritmo ajustado ao seu nível.", m("o treino funcional"))}
    {block("aerobico", "Exercícios <em>aeróbicos</em>", "Aula em grupo, com ritmo e energia.", ["af-aerobico", "af-salao"],
           "Aulas que elevam a frequência cardíaca e trabalham o fôlego.",
           "Para quem quer gastar calorias, melhorar o condicionamento e treinar acompanhado.",
           "A turma treina junta na sala de piso de madeira, seguindo os movimentos do professor.", m("as aulas de aeróbico"))}
    {block("jovens", "Aulas para <em>jovens</em>", "Para começar cedo, do jeito certo.", ["af-turma", "af-lutas"],
           "Turmas voltadas para jovens, com atividades adequadas à idade.",
           "Para adolescentes e jovens que querem praticar atividade física com orientação.",
           "Pergunte pelo WhatsApp sobre idades, modalidades e horários das turmas.", m("as aulas para jovens"))}
  </div>
</section>

{faq_block(faq, "Dúvidas sobre as aulas")}

{band("Escolha a sua aula", "Chame no WhatsApp, pergunte os horários das turmas e venha treinar.", msg)}
"""
    return layout("aulas.html",
                  "Artes marciais, funcional e aeróbico | AF Fitness Fortaleza",
                  "Aulas de artes marciais, treino funcional, aeróbico e turmas para jovens na AF Fitness, academia no Parque Dois Irmãos, Fortaleza. Chame no WhatsApp.",
                  body, msg, crumb="Aulas", faq=faq)


# ────────────────────── PERSONAL E NUTRIÇÃO ──────────────────────
def page_personal():
    msg = "Olá! Vi o site da AF Fitness e quero saber sobre personal trainer e nutricionista."
    m = lambda s: f"Olá! Vi o site da AF Fitness e quero saber sobre {s}."
    faq = [
        ("Como contratar um personal trainer na AF Fitness?", f"Chame no WhatsApp, no {FONE_EXIBE}, e diga o seu objetivo e os horários em que pode treinar."),
        ("Qual a diferença entre personal trainer e aula particular?", "O personal acompanha o seu treino de forma contínua. A aula particular é uma sessão individual, que pode ser de uma modalidade específica."),
        ("O que faz a nutricionista da academia?", "Avalia a sua rotina e orienta a alimentação de acordo com o seu treino e o seu objetivo."),
    ]
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Personal e nutrição")}
    <div class="grid">
      <div class="page-hero-text">
        <h1>Personal trainer e nutricionista em <em>Fortaleza</em></h1>
        <p class="lead">Acompanhamento individual na AF Fitness, no Parque Dois Irmãos: treino de perto, aulas particulares e orientação de alimentação.</p>
        <div class="actions"><a class="btn btn--yellow" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Quero acompanhamento</a></div>
      </div>
      <div class="page-hero-media"><div class="duo" style="max-width:none">{thumb("af-pesos", eager=True)}{thumb("af-aparelhos", eager=True)}</div></div>
    </div>
  </div>
</section>

<section class="section--surface" aria-label="Acompanhamento individual">
  <div class="wrap">
    {block("personal", "<em>Personal</em> trainer", "Treino montado e acompanhado para você.", [],
           "Um profissional acompanha o seu treino, corrige a execução e ajusta a carga a cada sessão.",
           "Para quem quer resultado com segurança, está começando ou voltando a treinar, ou precisa de mais motivação.",
           "Você combina objetivo e horários, e o treino é planejado e acompanhado de perto.", m("personal trainer"))}
    {block("aulas-particulares", "Aulas <em>particulares</em>", "Uma sessão só sua.", [],
           "Aulas individuais, com atenção exclusiva do professor.",
           "Para quem prefere aprender no próprio ritmo ou quer evoluir mais rápido em uma modalidade.",
           "A aula é marcada em horário combinado. Pergunte pelo WhatsApp quais modalidades têm aula particular.", m("aulas particulares"))}
    {block("nutricao", "<em>Nutricionista</em> e consultoria em nutrição", "Alimentação alinhada ao treino.", ["af-suplementos", "af-musculacao"],
           "Consultoria com nutricionista para organizar a alimentação de acordo com o seu objetivo.",
           "Para quem quer emagrecer, ganhar massa muscular ou ter mais disposição para treinar.",
           "A nutricionista avalia a sua rotina e orienta o que ajustar. Agende pelo WhatsApp.", m("a consultoria em nutrição"))}
  </div>
</section>

{faq_block(faq, "Dúvidas sobre acompanhamento")}

{band("Treine com acompanhamento", "Chame no WhatsApp e conte o seu objetivo. A gente indica o melhor caminho.", msg)}
"""
    return layout("personal-e-nutricao.html",
                  "Personal trainer e nutricionista em Fortaleza | AF Fitness",
                  "Personal trainer, aulas particulares e nutricionista na AF Fitness, academia no Parque Dois Irmãos, Fortaleza. Treino e alimentação alinhados ao seu objetivo.",
                  body, msg, crumb="Personal e nutrição", faq=faq)


# ───────────────────────────── CONTATO ─────────────────────────────
def page_contato():
    msg = "Olá! Vi o site da AF Fitness e quero saber sobre planos e horários."
    body = f"""
<section class="page-hero" style="padding-bottom:clamp(2rem,4vw,3rem)">
  <div class="wrap">
    {crumbs("Contato")}
    <h1>Fale com a <em>AF Fitness</em></h1>
    <p class="lead">Planos, horários e modalidades: pergunte pelo WhatsApp, ligue ou venha conhecer a academia no Parque Dois Irmãos.</p>
  </div>
</section>

<section aria-label="Canais de contato" style="padding-bottom:var(--section)">
  <div class="wrap">
    <ul class="channels reveal">
      <li class="channel"><a href="{wa(msg)}" target="_blank" rel="noopener"><span class="k">WhatsApp</span><span class="big">Chamar agora</span><span class="note">{FONE_EXIBE}</span></a></li>
      <li class="channel"><a href="tel:{FONE_TEL}"><span class="k">Telefone</span><span class="big">{FONE_EXIBE}</span><span class="note">Toque para ligar</span></a></li>
      <li class="channel"><a href="{MAPS_ROTA}" target="_blank" rel="noopener"><span class="k">Endereço</span><span class="big">{RUA}, Parque Dois Irmãos</span><span class="note">Fortaleza - CE, {CEP}</span></a></li>
    </ul>
  </div>
</section>

{onde()}

{band("Venha conhecer a academia", "Chame no WhatsApp para tirar as dúvidas ou passe na R. 15, 190.", msg)}
"""
    return layout("contato.html",
                  "Endereço e WhatsApp da AF Fitness | Parque Dois Irmãos",
                  "AF Fitness Academia: R. 15, 190, Parque Dois Irmãos, Fortaleza - CE. WhatsApp e telefone (85) 98187-6641. Veja o mapa e como chegar.",
                  body, msg, crumb="Contato")


def page_404():
    body = f"""
<section class="page-hero" style="min-height:60vh">
  <div class="wrap">
    <span class="eyebrow">Erro 404</span>
    <h1>Página não <em>encontrada</em></h1>
    <p class="lead">O endereço pode ter mudado. Volte para o início ou fale com a academia.</p>
    <div class="actions"><a class="btn btn--yellow" href="index.html">Ir para o início</a><a class="btn btn--ghost" href="contato.html">Contato</a></div>
  </div>
</section>"""
    return layout("404.html", "Página não encontrada | AF Fitness", "Página não encontrada no site da AF Fitness Academia.", body,
                  "Olá! Vi o site da AF Fitness.", robots="noindex, follow")


PAGES = {"index.html": page_index, "musculacao.html": page_musculacao, "aulas.html": page_aulas,
         "personal-e-nutricao.html": page_personal, "contato.html": page_contato}
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#0d0d0e"/>'
           '<path d="M8 14h28l20 18-20 18H8z" fill="#f7b90b"/>'
           '<text x="12" y="40" font-family="Arial Narrow, Arial, sans-serif" font-weight="900" font-size="23" fill="#121212">AF</text></svg>')
LOGO_FILE = LOGO.replace('class="brand-logo" ', 'xmlns="http://www.w3.org/2000/svg" ')
MANIFEST = {"name": NOME, "short_name": "AF Fitness", "start_url": "./index.html", "display": "browser",
            "background_color": "#0d0d0e", "theme_color": "#0d0d0e", "lang": "pt-BR",
            "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    (OUT / "404.html").write_text(page_404(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (OUT / "logo-af-fitness.svg").write_text(LOGO_FILE, encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1), encoding="utf-8")
    urls = "".join(f"  <url><loc>{url_of(n)}</loc><lastmod>{HOJE}</lastmod></url>\n" for n in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    print("ok:", ", ".join(PAGES))
