import math
from svgdsl import *
def bars(vals,hl=None,col=V,gap=.38,x0=X0+30,x1=X1-30,base=Y1,top=Y0+10,hlc=LM,horiz=False):
    n=len(vals); m=max(vals); o=[]
    if not horiz:
        step=(x1-x0)/n; bw=step*(1-gap)
        for i,v in enumerate(vals):
            h=(base-top)*v/m
            o.append(R(x0+i*step+(step-bw)/2,base-h,bw,h,hlc if i==hl else col,5))
    else:
        step=(base-top)/n; bh=step*(1-gap)
        for i,v in enumerate(vals):
            w=(x1-x0)*v/m
            o.append(R(X0,top+i*step+(step-bh)/2,w,bh,hlc if i==hl else col,5))
    return o
def smooth(pts):
    d=f'M{f(pts[0][0])},{f(pts[0][1])}'
    for i in range(1,len(pts)):
        x0,y0=pts[i-1]; x1,y1=pts[i]; mx=(x0+x1)/2
        d+=f' C{f(mx)},{f(y0)} {f(mx)},{f(y1)} {f(x1)},{f(y1)}'
    return d
def series(vals,x0=X0+20,x1=X1-10,top=Y0+20,base=Y1-20):
    m=max(vals); n=len(vals)
    return [(x0+(x1-x0)*i/(n-1), base-(base-top)*v/m) for i,v in enumerate(vals)]
def lollipop(vals,hl):
    o=[]; n=len(vals); step=(X1-X0-60)/n; m=max(vals)
    for i,v in enumerate(vals):
        x=X0+30+step*i+step/2; y=Y1-(Y1-Y0-10)*v/m
        o+= [L(x,Y1,x,y,LA,3,.5), C(x,y,11,LM if i==hl else LI)]
    return o
def line_pts(x0,y0,x1,y1): return [(x0,y0),(x1,y1)]
def paired(horiz=False,time=False):
    a=[5,8,6,9,7]; b=[3,6,4,7,5]; o=axes(); n=5; m=9
    if not horiz:
        step=(X1-X0-50)/n; bw=step*.32
        for i in range(n):
            x=X0+25+i*step+step*.17
            o+=[R(x,Y1-(Y1-Y0-10)*a[i]/m,bw,(Y1-Y0-10)*a[i]/m,V,4),R(x+bw+4,Y1-(Y1-Y0-10)*b[i]/m,bw,(Y1-Y0-10)*b[i]/m,LI if i!=2 else LM,4)]
    else:
        n=4; step=(Y1-Y0-20)/n; bh=step*.3
        for i in range(n):
            y=Y0+10+i*step+step*.18
            o+=[R(X0,y,(X1-X0-40)*a[i]/m,bh,V,4),R(X0,y+bh+4,(X1-X0-40)*b[i]/m,bh,LI if i!=1 else LM,4)]
    return o

def g_barra_divergente():
    o=[L(400,Y0,400,Y1,LA,2,.4)]; vals=[7,4,2,-3,-5,-8]
    step=(Y1-Y0)/len(vals)
    for i,v in enumerate(vals):
        w=abs(v)*24; y=Y0+i*step+8
        o.append(R(400 if v>0 else 400-w,y,w,step-18,LI if v>0 else CO,5))
    return o
def g_espinha():
    o=[L(400,Y0,400,Y1,LA,2,.4)]; L_=[6,5,7,4,6]; Rr=[4,5,3,6,4]; step=(Y1-Y0)/5
    for i in range(5):
        y=Y0+i*step+8; o+= [R(400-L_[i]*26,y,L_[i]*26,step-18,V,5), R(400,y,Rr[i]*26,step-18,LM if i==3 else LI,5)]
    return o
def g_area_divergente():
    pts=[(X0+10,300),(240,260),(310,200),(380,230),(450,310),(520,360),(590,330),(X1-10,250)]
    zero=250; o=[L(X0,zero,X1,zero,LA,2,.4)]
    up=[(x,min(y,zero)) for x,y in pts]; dn=[(x,max(y,zero)) for x,y in pts]
    o.append(PG([(pts[0][0],zero)]+up+[(pts[-1][0],zero)],LI,.85)); o.append(PG([(pts[0][0],zero)]+dn+[(pts[-1][0],zero)],CO,.85))
    o.append(PL(pts,LA,3,.9)); return o
def g_dispersao():
    import random; random.seed(4); o=axes()
    for i in range(26):
        x=X0+30+i*17; y=Y1-30-i*8+random.uniform(-45,45); o.append(C(x,y,8,LI,.9))
    o.append(L(X0+30,Y1-20,X1-30,Y0+40,LM,3,.9,'8 8')); return o
def g_bolhas():
    o=axes(); pts=[(230,300,18,V),(300,230,34,LI),(380,320,22,V),(450,180,46,LM),(520,280,28,LI),(580,200,16,V)]
    for x,y,r,c in pts: o.append(C(x,y,r,c,.85))
    return o
def g_calor_xy():
    o=[]; n=6; s=44; gx=X0+55; gy=Y0+10
    import random; random.seed(2)
    for i in range(n):
        for j in range(n):
            t=(i*j+random.random()*8)/40; t=min(1,t)
            col=[BG2,LA,LI,V,'#3A1F66'][min(4,int(t*5))]; 
            o.append(R(gx+i*(s+6),gy+j*(s+6),s,s,LM if (i,j)==(5,5) else col,6))
    return o
def g_colunas(): return axes()+bars([4,9,6,8,5,7],hl=1)
def g_barras(): return axes()+bars([9,7,6,4,3],hl=0,horiz=True,x1=X1-30)
def g_pirulito(): return axes()+lollipop([9,8,6,5,3],0)
def g_inclinacao():
    o=[]; a=[(260,140,220,2),(260,200,330,1)]
    L_=[(150,120),(210,300),(260,230),(330,180)]; Rr=[(100,230),(170,140),(330,290),(250,270)]
    L_=[130,200,270,330]; R_=[230,150,330,270]
    o+= [L(260,Y0,260,Y1,LA,2,.25),L(540,Y0,540,Y1,LA,2,.25)]
    cols=[V,LM,LI,V]
    for l,r,c in zip(L_,R_,cols): o+= [L(260,l+60,540,r+60,c,5 if c==LM else 3.5,1),C(260,l+60,8,c),C(540,r+60,8,c)]
    return o
def g_bump():
    o=[]; xs=[230,330,430,530,610]; ranks={'a':[1,1,2,3,3],'b':[2,3,3,2,1],'c':[3,2,1,1,2],'d':[4,4,4,4,4]}
    cols={'a':V,'b':LM,'c':LI,'d':V}
    for k,r in ranks.items():
        pts=[(x,Y0+30+(rr-1)*70) for x,rr in zip(xs,r)]
        o.append(PL(pts,cols[k] if k=='b' else LA,6 if k=='b' else 3,1 if k=='b' else .45))
        o+= [C(x,y,7 if k=='b' else 5,cols[k] if k=='b' else LA,1 if k=='b' else .5) for x,y in pts]
    return o
def g_tabela():
    o=[]; x=X0+20; y=Y0+10
    o.append(R(x,y,440,34,V,6))
    for r in range(1,6):
        o.append(R(x,y+r*48-6,440,40,BG2,6,1 if r%2==0 else 0))
        for c_,w in enumerate([120,70,90]):
            o.append(R(x+16+[0,160,270][c_],y+r*48+6,w,10,GR,5,.3))
    o.append(R(x+270+14,y+3*48+2,64,18,LM,6)); return o
def g_pontos_amplitude():
    o=[]; rows=[(0,.3,.8),(1,.1,.6),(2,.45,.95),(3,.2,.5)]
    for i,a,b in rows:
        y=Y0+30+i*72; xa=X0+30+a*(X1-X0-80); xb=X0+30+b*(X1-X0-80)
        o+= [L(X0+30,y,X1-20,y,LA,1.5,.15),L(xa,y,xb,y,LA,3,.5),C(xa,y,10,V),C(xb,y,10,LM if i==2 else LI)]
    return o
def g_histograma():
    v=[1,2,4,7,9,7,4,2]; return axes()+bars(v,gap=.06,hl=4)
def g_boxplot():
    o=axes(); stats=[(300,330,230,170,150),(340,300,250,210,160),(280,310,240,200,130)]
    for i,(mn,q1,med,q3,mx) in enumerate(stats):
        x=X0+80+i*140
        o+= [L(x,mx,x,mn,LA,3,.6),L(x-18,mx,x+18,mx,LA,3,.6),L(x-18,mn,x+18,mn,LA,3,.6),R(x-34,q3,68,q1-q3,V if i!=1 else LI,6),L(x-34,med,x+34,med,LM if i==1 else WH,4)]
    o.append(C(X0+80+280+10,120,6,LM)); return o
def g_violino():
    o=axes(); 
    for i,(cx,wid,col) in enumerate([(X0+100,70,V),(X0+230,46,LI),(X0+360,60,V)]):
        top,bot=Y0+10,Y1-10
        pts=[]
        for t in range(0,21):
            y=top+(bot-top)*t/20; w=wid*math.exp(-((t-10+ (i-1)*3)/5)**2)+6
            pts.append((cx+w,y))
        pts2=[(2*cx-x,y) for x,y in reversed(pts)]
        o.append(PG(pts+pts2,col,.9))
        o.append(L(cx,top+60,cx,bot-60,LA,3,.7)); o.append(C(cx,(top+bot)/2,6,LM if i==1 else WH))
    return o
def g_histograma_comparado():
    o=[L(400,Y0,400,Y1,LA,2,.3)]; l=[2,4,7,9,6,3]; r=[1,3,5,7,8,4]; step=(Y1-Y0)/6
    for i in range(6):
        y=Y0+i*step+4; o+= [R(400-l[i]*28,y,l[i]*28,step-8,V,3),R(400,y,r[i]*28,step-8,LI if i!=4 else LM,3)]
    return o
def g_histograma_linha():
    v=[1,2,4,7,9,7,4,2]; o=axes()+bars(v,gap=.06,col=V)
    for r in o: pass
    pts=[(X0+30+(X1-X0-60)*(i+.5)/8, Y1-(Y1-Y0-10)*vv/9) for i,vv in enumerate(v)]
    o=axes()+[R(X0+30+(X1-X0-60)*i/8+2,Y1-(Y1-Y0-10)*vv/9,(X1-X0-60)/8-4,(Y1-Y0-10)*vv/9,V,3,.35) for i,vv in enumerate(v)]
    o.append(P(smooth(pts),stroke=LM,w=5)); return o
def g_superficie():
    o=[]; n=7
    for j in range(n):
        pts=[]
        for i in range(n+3):
            x=X0+40+i*38+j*14; z=math.sin(i/2+j/3)*28+math.cos(j/2)*14
            y=Y0+40+j*34-z
            pts.append((x,y))
        o.append(PL(pts,[V,LI,LA,LI,V,LI,LM][j],3,.9))
    return o
def g_multilinhas():
    o=axes()+grid(3)
    for vals,c,w in [([3,4,5,5,7,8],V,4),([5,5,6,7,6,6],LA,3),([2,3,3,4,4,5],LI,4),([6,7,6,5,4,3],LM,6)]:
        o.append(PL(series(vals+[vals[-1]] if False else vals),c,w,.95 if c==LM else .8))
    return o
def g_linha_coluna():
    o=axes()+bars([5,7,6,8,7,9],col=V,gap=.45)
    pts=series([4,6,5,7,8,9],x0=X0+55,x1=X1-55,top=Y0+30,base=Y1-60); o.append(PL(pts,LM,5)); o+= [C(x,y,7,LM) for x,y in pts]; return o
def g_linha():
    pts=series([2,3,3,5,4,6,8,7,9]); return axes()+grid(3)+[P(smooth(pts),stroke=LI,w=5)]+[C(*pts[-1],9,LM)]
def g_velas():
    o=axes(); data=[(300,230,330,200,'u'),(250,200,280,170,'u'),(260,300,230,330,'d'),(300,260,330,220,'d'),(180,260,160,300,'u'),(150,190,120,230,'u')]
    vs=[(210,270,190,300,1),(250,200,170,290,1),(200,260,180,280,0),(230,300,210,330,0),(180,240,150,290,1),(150,180,120,230,1),(120,170,100,210,1)]
    for i,(o1,c1,hi,lo,up) in enumerate(vs):
        x=X0+40+i*62; top=min(o1,c1); bt=max(o1,c1)
        o+= [L(x,hi-10,x,lo+30,LA,3,.6),R(x-14,top,28,bt-top,LM if i==5 else (LI if up else CO),4)]
    return o
def g_leque():
    o=axes(); hist=series([3,4,4,5,6],x0=X0+20,x1=X0+200,top=Y0+60,base=Y1-80)
    fut=[(hist[-1][0],hist[-1][1])]+[(X0+200+i*60,hist[-1][1]-i*14) for i in range(1,6)]
    for k,(op,sp) in enumerate([(0.22,50),(0.35,30),(0.55,14)]):
        up=[(x,y-sp*i/5) for i,(x,y) in enumerate(fut)]; dn=[(x,y+sp*i/5) for i,(x,y) in enumerate(fut)]
        o.append(PG(up+list(reversed(dn)),LI,op))
    o+= [PL(hist,LA,4,.9),PL(fut,LM,5)]; return o
def g_priestley():
    o=[]; rows=[(0,.05,.5),(1,.2,.7),(2,.35,.55),(3,.5,.95),(4,.15,.4)]
    for i,a,b in rows:
        y=Y0+10+i*58; xa=X0+10+a*(X1-X0-30); xb=X0+10+b*(X1-X0-30)
        o+= [R(xa,y,xb-xa,24,LM if i==3 else (V if i%2==0 else LI),12)]
    o.append(L(X0+10,Y1+5,X1-10,Y1+5,LA,2,.3)); return o
def g_linha_tempo_circular():
    o=[]; cx,cy=400,250
    for r in (60,105,150): o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GR}" stroke-opacity=".22" stroke-width="2"/>')
    import random; random.seed(7)
    for i in range(22):
        a=random.uniform(0,6.28); r=random.choice((60,105,150)); x,y=pol(cx,cy,r,a); o.append(C(x,y,random.choice((6,9,14,20)),LM if i==5 else random.choice((V,LI)),.85))
    return o
def g_sismograma():
    o=[]; import random; random.seed(11)
    for k in range(4):
        y=Y0+30+k*80; pts=[]
        for i in range(60):
            x=X0+10+i*7.5; amp=(18 if k!=2 else 34)*math.exp(-((i-(20+k*8))/9)**2)+3; pts.append((x,y+random.uniform(-amp,amp)))
        o.append(PL(pts,LM if k==2 else (LI if k%2 else V),2.5,1,join='round'))
        o.append(L(X0+10,y,X1-10,y,LA,1,.15))
    return o
def g_streamgraph():
    n=10; xs=[X0+10+(X1-X0-20)*i/(n-1) for i in range(n)]
    import random; random.seed(3)
    layers=[[random.uniform(20,60) for _ in range(n)] for _ in range(4)]
    tot=[sum(l[i] for l in layers) for i in range(n)]; base=[250-t/2 for t in tot]; o=[]
    cur=base[:]
    for k,l in enumerate(layers):
        top=[cur[i]+l[i] for i in range(n)]
        pts=[(xs[i],cur[i]) for i in range(n)]+[(xs[i],top[i]) for i in reversed(range(n))]
        o.append(PG(pts,[V,LI,LM,LA][k],.9 if k!=3 else .55)); cur=top
    return o
def g_radar():
    cx,cy=400,250; o=[]; n=6
    for r in (40,80,120):
        o.append(PG([pol(cx,cy,r,-math.pi/2+i*2*math.pi/n) for i in range(n)],'none',1,LA,1.5).replace('opacity="1"','opacity=".2"'))
    for i in range(n): o.append(L(cx,cy,*pol(cx,cy,120,-math.pi/2+i*2*math.pi/n),LA,1.5,.2))
    vals=[.9,.6,.8,.4,.7,.55]; pts=[pol(cx,cy,120*v,-math.pi/2+i*2*math.pi/n) for i,v in enumerate(vals)]
    o+= [PG(pts,LI,.35,LM,3)]+[C(x,y,6,LM) for x,y in pts]; return o
def g_colunas_pareadas(): return paired()
def g_barras_pareadas(): return paired(horiz=True)
def g_pictograma():
    o=[]; rows=[7,5,3]
    for r,n in enumerate(rows):
        for i in range(n):
            x=X0+40+i*52; y=Y0+20+r*85
            o+= [C(x+16,y+8,9,LM if (r==0 and i==6) else LI),R(x+4,y+22,24,34,LM if (r==0 and i==6) else LI,9)]
    return o
def g_largura_variavel():
    o=axes(); cols=[(90,[5,3,2]),(150,[6,4,3]),(70,[4,6,1]),(110,[3,3,4])]; x=X0+10
    for w,seg in cols:
        tot=sum(seg); y=Y1
        for k,s in enumerate(seg):
            h=(Y1-Y0-10)*s/tot; y-=h
            o.append(R(x,y,w-6,h-3,[V,LI,LM][k] if not(k==2 and x>X0+300) else LA,3))
        x+=w
    return o
def g_coord_paralelas():
    o=[]; xs=[X0+30+i*(X1-X0-60)/4 for i in range(5)]
    for x in xs: o.append(L(x,Y0,x,Y1,LA,2,.35))
    import random; random.seed(5)
    for k in range(8):
        pts=[(x,random.uniform(Y0+20,Y1-20)) for x in xs]; o.append(PL(pts,LA,2.5,.35))
    hl=[(x,y) for x,y in zip(xs,[300,160,250,130,200])]; o.append(PL(hl,LM,5)); return o
def g_bullet():
    o=[]; rows=[(0,.55,.78),(1,.9,.7),(2,.4,.6)]
    for i,v,t in rows:
        y=Y0+30+i*85; w=X1-X0-40
        o+= [R(X0+20,y,w*.5,34,V,4,.35),R(X0+20+w*.5,y,w*.3,34,V,4,.55),R(X0+20+w*.8,y,w*.2,34,V,4,.8),
             R(X0+20,y+11,w*v,12,LM if i==1 else LI,4),L(X0+20+w*t,y-4,X0+20+w*t,y+38,WH,4)]
    return o
def g_velocimetro():
    cx,cy=400,330; o=[]
    for k,(a0,a1,c) in enumerate([(math.pi,math.pi*1.4,V),(math.pi*1.4,math.pi*1.75,LI),(math.pi*1.75,math.pi*2,LA)]):
        o.append(arc(cx,cy,95,150,a0,a1,c,.9))
    a=math.pi*1.62; x,y=pol(cx,cy,125,a); o+= [L(cx,cy,x,y,LM,7),C(cx,cy,16,LM)]; return o
def stacked(n,hundred,horiz):
    o=axes(); data=[[4,3,2,1],[3,4,3,2],[2,3,4,3],[3,2,3,5],[4,4,2,2]][:n]; cols=[V,LI,LA,LM]
    if not horiz:
        step=(X1-X0-40)/n; bw=step*.58
        for i,row in enumerate(data):
            tot=sum(row); y=Y1; scale=(Y1-Y0-10)/(10 if not hundred else tot)
            for k,s in enumerate(row):
                h=s*scale; y-=h; o.append(R(X0+20+i*step+(step-bw)/2,y,bw,h-2,cols[k] if k!=3 else (LM if i==2 else cols[3]),3))
    else:
        step=(Y1-Y0)/n; bh=step*.6
        for i,row in enumerate(data):
            tot=sum(row); x=X0; scale=(X1-X0-30)/(10 if not hundred else tot)
            for k,s in enumerate(row):
                w=s*scale; o.append(R(x,Y0+i*step+(step-bh)/2,w-2,bh,cols[k] if k!=3 else cols[3],3)); x+=w
    return o
def g_barras_100(): return stacked(4,True,True)
def g_colunas_100(): return stacked(5,True,False)
def g_colunas_empilhadas(): return stacked(5,False,False)
def g_area_100():
    n=6; xs=[X0+10+(X1-X0-20)*i/(n-1) for i in range(n)]
    a=[.5,.45,.4,.35,.3,.28]; b=[.3,.32,.34,.36,.38,.4]; o=[]
    h=Y1-Y0-10; y0=Y1
    o.append(PG([(x,y0-h*ai) for x,ai in zip(xs,a)]+[(xs[-1],y0),(xs[0],y0)],V,.95))
    o.append(PG([(x,y0-h*(ai+bi)) for x,ai,bi in zip(xs,a,b)]+[(x,y0-h*ai) for x,ai in reversed(list(zip(xs,a)))],LI,.95))
    o.append(PG([(x,y0-h) for x in xs]+[(x,y0-h*(ai+bi)) for x,ai,bi in reversed(list(zip(xs,a,b)))],LM,.9)); return axes()+o
def g_area_empilhada():
    n=6; xs=[X0+10+(X1-X0-20)*i/(n-1) for i in range(n)]
    a=[40,50,45,60,55,70]; b=[30,35,50,45,60,50]; o=[]
    o.append(PG([(x,Y1-v) for x,v in zip(xs,a)]+[(xs[-1],Y1),(xs[0],Y1)],V,.95))
    o.append(PG([(x,Y1-va-vb) for x,va,vb in zip(xs,a,b)]+[(x,Y1-va) for x,va in reversed(list(zip(xs,a)))],LI,.95))
    return axes()+o
def g_pizza():
    cx,cy=400,250; o=[]; a0=-math.pi/2
    for v,c in [(.55,V),(.25,LI),(.20,LM)]:
        a1=a0+v*2*math.pi; o.append(arc(cx,cy,0,130,a0,a1,c)); a0=a1
    return o
def g_rosca():
    cx,cy=400,250; o=[]; a0=-math.pi/2
    for v,c in [(.55,V),(.25,LI),(.20,LM)]:
        a1=a0+v*2*math.pi; o.append(arc(cx,cy,70,130,a0,a1-0.02,c)); a0=a1
    return o
def g_treemap():
    o=[]; x,y,w,h=X0+10,Y0+5,X1-X0-20,Y1-Y0-10
    o+= [R(x,y,w*.55-4,h,V,6),R(x+w*.55,y,w*.45,h*.55-4,LI,6),R(x+w*.55,y+h*.55,w*.25-4,h*.45,LM,6),R(x+w*.8,y+h*.55,w*.2,h*.45,LA,6)]; return o
def g_cascata():
    o=axes(); steps=[(0,8,'t'),(8,11,'u'),(11,9,'d'),(9,12,'u'),(12,7,'d'),(0,7,'t')]; n=len(steps); step=(X1-X0-40)/n; m=14
    for i,(a,b,t) in enumerate(steps):
        lo,hi=min(a,b),max(a,b); y=Y1-(Y1-Y0-10)*hi/m; h=(Y1-Y0-10)*(hi-lo)/m
        c={'t':V,'u':LI,'d':CO}[t]; 
        if i==5: c=LM
        o.append(R(X0+20+i*step+8,y,step-16,h,c,4))
    return o
def g_venn():
    o=[C(350,250,100,V,.65),C(450,250,100,LI,.6),C(400,320,100,LA,.35)]
    o.append(P('M400,206 A100,100 0 0 1 436,274 A100,100 0 0 1 364,274 A100,100 0 0 1 400,206Z',fill=LM,op=.95)); return o
def g_coluna_100_destaque():
    o=axes(); n=5; step=(X1-X0-40)/n; bw=step*.58; h=Y1-Y0-10
    for i in range(n):
        x=X0+20+i*step+(step-bw)/2; segs=[(.5,V),(.3,LI),(.2,LM if i==2 else LA)]; y=Y1
        for s,c in segs: y-=h*s; o.append(R(x,y,bw,h*s-2,c,3,1 if (c!=LA) else .6))
    return o
def g_waffle():
    o=[]; s=26; gx,gy=X0+90,Y0+5; k=0
    for j in range(10):
        for i in range(10):
            idx=j*10+i; c=LM if idx<12 else (LI if idx<40 else V)
            o.append(R(gx+i*(s+4),gy+(9-j)*(s+4)*.99,s,s,c,5,.95)); 
    return o
def g_coropletico():
    o=[]; cells=[[(0,0,V),(1,0,LI),(2,0,LA)],[(0,1,LI),(1,1,LM),(2,1,V)],[(0,2,LA),(1,2,V),(2,2,LI)]]
    pts=[(300,120),(420,100),(520,140),(560,230),(520,330),(420,380),(320,350),(260,260)]
    o.append(PG(pts,BG2,1,LA,2)); o[-1]=o[-1].replace('opacity="1"','opacity=".6"')
    o+= [PG([(300,120),(420,100),(430,200),(330,220),(260,260)],LI,.9),PG([(420,100),(520,140),(560,230),(430,200)],V,.9),PG([(430,200),(560,230),(520,330),(420,300)],LM,.95),PG([(330,220),(430,200),(420,300),(420,380),(320,350)],V,.7),PG([(260,260),(330,220),(320,350)],LA,.5)]
    return o
def g_mapa_bolhas():
    o=[PG([(300,120),(420,100),(520,140),(560,230),(520,330),(420,380),(320,350),(260,260)],BG2,.6,LA,2)]
    for x,y,r,c in [(360,200,26,V),(470,170,16,LI),(500,280,38,LM),(400,320,20,LI),(330,290,12,V)]: o.append(C(x,y,r,c,.85))
    return o
def g_mapa_fluxo():
    o=[PG([(300,120),(420,100),(520,140),(560,230),(520,330),(420,380),(320,350),(260,260)],BG2,.6,LA,2)]
    hubs=[(330,200),(510,180),(480,320),(350,320)]
    for (x1,y1),(x2,y2),w in [(hubs[0],hubs[1],7),(hubs[0],hubs[2],4),(hubs[3],hubs[1],3)]:
        o.append(P(f'M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-60} {x2},{y2}',stroke=LM if w==7 else LI,w=w,op=.9))
    o+= [C(x,y,9,WH) for x,y in hubs]; return o
def g_mapa_calor():
    o=[PG([(300,120),(420,100),(520,140),(560,230),(520,330),(420,380),(320,350),(260,260)],BG2,.6,LA,2)]
    for x,y,r,op in [(470,260,80,.18),(470,260,52,.3),(470,260,26,.8),(360,190,50,.2),(360,190,26,.4)]: o.append(C(x,y,r,LM if r==26 and x==470 else LI,op))
    return o
def g_sankey():
    o=[]; 
    def band(x0,y0,h0,x1,y1,h1,c,op=.7):
        m=(x0+x1)/2
        return P(f'M{x0},{y0} C{m},{y0} {m},{y1} {x1},{y1} L{x1},{y1+h1} C{m},{y1+h1} {m},{y0+h0} {x0},{y0+h0} Z',fill=c,op=op)
    o+= [R(X0+20,Y0+10,14,150,V,3),R(X0+20,Y0+190,14,90,V,3),R(X1-30,Y0+10,14,120,LI,3),R(X1-30,Y0+170,14,100,LM,3)]
    o+= [band(X0+34,Y0+10,100,X1-30,Y0+10,100,V,.55),band(X0+34,Y0+110,50,X1-30,Y0+170,50,V,.55),band(X0+34,Y0+190,60,X1-30,Y0+120,0,LI,.0),band(X0+34,Y0+190,90,X1-30,Y0+220,50,LM,.8)]
    return o
def g_faixas():
    xs=[X0+30+i*88 for i in range(6)]; o=[]
    pos={'a':[0,0,1,1,2,2],'b':[1,2,0,0,0,1],'c':[2,1,2,2,1,0]}; cols={'a':V,'b':LM,'c':LI}
    hs={'a':[60,55,60,58,50,52],'b':[40,38,70,72,75,60],'c':[30,40,35,40,42,70]}
    for k in 'acb':
        top=[Y0+10+p*85 for p in pos[k]]; h=hs[k]
        poly=[(x,t) for x,t in zip(xs,top)]+[(x,t+hh) for x,t,hh in reversed(list(zip(xs,top,h)))]
        o.append(PG(poly,cols[k],.85 if k!='b' else .95))
    return o
def g_gantt():
    o=[]; rows=[(0,.0,.35),(1,.2,.55),(2,.4,.8),(3,.5,.7),(4,.7,1.0)]
    for i,a,b in rows:
        y=Y0+12+i*58; xa=X0+10+a*(X1-X0-30); xb=X0+10+b*(X1-X0-30)
        o+= [L(X0+10,y+22,X1-10,y+22,LA,1,.1),R(xa,y,xb-xa,26,LM if i==2 else (V if i%2==0 else LI),7)]
    return o
def g_rede():
    pts=[(400,250),(300,170),(500,170),(300,330),(500,330),(220,250),(580,250),(400,120),(400,380)]
    o=[]
    for a,b in [(0,1),(0,2),(0,3),(0,4),(1,5),(2,6),(1,7),(2,7),(3,5),(4,6),(3,8),(4,8)]:
        o.append(L(*pts[a],*pts[b],LA,2.5,.35))
    for i,(x,y) in enumerate(pts): o.append(C(x,y,24 if i==0 else 12,LM if i==0 else (V if i%2 else LI)))
    return o
def g_cordas():
    cx,cy=400,250; o=[]; R_=130
    segs=[(0,.9,V),(1.0,1.9,LI),(2.0,2.7,LM),(2.8,3.7,V),(3.8,4.7,LI),(4.8,6.1,LA)]
    for a0,a1,c in segs: o.append(arc(cx,cy,R_,R_+16,a0,a1,c))
    for a,b,c in [(.45,3.3,V),(1.4,4.2,LM),(2.3,5.4,LI)]:
        x1,y1=pol(cx,cy,R_-2,a); x2,y2=pol(cx,cy,R_-2,b); o.append(P(f'M{f(x1)},{f(y1)} Q{cx},{cy} {f(x2)},{f(y2)}',stroke=c,w=7,op=.7))
    return o
def g_dendrograma():
    o=[]; ys=[Y0+10+i*45 for i in range(7)]
    def j(x0,ya,yb,x1,c=LA):
        return [L(x0,ya,x1,ya,c,3,.8),L(x0,yb,x1,yb,c,3,.8),L(x1,ya,x1,yb,c,3,.8)]
    xr=X1-20
    o+= j(xr-60,ys[0],ys[1],xr-170) ; o+= j(xr-60,ys[2],ys[3],xr-130) ; o+= j(xr-60,ys[5],ys[6],xr-200)
    m1=(ys[0]+ys[1])/2; m2=(ys[2]+ys[3])/2; m3=(ys[5]+ys[6])/2
    o+= [L(xr-170,m1,xr-250,m1,LM,4),L(xr-130,m2,xr-250,m2,LM,4),L(xr-250,m1,xr-250,m2,LM,4)]
    mm=(m1+m2)/2; o+= [L(xr-250,mm,xr-320,mm,LI,3),L(xr-200,m3,xr-320,m3,LI,3),L(xr-320,mm,xr-320,m3,LI,3)]
    o+= [C(xr-60,y,7,V) for y in ys if True][:0]
    o+= [C(xr-60,y,7,LI) for y in ys]; return o
def g_funil():
    o=[]; ws=[420,340,250,170,100]; cols=[V,V,LI,LI,LM]
    for i,w in enumerate(ws):
        y=Y0+i*58; o.append(R(400-w/2,y,w,48,cols[i],8,.95))
    return o
def g_cartao():
    o=[R(250,150,300,200,V,24,.28),R(250,150,300,200,'none',24,1)]
    o[1]=f'<rect x="250" y="150" width="300" height="200" rx="24" fill="none" stroke="{LI}" stroke-opacity=".9" stroke-width="2.5"/>'
    o+= [R(290,200,150,22,LA,8,.35),R(290,245,200,56,LM,10),PL([(470,300),(490,282),(510,291),(530,266)],LI,5)]; return o
def g_sunburst():
    cx,cy=400,250; o=[]
    o.append(C(cx,cy,38,LM))
    a=-math.pi/2
    for v,c in [(.45,V),(.30,LI),(.25,LA)]:
        a1=a+v*2*math.pi; o.append(arc(cx,cy,48,92,a,a1-.02,c,.95))
        sub=[.6,.4]; b=a
        for s in sub:
            b1=b+(a1-a)*s; o.append(arc(cx,cy,98,138,b,b1-.02,c,.6)); b=b1
        a=a1
    return o
