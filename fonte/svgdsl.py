import math
BG1,BG2='#FFFFFF','#F4ECFC'
DK='#170E27'; GR='#211A2B'
V,LI,LA,LM,CO,WH='#7139B8','#B66BEA','#E7C5FF','#D7F34A','#FF665D','#FFFFFF'
X0,X1,Y0,Y1=170,630,100,400     # área de desenho (margens generosas = espaço negativo)
W,H=800,500
def f(n): return f'{n:.1f}'.rstrip('0').rstrip('.')
def _o(fill): return f' stroke="{DK}" stroke-width="2"' if fill==LM else ''
def R(x,y,w,h,fill=V,rx=4,op=1): return f'<rect x="{f(x)}" y="{f(y)}" width="{f(max(w,0))}" height="{f(max(h,0))}" rx="{rx}" fill="{fill}" opacity="{op}"{_o(fill)}/>'
def L(x1,y1,x2,y2,c=LA,w=2,op=1,dash=None,cap='round'):
    c=GR if c==LA else (DK if c in (LM,WH) else c)
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}" opacity="{op}" stroke-linecap="{cap}"{d}/>'
def PL(pts,c=LI,w=4,op=1,fill='none',join='round'):
    c=GR if c==LA else (DK if c in (LM,WH) else c)
    p=' '.join(f'{f(x)},{f(y)}' for x,y in pts)
    return f'<polyline points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="{join}" stroke-linecap="round" opacity="{op}"/>'
def PG(pts,fill=V,op=1,stroke='none',w=0):
    if stroke==LA: stroke='#9C8AB0'
    if fill==LM and stroke=='none': stroke,w=DK,2
    p=' '.join(f'{f(x)},{f(y)}' for x,y in pts)
    return f'<polygon points="{p}" fill="{fill}" opacity="{op}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'
def C(cx,cy,r,fill=V,op=1,stroke='none',w=0):
    if fill==WH: fill=DK
    if fill==LM and stroke=='none': stroke,w=DK,2
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" opacity="{op}" stroke="{stroke}" stroke-width="{w}"/>'
def P(d,fill='none',stroke='none',w=0,op=1):
    if stroke==LM: stroke=DK
    if fill==LM and stroke=='none': stroke,w=DK,2
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>'
def pol(cx,cy,r,a): return cx+r*math.cos(a), cy+r*math.sin(a)
def arc(cx,cy,r0,r1,a0,a1,fill=V,op=1):
    large=1 if (a1-a0)%(2*math.pi)>math.pi else 0
    x0,y0=pol(cx,cy,r1,a0); x1,y1=pol(cx,cy,r1,a1); x2,y2=pol(cx,cy,r0,a1); x3,y3=pol(cx,cy,r0,a0)
    if r0<=0.1: d=f'M{f(cx)},{f(cy)} L{f(x0)},{f(y0)} A{f(r1)},{f(r1)} 0 {large} 1 {f(x1)},{f(y1)} Z'
    else: d=f'M{f(x0)},{f(y0)} A{f(r1)},{f(r1)} 0 {large} 1 {f(x1)},{f(y1)} L{f(x2)},{f(y2)} A{f(r0)},{f(r0)} 0 {large} 0 {f(x3)},{f(y3)} Z'
    return P(d,fill=fill,op=op)
def axes(x=True,y=True,c=LA,op=.35):
    o=[]
    if y: o.append(L(X0,Y0-10,X0,Y1,c,2,op))
    if x: o.append(L(X0,Y1,X1,Y1,c,2,op))
    return o
def grid(n=3,c=LA,op=.12):
    return [L(X0,Y1-(Y1-Y0)*i/n,X1,Y1-(Y1-Y0)*i/n,c,1.5,op) for i in range(1,n+1)]
def svg(els):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
      f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'
      f'<radialGradient id="r" cx="0.85" cy="0.1" r="0.7"><stop offset="0" stop-color="{V}" stop-opacity=".10"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient></defs>'
      f'<rect width="{W}" height="{H}" fill="url(#g)"/><rect width="{W}" height="{H}" fill="url(#r)"/>'+''.join(els)+f'<text x="772" y="478" text-anchor="end" font-family="Inter,Segoe UI,sans-serif" font-size="14" font-weight="700" letter-spacing=".4" fill="{V}" opacity=".6">Lucas Delfino</text></svg>')
