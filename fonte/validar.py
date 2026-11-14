import zipfile,json,collections
z=zipfile.ZipFile('repo/dist/Guia_Visualizacao_Lucas_Delfino.pbit')
m=json.loads(z.read('DataModelSchema').decode('utf-16le')); L=json.loads(z.read('Report/Layout').decode('utf-16le'))
bad=[]
for t in m['model']['tables']:
    names=[c['name'].lower() for c in t['columns']]+[x['name'].lower() for x in t.get('measures',[])]
    bad+=[(t['name'],n) for n,c in collections.Counter(names).items() if c>1]
print('nomes duplicados:',bad)
tb={t['name'] for t in m['model']['tables']}
print('relações:',[(r['fromTable'],r['toTable']) for r in m['model']['relationships']], all(r['fromTable'] in tb and r['toTable'] in tb for r in m['model']['relationships']))
cols={t['name']:{c['name'] for c in t['columns']}|{x['name'] for x in t.get('measures',[])} for t in m['model']['tables']}
miss=[];names={s['name'] for s in L['sections']};ids=[]
for s in L['sections']:
    seen=set()
    for v in s['visualContainers']:
        c=json.loads(v['config']); sv=c['singleVisual']; 
        assert c['name'] not in seen; seen.add(c['name'])
        pq=sv.get('prototypeQuery')
        if pq:
            fm={f['Name']:f['Entity'] for f in pq['From']}
            for sel in pq['Select']:
                e=sel.get('Column') or sel.get('Measure') or sel['Aggregation']['Expression']['Column']
                if e['Property'] not in cols[fm[e['Expression']['SourceRef']['Source']]]: miss.append((s['displayName'],e['Property']))
        lk=sv.get('vcObjects',{}).get('visualLink')
        if lk and 'navigationSection' in lk[0]['properties']:
            assert lk[0]['properties']['navigationSection']['expr']['Literal']['Value'].strip("'") in names
    print(s['displayName'],len(s['visualContainers']))
print('referências quebradas:',miss)
for f in z.namelist():
    if 'Registered' in f: print(f)
