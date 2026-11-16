# Aplica ajustes finais sobre o .pbit exportado do Desktop: links como imagem transparente (sem contorno),
# filtros mais altos e cartões da galeria com altura para a imagem com nome.
import zipfile,json,struct,zlib,sys
def png(w,h):
    raw=b''.join(b'\x00'+b'\x00\x00\x00\x00'*w for _ in range(h))
    def ch(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b'')
TR='transparente_7000008.png'
src,out=sys.argv[1],sys.argv[2]
zi=zipfile.ZipFile(src); zo=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)
L=lambda v:{'expr':{'Literal':{'Value':v}}}
n={'img':0,'sl':0,'cb':0}
for it in zi.infolist():
    data=zi.read(it.filename)
    if it.filename=='Report/definition/report.json':
        r=json.loads(data.decode('utf-8'))
        for p in r['resourcePackages']:
            if p['name']=='RegisteredResources' and not any(i['name']==TR for i in p['items']): p['items'].append({'name':TR,'path':TR,'type':'Image'})
        data=json.dumps(r,ensure_ascii=False,indent=2).encode('utf-8')
    elif it.filename.endswith('visual.json') and '/visuals/' in it.filename:
        d=json.loads(data.decode('utf-8')); v=d['visual']; ch=False
        if v['visualType']=='shape':
            v['visualType']='image'
            v['objects']={'general':[{'properties':{'imageUrl':{'expr':{'ResourcePackageItem':{'PackageName':'RegisteredResources','PackageType':1,'ItemName':TR}}}}}],
                          'imageScaling':[{'properties':{'imageScalingType':L("'Fill'")}}]}
            ch=True; n['img']+=1
        elif v['visualType']=='slicer' and d['position']['y']==122 and d['position']['height']==32:
            d['position']['y']=116; d['position']['height']=44; ch=True; n['sl']+=1
        elif v['visualType'].startswith('CardBrowser') and 'Dim_Grafico.imagem_' in json.dumps(v['query']):
            p=v['objects']['presentation'][0]['properties']
            p['cardHeight']=L('205D' if 'Credit' in it.filename else '172D'); ch=True; n['cb']+=1
        if ch: data=json.dumps(d,ensure_ascii=False,indent=2).encode('utf-8')
    zo.writestr(it,data)
if TR not in zi.namelist() and 'Report/StaticResources/RegisteredResources/'+TR not in zi.namelist():
    zo.writestr('Report/StaticResources/RegisteredResources/'+TR,png(8,8))
zo.close(); print(n); print(zipfile.ZipFile(out).testzip())
