import json,glob,os,sys
sys.path.insert(0,'.')
import content as C, pandas as pd
g=pd.read_csv('repo/dados/dim_grafico.csv',dtype=str).fillna('')
ob=pd.read_csv('repo/dados/dim_objetivo.csv',dtype=str)
fa=pd.read_csv('repo/dados/fato_selecao.csv')
charts=[dict(id=int(r.id_grafico),slug=r.slug,pt=r.nome_pt,en=r.nome_en,uso_pt=r.uso_pt,uso_en=r.uso_en,cuidado_pt=r.cuidado_pt,cuidado_en=r.cuidado_en,pbi_pt=r.pbi_pt,pbi_en=r.pbi_en,usado_pt=r.usado_pt,usado_en=r.usado_en,perfil=[k for k,v in C.PERFIL.items() if v[0]==r.perfil_pt][0],ess=r.essencial=='sim') for r in g.itertuples()]
objs=[dict(id=int(r.id_objetivo),pt=r.nome_pt,en=r.nome_en) for r in ob.itertuples()]
rows=[dict(s=int(r.id_selecao),g=int(r.id_grafico),o=int(r.id_objetivo),v=int(r.vars_ord),t=int(r.tempo_ord),c=int(r.cat_ord),w=int(r.val_ord),p=int(r.comp_ord)) for r in fa.itertuples()]
old=open('simulacao.html').read(); i=old.index('const D=');j=old.index(';\n',i);OD=json.loads(old[i+8:j])
sl={c['slug'] for c in charts}
D=dict(charts=charts,objs=objs,rows=rows,labels=OD['labels'],perfilLabels=OD['perfilLabels'],cases=json.load(open('cases.json')),svg={os.path.basename(f)[:-4]:open(f).read() for f in glob.glob('svg/*.svg') if os.path.basename(f)[:-4] in sl})
av=old[old.index('const AVATAR="')+14:]; av=av[:av.index('"')]
t=open('sim5_tpl.html').read().replace('__D__',json.dumps(D,ensure_ascii=False)).replace('__AV__',av)
open('simulacao5.html','w').write(t); print(len(charts),sum(c['ess'] for c in charts))
