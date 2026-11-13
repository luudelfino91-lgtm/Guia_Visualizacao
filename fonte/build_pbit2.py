# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,".")
import json, uuid, zipfile, shutil, os, glob, copy, hashlib
import pandas as pd
ORIG='../pbix/x'
BASE='https://raw.githubusercontent.com/luudelfino91-lgtm/Guia_Visualizacao/main'
OUT='repo/dist/Guia_Visualizacao_Lucas_Delfino.pbit'
os.makedirs('repo/dist',exist_ok=True)
def g(seed): return str(uuid.UUID(hashlib.md5(seed.encode()).hexdigest()))
def hx(seed): return hashlib.md5(seed.encode()).hexdigest()[:20]
def u16(s): return s.encode('utf-16le')
def J(o): return json.dumps(o,ensure_ascii=False,separators=(',',':'))

# ---------- 1. Modelo (DataModelSchema) ----------
tables_def={}
for t,fn in [('Dim_Grafico','dim_grafico'),('Dim_Objetivo','dim_objetivo'),('Fato_Selecao','fato_selecao'),('Dim_Caso','dim_caso'),('Ponte_Caso_Grafico','ponte_caso_grafico')]:
    df=pd.read_csv(f'repo/dados/{fn}.csv',dtype=str,keep_default_na=False); tables_def[t]=(fn,list(df.columns))
INT={'id_caso','grupo_ord','id_grafico','id_objetivo','ordem','linha_id','id_selecao','vars_ord','tempo_ord','cat_ord','val_ord','comp_ord'}
SORT={('Dim_Grafico','grupo_pt'):'grupo_ord',('Dim_Grafico','grupo_en'):'grupo_ord',('Dim_Caso','titulo_pt'):'id_caso',('Dim_Caso','titulo_en'):'id_caso',('Dim_Objetivo','nome_pt'):'ordem',('Dim_Objetivo','nome_en'):'ordem',
      ('Fato_Selecao','vars_pt'):'vars_ord',('Fato_Selecao','vars_en'):'vars_ord',
      ('Fato_Selecao','tempo_pt'):'tempo_ord',('Fato_Selecao','tempo_en'):'tempo_ord',
      ('Fato_Selecao','cat_pt'):'cat_ord',('Fato_Selecao','cat_en'):'cat_ord',
      ('Fato_Selecao','val_pt'):'val_ord',('Fato_Selecao','val_en'):'val_ord',
      ('Fato_Selecao','comp_pt'):'comp_ord',('Fato_Selecao','comp_en'):'comp_ord'}
HIDE={'grupo_ord','id_caso','ordem','vars_ord','tempo_ord','cat_ord','val_ord','comp_ord','linha_id','slug'}
tables=[]
for t,(fn,cols) in tables_def.items():
    cdefs=[]
    for c in cols:
        d={'name':c,'dataType':'int64' if c in INT else 'string','sourceColumn':c,'lineageTag':g(t+c),'summarizeBy':'none'}
        if c=='imagem_url': d['dataCategory']='ImageUrl'
        if (t,c) in SORT: d['sortByColumn']=SORT[(t,c)]
        if c in HIDE: d['isHidden']=True
        d['annotations']=[{'name':'SummarizationSetBy','value':'User'}]
        cdefs.append(d)
    types=','.join('{"%s", %s}'%(c,'Int64.Type' if c in INT else 'type text') for c in cols)
    m=['let',
       f'    Fonte = Csv.Document(Web.Contents("{BASE}/dados/{fn}.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
       '    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),',
       f'    Tipos = Table.TransformColumnTypes(Cabecalhos, {{{types}}})',
       'in','    Tipos']
    tables.append({'name':t,'lineageTag':g(t),'columns':cdefs,
        'partitions':[{'name':t,'mode':'import','source':{'type':'m','expression':m}}],
        'annotations':[{'name':'PBI_ResultType','value':'Table'}]})
MEAS={'Dim_Grafico':[('Contador_PT','COUNTROWS(Dim_Grafico) & " de " & CALCULATE(COUNTROWS(Dim_Grafico), ALL(Dim_Grafico)) & " gráficos"'),
  ('Contador_EN','COUNTROWS(Dim_Grafico) & " of " & CALCULATE(COUNTROWS(Dim_Grafico), ALL(Dim_Grafico)) & " charts"')],
 'Dim_Caso':[('Texto_Pergunta_PT','SELECTEDVALUE(Dim_Caso[pergunta_pt], "")'),('Texto_Pergunta_EN','SELECTEDVALUE(Dim_Caso[pergunta_en], "")'),
  ('Texto_Dica_PT','VAR d = SELECTEDVALUE(Dim_Caso[dica_pt], "") RETURN IF(d = "", "", "Dica: " & d)'),('Texto_Dica_EN','VAR d = SELECTEDVALUE(Dim_Caso[dica_en], "") RETURN IF(d = "", "", "Tip: " & d)')]}
for tb in tables:
    if tb['name'] in MEAS: tb['measures']=[{'name':n,'expression':e,'lineageTag':g(tb['name']+n)} for n,e in MEAS[tb['name']]]
rels=[{'name':g('r1'),'fromTable':'Fato_Selecao','fromColumn':'id_grafico','toTable':'Dim_Grafico','toColumn':'id_grafico','crossFilteringBehavior':'bothDirections'},
      {'name':g('r3'),'fromTable':'Ponte_Caso_Grafico','fromColumn':'id_grafico','toTable':'Dim_Grafico','toColumn':'id_grafico','crossFilteringBehavior':'bothDirections'},
      {'name':g('r4'),'fromTable':'Ponte_Caso_Grafico','fromColumn':'id_caso','toTable':'Dim_Caso','toColumn':'id_caso'},
      {'name':g('r2'),'fromTable':'Fato_Selecao','fromColumn':'id_objetivo','toTable':'Dim_Objetivo','toColumn':'id_objetivo'}]
model={'name':g('db'),'compatibilityLevel':1567,'model':{'culture':'pt-BR','dataAccessOptions':{'legacyRedirects':True,'returnErrorValuesAsNull':True},
  'defaultPowerBIDataSourceVersion':'powerBI_V3','sourceQueryCulture':'pt-BR','tables':tables,'relationships':rels,
  'annotations':[{'name':'PBI_QueryOrder','value':J(list(tables_def))},{'name':'__PBI_TimeIntelligenceEnabled','value':'0'}]}}

# ---------- 2. Layout ----------
from layout import *
orig=json.load(open('../pbix/layout.json'))
def lit(v): return {'expr':{'Literal':{'Value':v}}}
def txt(s): return lit("'"+s+"'")
def solid(hexc): return {'solid':{'color':lit("'"+hexc+"'")}}
def pos(x,y,w,h,z): return [{'id':0,'position':{'x':x,'y':y,'z':z,'width':w,'height':h}}]
def vc(cfg,x,y,w,h,z): return {'id':int(hx(cfg['name'])[:8],16),'x':x,'y':y,'z':z,'width':w,'height':h,'config':J(cfg),'filters':'[]'}
ALT=lambda s:{'general':[{'properties':{'altText':txt(s)}}]}
NOCHROME={'title':[{'properties':{'show':lit('false')}}],'background':[{'properties':{'show':lit('false')}}],'visualHeader':[{'properties':{'show':lit('false')}}]}
def default_filter(ent,prop,value):
    return {'filter':{'filter':{'Version':2,'From':[{'Name':'d','Entity':ent,'Type':0}],'Where':[{'Condition':{'In':{'Expressions':[{'Column':{'Expression':{'SourceRef':{'Source':'d'}},'Property':prop}}],'Values':[[{'Literal':{'Value':"'"+value+"'"}}]]}}}]}}}

def slicer(name,ent,prop,title,x,y,w,h,z,mode,alt,horizontal=True,single=False,default=None):
    ref=f'{ent}.{prop}'
    gen={'orientation':lit('1D' if horizontal else '0D')}
    if default: gen.update(default_filter(ent,prop,default))
    obj={'data':[{'properties':{'mode':txt(mode)}}],'general':[{'properties':gen}],
         'header':[{'properties':{'show':lit('false')}}],
         'items':[{'properties':{'fontColor':solid('#211A2B'),'background':solid('#F4ECFC'),'textSize':lit('12D'),'fontFamily':txt('Segoe UI')}}]}
    if single: obj['selection']=[{'properties':{'singleSelect':lit('true'),'selectAllCheckboxEnabled':lit('false')}}]
    return vc({'name':name,'layouts':pos(x,y,w,h,z),'singleVisual':{'visualType':'slicer',
      'projections':{'Values':[{'queryRef':ref,'active':True}]},
      'prototypeQuery':{'Version':2,'From':[{'Name':'s','Entity':ent,'Type':0}],'Select':[{'Column':{'Expression':{'SourceRef':{'Source':'s'}},'Property':prop},'Name':ref}]},
      'columnProperties':{ref:{'displayName':title}},'drillFilterOtherVisuals':True,'objects':obj,
      'vcObjects':{**NOCHROME,**ALT(alt)}}},x,y,w,h,z)

def button(name,target,x,y,w,h,z,alt,kind='PageNavigation',url=None):
    link={'show':lit('true'),'type':txt(kind)}
    if kind=='PageNavigation': link['navigationSection']=txt(target)
    if kind=='WebUrl': link['webUrl']=txt(url)
    return vc({'name':name,'layouts':pos(x,y,w,h,z),'singleVisual':{'visualType':'actionButton','drillFilterOtherVisuals':True,
      'objects':{'icon':[{'properties':{'shapeType':txt('blank')},'selector':{'id':'default'}}],
                 'outline':[{'properties':{'show':lit('false')},'selector':{'id':'default'}}],
                 'fill':[{'properties':{'show':lit('false')},'selector':{'id':'default'}}]},
      'vcObjects':{'visualLink':[{'properties':link}],'background':[{'properties':{'show':lit('false')}}],**ALT(alt)}}},x,y,w,h,z)

def card(name,measure,x,y,w,h,z,size,color,alt,bold=False,ent='Dim_Grafico'):
    ref=f'{ent}.{measure}'
    lab={'color':solid(color),'fontSize':lit(f'{size}D'),'fontFamily':txt('Segoe UI Semibold' if bold else 'Segoe UI')}
    return vc({'name':name,'layouts':pos(x,y,w,h,z),'singleVisual':{'visualType':'card','projections':{'Values':[{'queryRef':ref}]},
      'prototypeQuery':{'Version':2,'From':[{'Name':'d','Entity':ent,'Type':0}],'Select':[{'Measure':{'Expression':{'SourceRef':{'Source':'d'}},'Property':measure},'Name':ref}]},
      'objects':{'labels':[{'properties':lab}],'categoryLabels':[{'properties':{'show':lit('false')}}]},
      'vcObjects':{**NOCHROME,**ALT(alt)}}},x,y,w,h,z)

CB='CardBrowser8D7CFFDA2E7E400C9474F41B9EDBBA58'
def cardbrowser(L,name,alt,x,y,w,h):
    cols=[('id_grafico',None),(f'nome_{L}',None),('imagem_url',None)]
    meta=[(f'uso_{L}',{'pt':'Serve para','en':'Use it for'}[L]),(f'cuidado_{L}',{'pt':'Cuidado','en':'Watch out'}[L]),
          (f'pbi_{L}',{'pt':'No Power BI','en':'In Power BI'}[L]),(f'usado_{L}',{'pt':'Muito usado em','en':'Often used in'}[L]),
          (f'perfil_{L}',{'pt':'Perfil','en':'Profile'}[L])]
    select=[{'Column':{'Expression':{'SourceRef':{'Source':'g'}},'Property':p},'Name':f'Dim_Grafico.{p}'} for p,_ in cols]
    proj={'id':[{'queryRef':'Dim_Grafico.id_grafico'}],'title':[{'queryRef':f'Dim_Grafico.nome_{L}'}],'imageUrl':[{'queryRef':'Dim_Grafico.imagem_url'}],'metadata':[]}
    colprops={}
    for p,disp in meta:
        qn=f'Min(Dim_Grafico.{p})'
        select.append({'Aggregation':{'Expression':{'Column':{'Expression':{'SourceRef':{'Source':'g'}},'Property':p}},'Function':3},'Name':qn})
        proj['metadata'].append({'queryRef':qn}); colprops[qn]={'displayName':disp}
    return vc({'name':name,'layouts':pos(x,y,w,h,0),'singleVisual':{'visualType':CB,'projections':proj,
      'prototypeQuery':{'Version':2,'From':[{'Name':'g','Entity':'Dim_Grafico','Type':0}],'Select':select},
      'columnProperties':colprops,'drillFilterOtherVisuals':True,
      'objects':{'presentation':[{'properties':{'cropImages':lit('true'),'filter':lit('true'),'shadow':lit('false')}}],
                 'flipState':[{'properties':{'cardFaceDefault':txt('preview')}}],
                 'reader':[{'properties':{'headerBackgroundColor':solid('#7139B8')}}]},
      'vcObjects':{'background':[{'properties':{'show':lit('false')}}],'visualHeader':[{'properties':{'show':lit('false')}}],**ALT(alt)}}},x,y,w,h,0)

SEC={'pt':'ReportSectionGuiaPT0001','en':'ReportSectionGuideEN0002','cr_pt':'ReportSectionCreditoPT03','cr_en':'ReportSectionCreditEN004','sobre':'ReportSectionSobre00005'}
BG={'pt':'fundo_guia_pt','en':'fundo_guide_en','cr_pt':'fundo_credito_pt','cr_en':'fundo_credit_en','sobre':'fundo_sobre'}
BGFILE={k:f'{v}_{7000000+i}.png' for i,(k,v) in enumerate(BG.items())}
def section(key,disp,ordinal,vcs):
    inter=[]
    names=[json.loads(v['config'])['name'] for v in vcs if '"visualType":"slicer"' in v['config']]
    for a in names:
        for b in names:
            if a!=b: inter.append({'source':a,'target':b,'type':3})
    cfg={'relationships':inter,'objects':{'background':[{'properties':{
        'color':{'solid':{'color':{'expr':{'ThemeDataColor':{'ColorId':1,'Percent':0}}}}},
        'image':{'image':{'name':txt(BG[key]+'.png'),'url':{'expr':{'ResourcePackageItem':{'PackageName':'RegisteredResources','PackageType':1,'ItemName':BGFILE[key]}}},'scaling':txt('Fit')}},
        'transparency':lit('0D')}}],
      'outspace':[{'properties':{'color':solid('#FAF7FE')}}]}}
    return {'id':int(hx(key)[:8],16),'name':SEC[key],'displayName':disp,'filters':'[]','ordinal':ordinal,'visualContainers':vcs,
            'objectId':g('sec'+key),'config':J(cfg),'displayOption':1,'width':1280,'height':720}

LI='https://www.linkedin.com/in/lucasdelfino-/'
def chrome(key,L):
    # botões transparentes sobre o cabeçalho desenhado no fundo
    guide='pt' if L=='pt' else 'en'; cred='cr_pt' if L=='pt' else 'cr_en'
    tpl=lambda k:{'pt':'pt','en':'en'}[k]
    if key=='sobre': tgt_pt,tgt_en='pt','en'
    elif key.startswith('cr'): tgt_pt,tgt_en='cr_pt','cr_en'
    else: tgt_pt,tgt_en='pt','en'
    n=lambda s:hx(f'{key}{s}')
    return [button(n('n1'),SEC[guide],NAV['guia'][0],0,NAV['guia'][1],56,6000,'Guia' if L=='pt' else 'Guide'),
            button(n('n2'),SEC[cred],NAV['cred'][0],0,NAV['cred'][1],56,6001,'Crédito e cobrança' if L=='pt' else 'Credit and collections'),
            button(n('n3'),SEC['sobre'],NAV['sobre'][0],0,NAV['sobre'][1],56,6002,'Sobre o autor' if L=='pt' else 'About the author'),
            button(n('n4'),'',NAV['li'][0],0,NAV['li'][1],56,6003,'LinkedIn de Lucas Delfino','WebUrl',LI),
            button(n('l1'),SEC[tgt_pt],LANG['pt'][0]-2,14,30,28,6004,'Português'),
            button(n('l2'),SEC[tgt_en],LANG['en'][0]+2,14,30,28,6005,'English')]

def guia(L):
    T={'pt':['Objetivo','Variáveis','Análise temporal?','Categorias','Valores','Composição'],'en':['Goal','Variables','Time analysis?','Categories','Values','Composition']}[L]
    specs=[('Dim_Objetivo',f'nome_{L}','Dropdown',36,True),('Fato_Selecao',f'vars_{L}','Basic',48,True),('Fato_Selecao',f'tempo_{L}','Basic',48,True),
           ('Fato_Selecao',f'cat_{L}','Basic',48,True),('Fato_Selecao',f'val_{L}','Basic',48,True),('Fato_Selecao',f'comp_{L}','Basic',48,True)]
    vcs=chrome('pt' if L=='pt' else 'en',L)
    vcs.append(card(hx(f'ct{L}'),'Contador_'+L.upper(),860,62,250,44,100,18,'#7139B8',{'pt':'Quantidade de gráficos exibidos','en':'Number of charts shown'}[L],True))
    vcs.append(button(hx(f'clr{L}'),'',1126,66,106,34,6010,{'pt':'Limpar filtros','en':'Clear filters'}[L],'ClearAllSlicers'))
    vcs.append(slicer(hx(f'mo{L}'),'Dim_Grafico',f'grupo_{L}',{'pt':'Mostrar','en':'Show'}[L],940,114,316,40,1100,'Basic',{'pt':'Mostrar essenciais ou demais gráficos','en':'Show essential or more charts'}[L],default={'pt':'Essenciais','en':'Essentials'}[L]))
    for i,(ent,prop,mode,h,_) in enumerate(specs):
        vcs.append(slicer(hx(f'sl{L}{i}'),ent,prop,T[i],COLS[i],200,COLW[i],h,1000+i,mode,T[i]))
    vcs.append(cardbrowser(L,hx(f'cb{L}'),{'pt':'Galeria de gráficos filtrada','en':'Filtered chart gallery'}[L],24,272,1232,412))
    return vcs
def credito(L):
    key='cr_'+L; first={'pt':'Aging da carteira','en':'Portfolio aging'}[L]
    vcs=chrome(key,L)
    vcs.append(slicer(hx(f'cs{L}'),'Dim_Caso',f'titulo_{L}',{'pt':'Caso de uso','en':'Use case'}[L],24,98,290,580,1000,'Basic',{'pt':'Casos de uso de crédito e cobrança','en':'Credit and collections use cases'}[L],horizontal=False,single=True,default=first))
    vcs.append(card(hx(f'q{L}'),'Texto_Pergunta_'+L.upper(),356,66,900,92,100,24,'#211A2B',{'pt':'Pergunta do caso','en':'Case question'}[L],True,'Dim_Caso'))
    vcs.append(card(hx(f'd{L}'),'Texto_Dica_'+L.upper(),356,160,900,36,101,14,'#4A4158',{'pt':'Dica de leitura','en':'Reading tip'}[L],False,'Dim_Caso'))
    vcs.append(cardbrowser(L,hx(f'cbc{L}'),{'pt':'Gráficos indicados para o caso','en':'Charts suggested for the case'}[L],340,230,916,446))
    return vcs
def sobre():
    vcs=chrome('sobre','pt')
    vcs.append(button(hx('lnk'),'',24,376,250,38,6010,'Conectar no LinkedIn / Connect on LinkedIn','WebUrl',LI))
    return vcs
sections=[section('pt','Descobrir',0,guia('pt')),section('en','Discover',1,guia('en')),section('cr_pt','Crédito e cobrança',2,credito('pt')),section('cr_en','Credit & collections',3,credito('en')),section('sobre','Sobre · About',4,sobre())]

rp=[{'resourcePackage':{'id':9239865,'name':CB,'type':0,'items':[{'id':27869168,'resourcePackageId':9239865,'type':5,'path':CB+'.pbiviz.json','resourcePackageItemBlobInfoId':107137015}],'disabled':False}},
    {'resourcePackage':{'id':9239867,'name':'RegisteredResources','type':1,'items':[{'type':100,'path':BGFILE[k],'name':BGFILE[k]} for k in BG],'disabled':False}},
    {'resourcePackage':{'id':9239868,'name':'SharedResources','type':2,'items':[{'id':27869171,'resourcePackageId':9239868,'type':202,'path':'BaseThemes/CY22SU03.json','name':'CY22SU03'}],'disabled':False}}]
layout={'id':7570077,'reportId':1328685,'resourcePackages':rp,'sections':sections,'config':orig['config'],'layoutOptimization':0,'publicCustomVisuals':[CB]}

# ---------- 3. Pacote ----------
nodes=[('Dim_Objetivo',0,0,200),('Fato_Selecao',300,0,300),('Dim_Grafico',600,0,320),('Ponte_Caso_Grafico',900,0,160),('Dim_Caso',1200,0,200)]
diag={'version':'1.1.0','diagrams':[{'ordinal':0,'scrollPosition':{'x':0,'y':0},'nodes':[{'location':{'x':x,'y':y},'nodeIndex':n,'size':{'height':h,'width':234},'zIndex':0} for n,x,y,h in nodes],
  'name':'Todas as tabelas','zoomValue':100,'pinKeyFieldsToTop':False,'showExtraHeaderInfo':False,'hideKeyFieldsWhenCollapsed':False,'tablesLocked':False}],
  'selectedDiagram':'Todas as tabelas','defaultDiagram':'Todas as tabelas'}
import re
ct=open(f'{ORIG}/[Content_Types].xml','rb').read().decode('utf-8-sig')
for part in ['/Connections','/SecurityBindings','/DataModel']:
    ct=re.sub(r'<Override PartName="%s" ContentType="[^"]*" />'%part,'',ct)
ct=ct.replace('<Override PartName="/Version"','<Override PartName="/DataModelSchema" ContentType="" /><Override PartName="/Version"')
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml',ct.encode('utf-8-sig'))
    z.writestr('Version',open(f'{ORIG}/Version','rb').read())
    z.writestr('DataModelSchema',u16(J(model)))
    z.writestr('DiagramLayout',u16(J(diag)))
    z.writestr('Metadata',open(f'{ORIG}/Metadata','rb').read())
    z.writestr('Settings',open(f'{ORIG}/Settings','rb').read())
    z.writestr('Report/Layout',u16(J(layout)))
    z.write(f'{ORIG}/Report/StaticResources/SharedResources/BaseThemes/CY22SU03.json','Report/StaticResources/SharedResources/BaseThemes/CY22SU03.json')
    for k in BG: z.write(f'repo/imagens/fundos/{BG[k]}.png',f'Report/StaticResources/RegisteredResources/{BGFILE[k]}')
    z.write(f'{ORIG}/Report/CustomVisuals/{CB}/package.json',f'Report/CustomVisuals/{CB}/package.json')
    z.write(f'{ORIG}/Report/CustomVisuals/{CB}/resources/{CB}.pbiviz.json',f'Report/CustomVisuals/{CB}/resources/{CB}.pbiviz.json')
print('ok',os.path.getsize(OUT)//1024,'KB')
json.dump(model,open('model_debug.json','w'),ensure_ascii=False,indent=1)
