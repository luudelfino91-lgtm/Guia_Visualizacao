# Gera imagens dos gráficos com o nome escrito (PT e EN) para a galeria do Power BI.
import sys,base64,csv,os
from playwright.sync_api import sync_playwright
FD=sys.argv[1]; RAIZ=sys.argv[2]
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
f1=b64(f'{FD}/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2')
rows=list(csv.DictReader(open(f'{RAIZ}/dados/dim_grafico.csv',encoding='utf-8')))
css=f'@font-face{{font-family:B;font-weight:800;src:url(data:font/woff2;base64,{f1})}}body{{margin:0}}.c{{width:800px;height:580px;background:#FBF9FD;position:relative;overflow:hidden}}img{{display:block;width:800px;height:500px}}.n{{position:absolute;left:0;right:0;bottom:0;height:80px;background:#7139B8;color:#fff;font:800 38px B,"Segoe UI",sans-serif;display:flex;align-items:center;padding:0 28px;white-space:nowrap}}'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':800,'height':580})
    for r in rows:
        im='data:image/png;base64,'+b64(f"{RAIZ}/imagens/graficos/{r['slug']}.png")
        for L in('pt','en'):
            nome=r['nome_'+L].replace('&','&amp;')
            pg.set_content(f'<style>{css}</style><div class="c"><img src="{im}"><div class="n">{nome}</div></div>')
            pg.screenshot(path=f"{RAIZ}/imagens/rotulados/{r['slug']}_{L}.png",clip={'x':0,'y':0,'width':800,'height':580})
    b.close()
