import zipfile,json,hashlib,uuid
src='dist/Guia_Visualizacao_Lucas_Delfino.pbit'; out='/home/claude/Guia_Visualizacao_Lucas_Delfino_v3.pbit'
zi=zipfile.ZipFile(src); zo=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)
L=lambda v:{'expr':{'Literal':{'Value':v}}}
n={'shape':0,'cb':0}
for it in zi.infolist():
    data=zi.read(it.filename)
    if it.filename=='DataModelSchema':
        m=json.loads(data.decode('utf-16le'))
        for tb in m['model']['tables']:
            if tb['name']=='Dim_Grafico':
                base=[c for c in tb['columns'] if c['name']=='imagem_url'][0]
                for nm in('imagem_pt','imagem_en'):
                    c=json.loads(json.dumps(base)); c['name']=nm; c['sourceColumn']=nm
                    c['lineageTag']=str(uuid.UUID(hashlib.md5(('Dim_Grafico'+nm).encode()).hexdigest())); tb['columns'].append(c)
                ex=tb['partitions'][0]['source']['expression']
                k=[i for i,l in enumerate(ex) if 'Tipos = ' in l][0]
                ex[k]=ex[k].replace('{"imagem_url", type text}','{"imagem_url", type text},{"imagem_pt", type text},{"imagem_en", type text}')
                assert 'imagem_en' in ex[k]
        data=json.dumps(m,ensure_ascii=False,separators=(',',':')).encode('utf-16le')
    elif it.filename.endswith('visual.json') and '/visuals/' in it.filename:
        v=json.loads(data.decode('utf-8')); vis=v['visual']; ch=False
        if vis['visualType']=='shape':
            vis['objects']['line']=[{'properties':{'show':L('false')}}]; ch=True; n['shape']+=1
        elif vis['visualType'].startswith('CardBrowser'):
            qs=vis['query']['queryState']; img=qs['imageUrl']['projections'][0]
            if img['field']['Column']['Property']=='imagem_url':
                lang=qs['title']['projections'][0]['field']['Column']['Property'][-2:]
                img['field']['Column']['Property']=f'imagem_{lang}'; img['queryRef']=f'Dim_Grafico.imagem_{lang}'
                p=vis['objects']['presentation'][0]['properties']
                p['cropImages']=L('false'); p['fade']=L('false')
                p['cardHeight']=L('215D' if 'Credit' in it.filename else '172D')
                ch=True; n['cb']+=1
        if ch: data=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    zo.writestr(it,data)
zo.close(); print(n)
z=zipfile.ZipFile(out);print(z.testzip(),len(z.namelist()))
