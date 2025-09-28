import pathlib, re, datetime, argparse, html

INDEX_FILENAME = 'College_4ieme_Maths.html'
TITLE = 'Collège 4ème - Maths (Cours accessibles)'
INTRO = 'Sélectionne un cours. Les plus récents apparaissent en premier. Ajoute la page à ton écran d\'accueil pour un accès rapide.'

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL)

CSS = """
:root { --bg:#ffffff; --fg:#222; --accent:#2563eb; --soft:#eff6ff; }
body { font-family: system-ui,-apple-system,"Segoe UI",Roboto; margin:0; background:var(--bg); color:var(--fg); line-height:1.45; }
header { background:var(--accent); color:#fff; padding:.9rem 1.1rem; }
header h1 { margin:0; font-size:1.1rem; }
main { padding:1rem; max-width:900px; margin:0 auto; }
.grid { display:grid; gap:.85rem; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); }
.card { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:.75rem .8rem .85rem; position:relative; box-shadow:0 2px 4px rgba(0,0,0,.05); display:flex; flex-direction:column; }
.card h2 { font-size:.9rem; margin:0 0 .4rem; line-height:1.25; }
.card a { color:var(--accent); text-decoration:none; font-weight:600; }
.meta { font-size:.65rem; text-transform:uppercase; letter-spacing:.05em; color:#555; margin-bottom:.4rem; }
footer { text-align:center; font-size:.65rem; padding:1.2rem .5rem 2rem; color:#555; }
.filter { margin:0 0 1rem; display:flex; gap:.5rem; flex-wrap:wrap; }
.filter input { padding:.5rem .6rem; font-size:.8rem; border:1px solid #cbd5e1; border-radius:6px; }
.tag { display:inline-block; background:var(--soft); color:var(--accent); padding:.15rem .45rem; font-size:.55rem; font-weight:600; border-radius:999px; letter-spacing:.05em; }
.empty { font-size:.85rem; opacity:.7; }
.dark { --bg:#1f2937; --fg:#f1f5f9; --accent:#60a5fa; --soft:#1e3a56; }
.dark body { background:var(--bg); color:var(--fg); }
.dark .card { background:#223042; border-color:#334155; }
.toggle { cursor:pointer; background:#fff; color:#111; border:none; border-radius:6px; padding:.4rem .7rem; font-size:.65rem; font-weight:600; }
.dark .toggle { background:#334155; color:#f1f5f9; }
.toolbar { margin-top:.6rem; display:flex; gap:.5rem; flex-wrap:wrap; }
.note { font-size:.7rem; margin-top:.4rem; opacity:.75; }
@media (max-width:640px){ .grid { grid-template-columns:1fr 1fr; } }
@media (max-width:460px){ .grid { grid-template-columns:1fr; } }
"""

JS = """
const q = document.getElementById('query');
const cards = [...document.querySelectorAll('.card')];
q.addEventListener('input', ()=>{
  const val = q.value.toLowerCase().trim();
  let shown = 0;
  cards.forEach(c=>{
    const t = c.dataset.title;
    if(!val || t.includes(val)) { c.style.display='flex'; shown++; } else c.style.display='none';
  });
  document.getElementById('count').textContent = shown + ' / ' + cards.length;
});
const modeBtn = document.getElementById('mode');
modeBtn.addEventListener('click', ()=>{ document.documentElement.classList.toggle('dark'); });
"""

def extract_title(html_text: str):
    m = TITLE_RE.search(html_text)
    if m:
        t = html.unescape(m.group(1).strip())
        return t
    m2 = H1_RE.search(html_text)
    if m2:
        return html.unescape(re.sub('<.*?>','',m2.group(1)).strip())
    return 'Cours'

def classify(title: str):
    t = title.lower()
    if 'fraction' in t: return 'Fractions'
    if 'pythagore' in t: return 'Pythagore'
    if 'equation' in t: return 'Équations'
    if 'proportion' in t: return 'Proportionnalité'
    return 'Autres'

def build_card(filename: str, title: str, mtime: float):
    dt = datetime.datetime.fromtimestamp(mtime)
    date_str = dt.strftime('%d/%m/%Y %H:%M')
    cat = classify(title)
    safe_title = html.escape(title)
    rel = pathlib.Path(filename).name
    return f"<div class='card' data-title='{html.escape(title.lower())}'><div class='meta'>{date_str}</div><h2><a href='{rel}'>{safe_title}</a></h2><div class='tag'>{cat}</div></div>"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='Répertoire des cours')
    ap.add_argument('--output', default=INDEX_FILENAME)
    args = ap.parse_args()

    base = pathlib.Path(args.dir)
    files = sorted(base.glob('cours_*.html'))
    cards = []
    for f in files:
        if f.name == args.output:
            continue
        text = f.read_text(encoding='utf-8', errors='ignore')
        title = extract_title(text)
        cards.append((f, title, f.stat().st_mtime))

    # tri inverse par date
    cards.sort(key=lambda x: x[2], reverse=True)

    cards_html = '\n'.join(build_card(f.name, t, mt) for f,t,mt in cards) if cards else "<p class='empty'>Aucun cours généré pour l'instant.</p>"

    html_page = f"""<!DOCTYPE html>
<html lang='fr'>
<head>
<meta charset='utf-8'/>
<meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>{TITLE}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>{TITLE}</h1>
  <div class='toolbar'>
    <button id='mode' class='toggle'>Mode sombre</button>
  </div>
  <div class='note'>{html.escape(INTRO)}</div>
</header>
<main>
  <div class='filter'>
    <input id='query' type='text' placeholder='Rechercher un cours...' aria-label='Rechercher'/>
    <div id='count' style='font-size:.7rem;align-self:center;opacity:.7'></div>
  </div>
  <div class='grid'>
    {cards_html}
  </div>
</main>
<footer>Index généré automatiquement - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</footer>
<script>{JS}</script>
</body>
</html>"""

    out_path = base / args.output
    out_path.write_text(html_page, encoding='utf-8')
    print(f"Index généré : {out_path}")

if __name__ == '__main__':
    main()
