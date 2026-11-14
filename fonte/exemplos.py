# -*- coding: utf-8 -*-
import asyncio, base64, math
from playwright.async_api import async_playwright
F='/tmp/claude-0/-home-claude/521df494-154e-5052-9bc2-95f5f31a5721/scratchpad/fonts/node_modules/@fontsource'
B64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
CSS='''@font-face{font-family:Brico;font-weight:800;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:400;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:600;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:700;src:url(data:font/woff2;base64,%s)}
*{margin:0;padding:0}body{width:800px;height:500px;background:#fff;overflow:hidden}svg{display:block}'''%(B64(F+'/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2'),B64(F+'/inter/files/inter-latin-400-normal.woff2'),B64(F+'/inter/files/inter-latin-600-normal.woff2'),B64(F+'/inter/files/inter-latin-700-normal.woff2'))
INK,V,LI,LA,LM,CO,GRY,SOFT,MUT='#211A2B','#7139B8','#B66BEA','#E7C5FF','#D7F34A','#FF665D','#DDD6E6','#F4ECFC','#5F5670'
def T(x,y,s,size=14,fill=INK,w=400,anchor='start',fam='Inter'):
    return f'<text x="{x}" y="{y}" font-family="{fam},sans-serif" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
def Rc(x,y,w,h,fill,rx=3,stroke='none',sw=0): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def Ln(x1,y1,x2,y2,c=GRY,w=1,dash=None): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def Pl(pts,c=V,w=4): return '<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'
def Ci(x,y,r,fill): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK if fill==LM else "none"}" stroke-width="2"/>'
MES={'pt':['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],'en':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}
VEN=[42,45,48,52,58,64,60,56,53,52,53,54]
def cols(vals,x0,y0,x1,y1,colors,top=70,grid=False,labels=None,ticks=False,box=False,lab_idx=None,mes=None,lblsz=11):
    o=[]
    if box: o.append(Rc(x0-30,y0-14,x1-x0+50,y1-y0+44,'none',0,'#6A6277',2))
    if grid or ticks:
        for t in range(0,top+1,10):
            y=y1-(y1-y0)*t/top
            if grid: o.append(Ln(x0,y,x1,y,'#6A6277' if box else GRY,1.2))
            if ticks: o.append(T(x0-8,y+4,str(t),11,MUT,400,'end'))
    n=len(vals); st=(x1-x0)/n; bw=st*.62
    for i,v in enumerate(vals):
        h=(y1-y0)*v/top; x=x0+i*st+(st-bw)/2
        o.append(Rc(x,y1-h,bw,h,colors[i] if isinstance(colors,list) else colors,2,INK if (isinstance(colors,list) and colors[i]==LM) else 'none',2))
        if labels=='all' or (lab_idx and i in lab_idx): o.append(T(x+bw/2,y1-h-6,str(v),lblsz,INK,600,'middle'))
        if mes: o.append(T(x+bw/2,y1+18,mes[i],11,MUT,400,'middle'))
    o.append(Ln(x0,y1,x1,y1,'#6A6277',1.5))
    return ''.join(o)
def line(vals,x0,y0,x1,y1,c=V,w=4,top=70,lo=0):
    n=len(vals); return [(x0+(x1-x0)*i/(n-1),y1-(y1-y0)*(v-lo)/(top-lo)) for i,v in enumerate(vals)],Pl([(x0+(x1-x0)*i/(n-1),y1-(y1-y0)*(v-lo)/(top-lo)) for i,v in enumerate(vals)],c,w)
def tag(kind,L):
    txt={'antes':{'pt':'ANTES','en':'BEFORE'},'depois':{'pt':'DEPOIS','en':'AFTER'}}[kind][L]
    bg,fg=(CO,'#fff') if kind=='antes' else (LM,INK)
    return Rc(28,22,86 if L=='pt' else 80,26,bg,3,INK if kind=='depois' else 'none',1.5)+T(28+(43 if L=='pt' else 40),40,txt,12,fg if kind=='antes' else INK,700,'middle')
def wrap(inner,kind,L):
    note={'pt':'Dados ilustrativos','en':'Illustrative data'}[L]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500"><rect width="800" height="500" fill="#fff"/>{tag(kind,L)}{inner}'+T(28,482,note,11,MUT)+T(772,482,'Lucas Delfino',11,'#8C8199',600,'end')+'</svg>'
S={'pt':dict(sales='Vendas',ctx_q='QUEM',ctx_qv='Diretoria comercial',ctx_d='DECISÃO',ctx_dv='Manter ou cortar o canal Parceiros?',ctx_i='IDEIA PRINCIPAL',ctx_iv='Parceiros vendem menos a cada trimestre.',
  ch=['Loja','Site','App','Rep.','Atacado','Parceiros','Outros'],peak='Junho: pico de 64',title7='Vendas caíram 19% depois de junho',sub7='Vendas mensais, em milhares de unidades',t_months='Vendas por mês',
  step=['Contexto','Virada','Ação'],stepv=['Vendas crescem até junho','Caem 19% depois','Reforçar o canal Parceiros'],h5a='Resultado do ano',h5s='Vendas mensais',note5='Fonte: sistema comercial',
  series=['Loja','Site','App'],leg='Legenda'),
 'en':dict(sales='Sales',ctx_q='WHO',ctx_qv='Sales leadership',ctx_d='DECISION',ctx_dv='Keep or cut the Partners channel?',ctx_i='BIG IDEA',ctx_iv='Partners sell less every quarter.',
  ch=['Store','Web','App','Reps','Wholesale','Partners','Other'],peak='June: peak of 64',title7='Sales fell 19% after June',sub7='Monthly sales, in thousands of units',t_months='Sales by month',
  step=['Context','Turn','Action'],stepv=['Sales grow until June','Fall 19% after','Reinforce the Partners channel'],h5a='Year results',h5s='Monthly sales',note5='Source: sales system',
  series=['Store','Web','App'],leg='Legend')}
CH=[24,19,16,14,11,9,7]
def ex(L):
    s=S[L]; M=MES[L]; out={}
    # 1 contexto
    out['contexto_antes']=cols(VEN,90,110,740,400,V,grid=True,ticks=True,mes=M)+T(90,86,s['sales'],16,INK,700)
    ch=[24,19,16,14,11,6,5]
    pan=''.join(Ln(40,y+12,300,y+12,GRY,1)+T(40,y,s[k],11,V,700)+T(40,y+32,s[k+'v'][:34] if len(s[k+'v'])<=34 else s[k+'v'][:34],14,INK,600) for k,y in [('ctx_q',110),('ctx_d',190),('ctx_i',290)] for _ in [0])
    # wrap long text manually
    def para(x,y,txt,size=14,w=24):
        words=txt.split(); lines=[]; cur=''
        for wd in words:
            if len(cur+' '+wd)>w: lines.append(cur); cur=wd
            else: cur=(cur+' '+wd).strip()
        lines.append(cur); return ''.join(T(x,y+i*(size+6),l,size,INK,600) for i,l in enumerate(lines))
    left=T(40,118,s['ctx_q'],11,V,700)+para(40,142,s['ctx_qv'])+T(40,208,s['ctx_d'],11,V,700)+para(40,232,s['ctx_dv'])+T(40,320,s['ctx_i'],11,V,700)+para(40,344,s['ctx_iv'])
    cc=[LA]*5+[LM]+[LA]
    right=''.join(T(0,0,'',1) for _ in [0])
    bx=''
    for i,(nm,v) in enumerate(zip(s['ch'],ch)):
        y=120+i*42; bx+=T(388,y+17,nm,13,INK,600 if i==5 else 400,'end')+Rc(400,y,(v/24)*320,26,LM if i==5 else LA,3,INK if i==5 else 'none',2)+T(400+(v/24)*320+8,y+18,str(v),12,INK,600)
    out['contexto_depois']=left+Ln(330,110,330,410,GRY,1)+bx
    # 2 escolher
    ang=-math.pi/2; pie=''; pal=[V,LI,LA,'#9C8AB0',LM,CO,'#4B2A80']
    for i,v in enumerate(CH):
        a1=ang+2*math.pi*v/sum(CH); x0,y0=240+120*math.cos(ang),250+120*math.sin(ang); x1,y1=240+120*math.cos(a1),250+120*math.sin(a1)
        pie+=f'<path d="M240,250 L{x0:.1f},{y0:.1f} A120,120 0 {1 if a1-ang>math.pi else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{pal[i]}" stroke="#fff" stroke-width="2"/>'; ang=a1
    leg=''.join(Rc(450,112+i*34,16,16,pal[i],2)+T(476,125+i*34,f'{s["ch"][i]}  {CH[i]}%',14,INK) for i in range(7))
    out['escolher_antes']=pie+leg
    b=''
    for i,(nm,v) in enumerate(zip(s['ch'],CH)):
        y=110+i*48; b+=T(150,y+22,nm,15,INK,600 if i==0 else 400,'end')+Rc(166,y,(v/24)*540,32,LM if i==0 else LA,3,INK if i==0 else 'none',2)+T(166+(v/24)*540+10,y+22,f'{v}%',14,INK,600)
    out['escolher_depois']=b
    # 3 ruido
    out['ruido_antes']=cols(VEN,100,110,730,400,[V]*12,grid=True,ticks=True,box=True,labels='all',mes=M,lblsz=10)+Rc(600,64,12,12,V,0)+T(618,75,s['sales'],12,INK)
    out['ruido_depois']=cols(VEN,90,130,740,400,LA,lab_idx=[5],mes=M)
    out['ruido_depois']=out['ruido_depois'].replace(LA,LA)
    # 4 olhar
    out['olhar_antes']=cols(VEN,90,110,740,400,V,mes=M)+T(90,86,s['sales'],16,INK,700)
    colr=[LA]*12; colr[5]=LM
    out['olhar_depois']=cols(VEN,90,130,740,400,colr,lab_idx=[5],mes=M)+T(388,112,s['peak'],14,INK,700,'middle')
    # 5 designer
    ch5=cols(VEN[:8],360,260,700,400,V,mes=M[:8])
    out['designer_antes']=T(400,100,s['h5s'],12,MUT,400,'middle')+T(60,150,s['h5a'],30,INK,700,fam='Brico')+f'<g transform="translate(40,60)">{cols(VEN[:8],300,200,600,360,V,mes=M[:8])}</g>'+T(120,440,s['note5'],18,V,600)+T(560,250,s['sales'],22,LI,700)
    out['designer_depois']=T(70,100,s['h5a'],30,INK,800,fam='Brico')+T(70,126,s['h5s'],14,MUT)+cols(VEN,70,170,730,400,LA,mes=M,lab_idx=[5])+Ci(0,0,0,'none')+T(70,452,s['note5'],12,MUT)
    # 6 historia
    mini=lambda x,y,w,h,kind:''
    ant=cols([6,9,5,8],50,120,220,230,V)+Pl([(300+i*40,230-v*5) for i,v in enumerate([6,9,5,8,7])],LI,3)+''.join(Ci(560,170,60,V) for _ in [0])+cols([8,6,4,3],470,300,730,400,LA)+cols([5,8,6],50,300,220,400,V)+cols([4,7,5,9],300,320,430,400,LI)
    out['historia_antes']=ant
    dep=''
    for i in range(3):
        x=40+i*250
        dep+=T(x,128,str(i+1),44,LM if False else V,800,fam='Brico')+T(x+40,120,s['step'][i].upper(),12,V,700)+T(x+40,142,s['stepv'][i][:26],14,INK,600)
        if i<2:
            vv=VEN; pts,pl=line(vv,x,200,x+210,340,LA,3,70,40); dep+=pl
            if i==0: _,p2=line(vv[:6],x,200,x+210*5/11,340,V,5,70,40); dep+=p2+Ci(*pts[5],7,LM)
            else: _,p2=line(vv[5:],x+210*5/11,200,x+210,340,CO,5,70,40); dep+=p2
            if i==1: dep=dep.replace('','')
        else:
            dep+=cols([24,19,16,14,11,6,5],x+10,200,x+210,340,[LA]*5+[LM,LA],top=24)
        dep+=Ln(x,380,x+210,380,GRY,1)
    out['historia_depois']=dep
    # 7 titulo
    pts,pl=line(VEN,90,150,730,380,LA,4,70,36)
    out['titulo_antes']=T(90,92,s['t_months'],20,INK,700)+Ln(90,380,730,380,'#6A6277',1.5)+pl.replace(LA,V)
    _,p1=line(VEN[:6],90,170,90+640*5/11,380,LA,4,70,36); _,p2=line(VEN[5:],90+640*5/11,170,730,380,CO,6,70,36)
    out['titulo_depois']=T(90,92,s['title7'],26,INK,800,fam='Brico')+T(90,116,s['sub7'],13,MUT)+Ln(90,380,730,380,'#6A6277',1.5)+pl.replace(LA,LA)+p2+Ci(*pts[5],7,LM)+Ci(*pts[9],7,CO)+T(pts[5][0],pts[5][1]-14,'64',13,INK,700,'middle')+T(pts[9][0],pts[9][1]+24,'52',13,INK,700,'middle')
    # 8 rotulos
    ser=[[40,42,45,47,50,52,51,49,47,46,46,47],[20,24,28,33,38,44,48,52,55,58,61,64],[10,12,13,15,16,18,19,21,22,24,25,27]]
    colsr=[LI,V,'#8C8199']; items=[]
    ant=''; dep=''
    for k,vv in enumerate(ser):
        pts,pl=line(vv,90,120,660,370,colsr[k],4 if k==1 else 3,70,0); ant+=pl; dep+=pl
        dep+=T(pts[-1][0]+10,pts[-1][1]+5,s['series'][k],14,colsr[k] if k!=0 else '#8E4BC4',700)
    ant+=''.join(Rc(250+i*110,430,14,14,colsr[i],2)+T(270+i*110,442,s['series'][i],13,INK) for i in range(3))+T(180,442,s['leg'],12,MUT)
    base=Ln(90,370,660,370,'#6A6277',1.5)
    out['rotulos_antes']=base+ant+''.join(Ln(90,370-(250)*t/70,740,370-(250)*t/70,GRY,1) for t in (20,40,60))
    out['rotulos_depois']=base+dep
    return out
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':800,'height':500},device_scale_factor=1.5)
        for L in ('pt','en'):
            for k,inner in ex(L).items():
                topic,kind=k.rsplit('_',1)
                await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{wrap(inner,kind,L)}</body></html>'); await pg.wait_for_timeout(120)
                await pg.screenshot(path=f'repo/imagens/storytelling/{topic}_{kind}_{L}.png')
        await b.close()
asyncio.run(main())
