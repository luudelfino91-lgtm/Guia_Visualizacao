import sys, subprocess, os
sys.path.insert(0,'.')
import content as CT, charts as G
from svgdsl import svg,PG,L,C,CO,WH
os.makedirs('svg',exist_ok=True)
err=[]
for s in CT.CH:
    try:
        els=getattr(G,'g_'+s)()
        if CT.CH[s][-1]=='cuidado':
            els=list(els)+[PG([(54,34),(36,66),(72,66)],CO,1),L(54,45,54,56,WH,3.5),C(54,61.5,2.2,WH)]
        open(f'svg/{s}.svg','w').write(svg(els))
        subprocess.run(['rsvg-convert','-w','800','-h','500',f'svg/{s}.svg','-o',f'repo/imagens/graficos/{s}.png'],check=True)
    except Exception as e: err.append((s,repr(e)))
print('erros:',err)
