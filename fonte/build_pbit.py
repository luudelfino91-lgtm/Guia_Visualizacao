# -*- coding: utf-8 -*-
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
for t,fn in [('Dim_Grafico','dim_grafico'),('Dim_Objetivo','dim_objetivo'),('Fato_Selecao','fato_selecao')]:
    df=pd.read_csv(f'repo/dados/{fn}.csv',dtype=str,keep_default_na=False); tables_def[t]=(fn,list(df.columns))
INT={'id_grafico','id_objetivo','ordem','linha_id','id_selecao','vars_ord','tempo_ord','cat_ord','val_ord','comp_ord'}
SORT={('Dim_Objetivo','nome_pt'):'ordem',('Dim_Objetivo','nome_en'):'ordem',
      ('Fato_Selecao','vars_pt'):'vars_ord',('Fato_Selecao','vars_en'):'vars_ord',
      ('Fato_Selecao','tempo_pt'):'tempo_ord',('Fato_Selecao','tempo_en'):'tempo_ord',
      ('Fato_Selecao','cat_pt'):'cat_ord',('Fato_Selecao','cat_en'):'cat_ord',
      ('Fato_Selecao','val_pt'):'val_ord',('Fato_Selecao','val_en'):'val_ord',
      ('Fato_Selecao','comp_pt'):'comp_ord',('Fato_Selecao','comp_en'):'comp_ord'}
HIDE={'ordem','vars_ord','tempo_ord','cat_ord','val_ord','comp_ord','linha_id','slug'}
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
rels=[{'name':g('r1'),'fromTable':'Fato_Selecao','fromColumn':'id_grafico','toTable':'Dim_Grafico','toColumn':'id_grafico'},
      {'name':g('r2'),'fromTable':'Fato_Selecao','fromColumn':'id_objetivo','toTable':'Dim_Objetivo','toColumn':'id_objetivo'}]
model={'name':g('db'),'compatibilityLevel':1567,'model':{'culture':'pt-BR','dataAccessOptions':{'legacyRedirects':True,'returnErrorValuesAsNull':True},
  'defaultPowerBIDataSourceVersion':'powerBI_V3','sourceQueryCulture':'pt-BR','tables':tables,'relationships':rels,
  'annotations':[{'name':'PBI_QueryOrder','value':J(list(tables_def))},{'name':'__PBI_TimeIntelligenceEnabled','value':'0'}]}}

# ---------- 2. Layout ----------
orig=json.load(open('../pbix/layout.json'))
def lit(v): return {'expr':{'Literal':{'Value':v}}}
def txt(s): return lit("'"+s+"'")
def solid(hexc): return {'solid':{'color':lit("'"+hexc+"'")}}
def pos(x,y,w,h,z): return [{'id':0,'position':{'x':x,'y':y,'z':z,'width':w,'height':h}}]
def vc(cfg,x,y,w,h,z): return {'id':int(hx(cfg['name'])[:8],16),'x':x,'y':y,'z':z,'width':w,'height':h,'config':J(cfg),'filters':'[]'}
GENERAL_ALT=lambda s:{'general':[{'properties':{'altText':txt(s)}}]}

def slicer(name,ent,prop,title,x,y,w,h,z,mode,alt):
    ref=f'{ent}.{prop}'
    return vc({'name':name,'layouts':pos(x,y,w,h,z),'singleVisual':{'visualType':'slicer',
      'projections':{'Values':[{'queryRef':ref,'active':True}]},
      'prototypeQuery':{'Version':2,'From':[{'Name':'s','Entity':ent,'Type':0}],'Select':[{'Column':{'Expression':{'SourceRef':{'Source':'s'}},'Property':prop},'Name':ref}]},
      'columnProperties':{ref:{'displayName':title}},'drillFilterOtherVisuals':True,
      'objects':{'data':[{'properties':{'mode':txt(mode)}}],'general':[{'properties':{'orientation':lit('1D')}}],
        'header':[{'properties':{'show':lit('false')}}],
        'items':[{'properties':{'fontColor':solid('#211A2B'),'background':solid('#F4ECFC'),'textSize':lit('11D'),'bold':lit('true')}}]},
      'vcObjects':{'title':[{'properties':{'show':lit('false')}}],'background':[{'properties':{'show':lit('false')}}],
        'visualHeader':[{'properties':{'show':lit('false')}}],**GENERAL_ALT(alt)}}},x,y,w,h,z)

def button(name,target,x,y,w,h,z,alt):
    return vc({'name':name,'layouts':pos(x,y,w,h,z),'singleVisual':{'visualType':'actionButton','drillFilterOtherVisuals':True,
      'objects':{'icon':[{'properties':{'shapeType':txt('blank')},'selector':{'id':'default'}}],
                 'outline':[{'properties':{'show':lit('false')},'selector':{'id':'default'}}],
                 'fill':[{'properties':{'show':lit('false')},'selector':{'id':'default'}}]},
      'vcObjects':{'visualLink':[{'properties':{'show':lit('true'),'type':txt('PageNavigation'),'navigationSection':txt(target)}}],
                   'background':[{'properties':{'show':lit('false')}}],**GENERAL_ALT(alt)}}},x,y,w,h,z)

CB='CardBrowser8D7CFFDA2E7E400C9474F41B9EDBBA58'
def cardbrowser(lang,name,alt):
    L=lang
    sel=[('f','Fato_Selecao','id_selecao',None,None),('g','Dim_Grafico',f'nome_{L}',None,None),('g','Dim_Grafico','imagem_url',None,None)]
    meta=[('o','Dim_Objetivo',f'nome_{L}',{'pt':'Objetivo','en':'Goal'}[L]),
          ('g','Dim_Grafico',f'uso_{L}',{'pt':'Quando usar','en':'When to use'}[L]),
          ('g','Dim_Grafico',f'cuidado_{L}',{'pt':'Cuidado','en':'Watch out'}[L]),
          ('g','Dim_Grafico',f'pbi_{L}',{'pt':'No Power BI','en':'In Power BI'}[L]),
          ('g','Dim_Grafico',f'usado_{L}',{'pt':'Muito usado em','en':'Often used in'}[L]),
          ('g','Dim_Grafico',f'perfil_{L}',{'pt':'Perfil','en':'Profile'}[L])]
    select=[{'Column':{'Expression':{'SourceRef':{'Source':a}},'Property':p},'Name':f'{e}.{p}'} for a,e,p,_,_ in sel]
    proj={'id':[{'queryRef':f'Fato_Selecao.id_selecao'}],'title':[{'queryRef':f'Dim_Grafico.nome_{L}'}],'imageUrl':[{'queryRef':'Dim_Grafico.imagem_url'}],'metadata':[]}
    colprops={}
    for a,e,p,disp in meta:
        qn=f'Min({e}.{p})'
        select.append({'Aggregation':{'Expression':{'Column':{'Expression':{'SourceRef':{'Source':a}},'Property':p}},'Function':3},'Name':qn})
        proj['metadata'].append({'queryRef':qn}); colprops[qn]={'displayName':disp}
    return vc({'name':name,'layouts':pos(34,226,1212,458,0),'singleVisual':{'visualType':CB,'projections':proj,
      'prototypeQuery':{'Version':2,'From':[{'Name':'f','Entity':'Fato_Selecao','Type':0},{'Name':'g','Entity':'Dim_Grafico','Type':0},{'Name':'o','Entity':'Dim_Objetivo','Type':0}],'Select':select},
      'columnProperties':colprops,'drillFilterOtherVisuals':True,
      'objects':{'presentation':[{'properties':{'cropImages':lit('true'),'filter':lit('true'),'shadow':lit('true')}}],
                 'flipState':[{'properties':{'cardFaceDefault':txt('preview')}}],
                 'reader':[{'properties':{'headerBackgroundColor':solid('#7139B8')}}]},
      'vcObjects':{'background':[{'properties':{'show':lit('false')}}],
                   'visualHeader':[{'properties':{'show':lit('false')}}],**GENERAL_ALT(alt)}}},34,226,1212,458,0)

SEC={'pt':'ReportSectionGuiaPT0001','en':'ReportSectionGuideEN0002','sobre':'ReportSectionSobre00003'}
BG={'pt':'fundo_guia_pt','en':'fundo_guide_en','sobre':'fundo_sobre'}
BGFILE={k:f'{v}_{7000000+i}.png' for i,(k,v) in enumerate(BG.items())}
def section(key,disp,ordinal,vcs):
    ids=[]; 
    inter=[]
    sl=[v for v in vcs if '"visualType":"slicer"' in v['config']]
    names=[json.loads(v['config'])['name'] for v in sl]
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

def guia(lang):
    L=lang; T={'pt':['OBJETIVO','VARIÁVEIS','ANÁLISE TEMPORAL?','CATEGORIAS','VALORES','COMPOSIÇÃO'],'en':['GOAL','VARIABLES','TIME ANALYSIS?','CATEGORIES','VALUES','COMPOSITION']}[L]
    specs=[('Dim_Objetivo',f'nome_{L}','Dropdown',156,34),('Fato_Selecao',f'vars_{L}','Basic',152,48),('Fato_Selecao',f'tempo_{L}','Basic',152,48),
           ('Fato_Selecao',f'cat_{L}','Basic',152,48),('Fato_Selecao',f'val_{L}','Basic',152,48),('Fato_Selecao',f'comp_{L}','Basic',152,48)]
    vcs=[cardbrowser(L,hx(f'cb{L}'),{'pt':'Galeria de gráficos filtrada','en':'Filtered chart gallery'}[L])]
    for i,(ent,prop,mode,y,h) in enumerate(specs):
        vcs.append(slicer(hx(f'sl{L}{i}'),ent,prop,T[i].title(),35+i*204+10,y,170,h,1000+i,mode,T[i].title()))
    other='en' if L=='pt' else 'pt'
    if L=='pt':
        vcs+= [button(hx('b1pt'),SEC['en'],1171,33,70,26,6000,'Mudar para inglês'),button(hx('b2pt'),SEC['sobre'],972,30,112,32,6001,'Sobre o guia')]
    else:
        vcs+= [button(hx('b1en'),SEC['pt'],1099,33,70,26,6000,'Switch to Portuguese'),button(hx('b2en'),SEC['sobre'],972,30,112,32,6001,'About the guide')]
    return vcs
sobre_vcs=[button(hx('s1'),SEC['pt'],1012,30,110,32,6000,'Voltar ao guia em português'),button(hx('s2'),SEC['en'],1134,30,110,32,6001,'Go to the English guide')]
sections=[section('pt','Guia (PT)',0,guia('pt')),section('en','Guide (EN)',1,guia('en')),section('sobre','Sobre · About',2,sobre_vcs)]

rp=[{'resourcePackage':{'id':9239865,'name':CB,'type':0,'items':[{'id':27869168,'resourcePackageId':9239865,'type':5,'path':CB+'.pbiviz.json','resourcePackageItemBlobInfoId':107137015}],'disabled':False}},
    {'resourcePackage':{'id':9239867,'name':'RegisteredResources','type':1,'items':[{'type':100,'path':BGFILE[k],'name':BGFILE[k]} for k in BG],'disabled':False}},
    {'resourcePackage':{'id':9239868,'name':'SharedResources','type':2,'items':[{'id':27869171,'resourcePackageId':9239868,'type':202,'path':'BaseThemes/CY22SU03.json','name':'CY22SU03'}],'disabled':False}}]
layout={'id':7570077,'reportId':1328685,'resourcePackages':rp,'sections':sections,'config':orig['config'],'layoutOptimization':0,'publicCustomVisuals':[CB]}

# ---------- 3. Pacote ----------
diag={'version':'1.1.0','diagrams':[{'ordinal':0,'scrollPosition':{'x':0,'y':0},'nodes':[
  {'location':{'x':0,'y':0},'nodeIndex':'Dim_Objetivo','size':{'height':200,'width':234},'zIndex':0},
  {'location':{'x':300,'y':0},'nodeIndex':'Fato_Selecao','size':{'height':300,'width':234},'zIndex':0},
  {'location':{'x':600,'y':0},'nodeIndex':'Dim_Grafico','size':{'height':300,'width':234},'zIndex':0}],
  'name':'Todas as tabelas','zoomValue':100,'pinKeyFieldsToTop':False,'showExtraHeaderInfo':False,'hideKeyFieldsWhenCollapsed':False,'tablesLocked':False}],
  'selectedDiagram':'Todas as tabelas','defaultDiagram':'Todas as tabelas'}
ct=open(f'{ORIG}/[Content_Types].xml','rb').read().decode('utf-8-sig')
for part in ['/Connections','/SecurityBindings','/DataModel']:
    import re; ct=re.sub(r'<Override PartName="%s" ContentType="[^"]*" />'%part,'',ct)
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
