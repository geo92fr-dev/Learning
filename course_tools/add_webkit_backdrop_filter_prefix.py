import os

ROOT='.'
updated=[]
marker='backdrop-filter:blur('
for base,_,files in os.walk(ROOT):
    for f in files:
        if not f.lower().endswith('.html'): continue
        p=os.path.join(base,f)
        try:
            txt=open(p,'r',encoding='utf-8').read()
            if marker not in txt: continue
            # naive pass: for each occurrence ensure -webkit-backdrop-filter just before
            parts=txt.split(marker)
            rebuilt=parts[0]
            changed=False
            for tail in parts[1:]:
                # look back in last 120 chars of current rebuilt buffer for existing webkit
                prev=rebuilt[-120:]
                if '-webkit-backdrop-filter' not in prev:
                    # inject
                    rebuilt += f"-webkit-{marker}" + tail
                    changed=True
                else:
                    rebuilt += marker + tail
            if changed:
                with open(p,'w',encoding='utf-8') as out:
                    out.write(rebuilt)
                updated.append(p)
        except Exception as e:
            print('Erreur fichier',p,e)

print('Fichiers mis à jour:',len(updated))
for fp in updated:
    print(' -',fp)
