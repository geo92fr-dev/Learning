import argparse
import pathlib
import re
import json
from datetime import datetime

# Simple Markdown-ish to HTML converter (limited)
MD_HEADERS = [('# ', 'h1'), ('## ', 'h2'), ('### ', 'h3'), ('#### ', 'h4')]

def md_to_blocks(md: str):
    lines = md.splitlines()
    html_parts = []
    buffer = []
    def flush_paragraph():
        nonlocal buffer
        if buffer:
            paragraph = ' '.join(buffer).strip()
            if paragraph:
                html_parts.append(f'<p>{paragraph}</p>')
            buffer = []
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_paragraph()
            continue
        handled = False
        for prefix, tag in MD_HEADERS:
            if line.startswith(prefix):
                flush_paragraph()
                content = line[len(prefix):].strip()
                html_parts.append(f'<{tag}>{content}</{tag}>')
                handled = True
                break
        if handled:
            continue
        # list item
        if line.startswith(('- ', '* ')):
            flush_paragraph()
            item = line[2:].strip()
            if not (html_parts and html_parts[-1].startswith('<ul')):
                html_parts.append('<ul>')
            html_parts.append(f'<li>{item}</li>')
            continue
        else:
            if html_parts and html_parts[-1] == '</ul>':
                pass
        buffer.append(line)
    flush_paragraph()
    # close list if needed (simple heuristic)
    fixed = []
    open_ul = False
    for part in html_parts:
        if part == '<ul>':
            if open_ul:
                fixed.append('</ul>')
            open_ul = True
            fixed.append(part)
        elif part.startswith('<li'):
            fixed.append(part)
        else:
            if open_ul:
                fixed.append('</ul>')
                open_ul = False
            fixed.append(part)
    if open_ul:
        fixed.append('</ul>')
    return '\n'.join(fixed)

BALISES = [
    'ROLE','CONTEXTE_ELEVE','OBJECTIFS','INTRO','DECOUVERTE','METHODE',
    'PRATIQUE','RESUME','AUTO_EVAL','CORRECTIONS','SOUTIEN_MOTIVATION',
    'ADAPTATIONS_DYS','SUIVI','VERSION_SYNTHETIQUE'
]

BALISE_RE = re.compile(r'<(' + '|'.join(BALISES) + r')>([\s\S]*?)</\1>', re.MULTILINE)

BLOCK_WRAPPER = '<div class="block" data-type="{name}">{inner}</div>'

def extract_balises(md: str):
    found = {}
    for m in BALISE_RE.finditer(md):
        name = m.group(1)
        content = m.group(2).strip()
        found[name] = content
    return found

def enhance_block(name: str, raw_md: str):
    # Basic conversion + tag label
    html = md_to_blocks(raw_md)
    label = f'<div class="tag">{name}</div>'
    return BLOCK_WRAPPER.format(name=name.lower(), inner=label + html)

HTML_TOKEN = '<!--PY_CONTENT-->'

def build_page(template_html: str, balise_map: dict):
    ordered = ['ROLE','CONTEXTE_ELEVE','OBJECTIFS','INTRO','DECOUVERTE','METHODE','PRATIQUE','RESUME','CORRECTIONS','SUIVI','VERSION_SYNTHETIQUE']
    blocks = []
    for name in ordered:
        if name in balise_map:
            blocks.append(enhance_block(name, balise_map[name]))
    assembled = '\n'.join(blocks)
    return template_html.replace('</main>', assembled + '\n</main>')


def main():
    ap = argparse.ArgumentParser(description='Génère une page HTML accessible à partir d\'un cours balisé.')
    ap.add_argument('source', help='Fichier source Markdown contenant les balises')
    ap.add_argument('-o','--output', help='Fichier de sortie HTML', default='cours_genere.html')
    ap.add_argument('-t','--template', help='Template HTML', default='template_base.html')
    args = ap.parse_args()

    src_path = pathlib.Path(args.source)
    if not src_path.exists():
        raise SystemExit(f"Source introuvable: {src_path}")

    tpl_path = pathlib.Path(args.template)
    if not tpl_path.exists():
        raise SystemExit(f"Template introuvable: {tpl_path}")

    md_content = src_path.read_text(encoding='utf-8')
    tpl_html = tpl_path.read_text(encoding='utf-8')

    balises = extract_balises(md_content)
    if not balises:
        print('Aucune balise détectée. Assurez-vous d\'utiliser <BALISE>...</BALISE>.')

    page = build_page(tpl_html, balises)

    # Ajouter un titre si présent
    title = balises.get('VERSION_SYNTHETIQUE','Cours').splitlines()[0][:60]
    page = page.replace('<title>Cours</title>', f'<title>{title}</title>')
    page = page.replace('<h1 id="courseTitle">Cours</h1>', f'<h1 id="courseTitle">{title}</h1>')

    out_path = pathlib.Path(args.output)
    out_path.write_text(page, encoding='utf-8')
    print(f"Page générée : {out_path} ({out_path.resolve()})")

if __name__ == '__main__':
    main()
