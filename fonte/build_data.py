# -*- coding: utf-8 -*-
import sys, csv, itertools
sys.path.insert(0,'.')
import content as C
import pandas as pd
ORIG='../pbix/tbl_Seleção_de_gráficos.csv'
BASE='https://raw.githubusercontent.com/luudelfino91-lgtm/Guia_Visualizacao/main'
d=pd.read_csv(ORIG,dtype=str)
slugs=list(C.CH.keys()); gid={s:i+1 for i,s in enumerate(slugs)}

# Dim_Grafico
rows=[]
for s in slugs:
    n_pt,n_en,u_pt,u_en,c_pt,c_en,k,p_pt,p_en,d_pt,d_en,perf=C.CH[s]
    kpt,ken=C.KIND[k]
    rows.append(dict(id_grafico=gid[s],slug=s,nome_pt=n_pt,nome_en=n_en,uso_pt=u_pt,uso_en=u_en,
      cuidado_pt=c_pt,cuidado_en=c_en,pbi_pt=f'{kpt} · {p_pt}',pbi_en=f'{ken} · {p_en}',
      usado_pt=d_pt,usado_en=d_en,perfil_pt=C.PERFIL[perf][0],perfil_en=C.PERFIL[perf][1],
      essencial='sim' if s in C.ESSENCIAL else 'não',imagem_url=f'{BASE}/imagens/graficos/{s}.png'))
pd.DataFrame(rows).to_csv('repo/dados/dim_grafico.csv',index=False,encoding='utf-8')

# Dim_Objetivo
orows=[dict(id_objetivo=k,nome_pt=v[0],nome_en=v[1],descricao_pt=v[2],descricao_en=v[3],ordem=k) for k,v in C.OBJ.items()]
pd.DataFrame(orows).to_csv('repo/dados/dim_objetivo.csv',index=False,encoding='utf-8')

# Fato_Selecao (expandido: célula vazia = "tanto faz" => aplica a todas as opções)
VARS={'1':('1','1',1),'2':('2','2',2),'3':('3 ou mais','3 or more',3),'3+':('3 ou mais','3 or more',3)}
TEMPO={'SIM':('Sim','Yes',1),'NÃO':('Não','No',2)}
CAT={'POUCAS':[('Poucas','Few',1)],'MUITAS':[('Muitas','Many',2)]}
CATALL=[('Poucas','Few',1),('Muitas','Many',2)]
VAL={'POUCOS':[('Poucos','Few',1)],'MUITOS':[('Muitos','Many',2)]}
VALALL=[('Poucos','Few',1),('Muitos','Many',2)]
COMP={'absoluta':[('Absoluta','Absolute',1)],'relativa':[('Relativa','Relative',2)],
      'relativa e absoluta':[('Absoluta','Absolute',1),('Relativa','Relative',2)]}
f=[]; lid=0
for _,r in d.iterrows():
    sid=int(r.ID); oid=C.OBJ_ID[r.objetivo_visual]
    cats=CAT.get(r.qtd_categorias,CATALL); vals=VAL.get(r.qtd_valores,VALALL); comps=COMP[r.composicao]
    for ct,vl,cp in itertools.product(cats,vals,comps):
        lid+=1
        v=VARS[r.qtd_variaveis_sem_considerar_tempo]; t=TEMPO[r.status_tempo]
        f.append(dict(linha_id=lid,id_selecao=sid,id_grafico=gid[C.SEL[sid]],id_objetivo=oid,
          vars_pt=v[0],vars_en=v[1],vars_ord=v[2],tempo_pt=t[0],tempo_en=t[1],tempo_ord=t[2],
          cat_pt=ct[0],cat_en=ct[1],cat_ord=ct[2],val_pt=vl[0],val_en=vl[1],val_ord=vl[2],
          comp_pt=cp[0],comp_en=cp[1],comp_ord=cp[2]))
F=pd.DataFrame(f).drop_duplicates(subset=['id_grafico','id_objetivo','vars_ord','tempo_ord','cat_ord','val_ord','comp_ord']).reset_index(drop=True); F['linha_id']=F.index+1; F.to_csv('repo/dados/fato_selecao.csv',index=False,encoding='utf-8')
print('dim_grafico',len(rows),'dim_obj',len(orows),'fato',len(F),'selecoes',F.id_selecao.nunique())
# checagem: toda combinação de filtros tem resultado?
combos=F.groupby(['vars_pt','tempo_pt','cat_pt','val_pt','comp_pt']).id_selecao.nunique()
print('combinações com resultado:',len(combos),'de',3*2*2*2*2)

import json
cases=json.load(open('cases.json'))
pd.DataFrame([dict(id_caso=i+1,titulo_pt=c['t_pt'],titulo_en=c['t_en'],pergunta_pt=c['q_pt'],pergunta_en=c['q_en'],dica_pt=c['n_pt'],dica_en=c['n_en']) for i,c in enumerate(cases)]).to_csv('repo/dados/dim_caso.csv',index=False,encoding='utf-8')
pd.DataFrame([dict(id_caso=i+1,id_grafico=gid[s],ordem=o+1) for i,c in enumerate(cases) for o,s in enumerate(c['charts'])]).to_csv('repo/dados/ponte_caso_grafico.csv',index=False,encoding='utf-8')
