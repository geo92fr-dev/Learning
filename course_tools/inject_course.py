import json, argparse, pathlib, re, sys, datetime

PLACEHOLDER_RE = re.compile(r"\[(\w+)\]")

def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Erreur lecture JSON {path}: {e}")
        sys.exit(1)

def build_map(data: dict):
    mapping = {}
    # aplatissement simple clés de 1er niveau + sous-dicts (clé_subclé)
    def walk(prefix, obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                walk(f"{prefix}_{k}" if prefix else k, v)
        elif isinstance(obj, list):
            mapping[prefix] = '\n'.join(str(x) for x in obj)
        else:
            mapping[prefix] = str(obj)
    walk('', data)
    # Ajouts utiles
    if 'DATE_MAJ' not in mapping:
        mapping['DATE_MAJ'] = datetime.date.today().strftime('%d/%m/%Y')
    return mapping

def inject(template: str, mapping: dict, strict: bool):
    def repl(m):
        key = m.group(1)
        return mapping.get(key, f"[{key}]" if not strict else f"<<MANQUE:{key}>>")
    return PLACEHOLDER_RE.sub(repl, template)

def main():
    ap = argparse.ArgumentParser(description='Injecte des valeurs JSON dans le template HTML de cours.')
    ap.add_argument('-t','--template', required=True, help='Fichier template HTML')
    ap.add_argument('-j','--json', required=True, help='Fichier JSON source')
    ap.add_argument('-o','--output', required=True, help='Fichier HTML de sortie')
    ap.add_argument('--strict', action='store_true', help='Marquer explicitement les placeholders manquants')
    args = ap.parse_args()

    tpl_path = pathlib.Path(args.template)
    js_path = pathlib.Path(args.json)

    if not tpl_path.exists() or not js_path.exists():
        print('Template ou JSON introuvable.')
        sys.exit(1)

    template = tpl_path.read_text(encoding='utf-8')
    data = load_json(js_path)
    mapping = build_map(data)
    result = inject(template, mapping, args.strict)

    out_path = pathlib.Path(args.output)
    out_path.write_text(result, encoding='utf-8')
    print(f"Fichier généré: {out_path}")

if __name__ == '__main__':
    main()
