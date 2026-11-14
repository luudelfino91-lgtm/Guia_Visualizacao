# -*- coding: utf-8 -*-
import asyncio, base64
from playwright.async_api import async_playwright
from layout import *
F='/tmp/claude-0/-home-claude/521df494-154e-5052-9bc2-95f5f31a5721/scratchpad/fonts/node_modules/@fontsource'
B64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
AV=base64.b64encode(open('avatar.jpg','rb').read()).decode()
CSS='''
@font-face{font-family:Brico;font-weight:700;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Brico;font-weight:800;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:400;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:600;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:Inter;font-weight:700;src:url(data:font/woff2;base64,%s)}
'''%tuple(B64(p) for p in [F+'/bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2',F+'/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2',F+'/inter/files/inter-latin-400-normal.woff2',F+'/inter/files/inter-latin-600-normal.woff2',F+'/inter/files/inter-latin-700-normal.woff2'])+'''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1280px;height:720px;background:#FBF9FD;font-family:Inter,sans-serif;color:#211A2B;position:relative;overflow:hidden;font-size:14px}
.a{position:absolute}
.hd{left:0;top:0;width:1280px;height:56px;background:#1C0F33}
.brand{left:24px;top:11px;color:#fff;font:700 17px Brico,sans-serif;letter-spacing:-.2px;line-height:1.05}
.brand small{display:block;font:600 9px Inter;letter-spacing:1.3px;color:#B9A8D6;margin-top:3px}
.nv{top:0;height:56px;display:flex;align-items:center;justify-content:center;color:#CFC2E6;font-size:14px}
.nv i{font-style:normal;position:relative;padding:5px 0}
.nv.cur{color:#fff}.nv.cur i{border-bottom:2px solid #D7F34A}
.lg{top:17px;height:22px;width:30px;display:flex;align-items:center;justify-content:center;font-size:12px;color:#CFC2E6;border-radius:2px}
.lg.on{background:#fff;color:#1C0F33;font-weight:700}
.me{left:1218px;top:9px;width:38px;height:38px;border-radius:50%;background-size:cover;background-position:center}
h1{left:24px;top:62px;font:800 30px/1.05 Brico,sans-serif;letter-spacing:-.6px;color:#211A2B}
h1 mark{background:linear-gradient(transparent 58%,#D7F34A 58% 92%,transparent 92%);color:inherit;padding:0 2px}
.sub{left:24px;top:100px;color:#5F5670;font-size:14px}
.lab{font:700 11px Inter;letter-spacing:1.3px;color:#6A6277;text-transform:uppercase}
.lab i{font-style:normal;color:#7139B8;margin-right:6px}
.line{height:1px;background:#E3DAEE;left:24px;width:1232px}
.btn{border:1px solid #211A2B;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:14px;color:#211A2B}
.foot{left:24px;top:696px;font-size:11px;color:#6A6277}
.q{font:800 28px/1.12 Brico,sans-serif;letter-spacing:-.5px}
'''
def header(cur,lang):
    L=lambda k,t,c=False:f'<div class="a nv{" cur" if c else ""}" style="left:{NAV[k][0]}px;width:{NAV[k][1]}px"><i>{t}</i></div>'
    names={'pt':('Guia','Storytelling','Crédito e cobrança','Sobre o autor'),'en':('Guide','Storytelling','Credit & collections','About the author')}[lang]
    return (f'<div class="a hd"></div><div class="a brand">Lucas Delfino<small>DATA &amp; BI ANALYST</small></div>'
      +L('guia',names[0],cur=='guia')+L('st',names[1],cur=='st')+L('cred',names[2],cur=='cred')+L('sobre',names[3],cur=='sobre')+L('port',{'pt':'Portfólio ↗','en':'Portfolio ↗'}[lang])+L('li','LinkedIn ↗')
      +f'<div class="a lg{" on" if lang=="pt" else ""}" style="left:{LANG["pt"][0]-2}px">PT</div><div class="a lg{" on" if lang=="en" else ""}" style="left:{LANG["en"][0]+2}px">EN</div>'
      +f'<div class="a me" style="background-image:url(data:image/jpeg;base64,{AV})"></div>')
FOOT='<div class="a foot">© Lucas Delfino · CC BY 4.0 · github.com/luudelfino91-lgtm/Guia_Visualizacao</div>'
def guia(lang):
    pt=lang=='pt'
    T={'pt':['Objetivo','Variáveis','Análise temporal?','Categorias','Valores','Composição'],'en':['Goal','Variables','Time analysis?','Categories','Values','Composition']}[lang]
    title='Qual <mark>gráfico</mark> usar?' if pt else 'Which <mark>chart</mark> to use?'
    labs=''.join(f'<div class="a lab" style="left:{COLS[i]}px;top:107px"><i>0{i+1}</i>{T[i]}</div>' for i in range(6))
    return (header('guia',lang)+f'<h1 class="a" style="font-size:26px;top:62px">{title}</h1>'
      +f'<div class="a btn" style="left:1126px;top:64px;width:106px;height:32px;font-size:13px">{"Limpar filtros" if pt else "Clear filters"}</div>'
      +f'<div class="a lab" style="left:470px;top:76px">{"Mostrar" if pt else "Show"}</div>'
      +'<div class="a line" style="top:100px"></div>'+labs+'<div class="a line" style="top:160px"></div>'+FOOT)
def storytelling(lang):
    pt=lang=='pt'
    note='Inspirado nas lições do livro <b>Storytelling with Data</b>, de Cole Nussbaumer Knaflic. Textos e exemplos são originais.' if pt else 'Inspired by the lessons of <b>Storytelling with Data</b> by Cole Nussbaumer Knaflic. Texts and examples are original.'
    return (header('st',lang)+f'<div class="a lab" style="left:24px;top:74px">{"Tópicos" if pt else "Topics"}</div>'
      +'<div class="a" style="left:330px;top:74px;width:1px;height:610px;background:#E3DAEE"></div>'
      +f'<div class="a lab" style="left:340px;top:170px">{"Como aplicar" if pt else "How to apply"}</div>'
      +f'<div class="a lab" style="left:340px;top:310px">{"Exemplos" if pt else "Examples"}</div>'
      +f'<div class="a" style="left:24px;top:470px;width:280px;font-size:12px;line-height:1.5;color:#5F5670">{note}</div>'+FOOT)
def credito(lang):
    pt=lang=='pt'
    return (header('cred',lang)+f'<div class="a lab" style="left:24px;top:74px">{"Casos de uso" if pt else "Use cases"}</div>'
      +'<div class="a" style="left:330px;top:74px;width:1px;height:610px;background:#E3DAEE"></div>'
      +'<div class="a" style="left:340px;top:162px;width:3px;height:34px;background:#D7F34A"></div>'
      +f'<div class="a lab" style="left:340px;top:208px">{"Gráficos indicados" if pt else "Suggested charts"}</div>'+FOOT)
def sobre():
    col=lambda x,h,facts,credit,refs,role:(f'<div class="a" style="left:{x}px;top:80px;width:420px"><div style="font:800 28px Brico,sans-serif;letter-spacing:-.5px">{h}</div>'
      +'<div style="margin-top:14px;border-top:1px solid #E3DAEE">'+''.join(f'<div style="padding:9px 0;border-bottom:1px solid #E3DAEE;font-size:14px">{f}</div>' for f in facts)+'</div>'
      +f'<div style="margin-top:16px;background:#F4ECFC;padding:12px 14px;border-radius:3px">{credit}</div>'
      +f'<div class="lab" style="margin-top:20px">{refs[0]}</div>'+''.join(f'<div style="padding:6px 0;border-bottom:1px solid #E3DAEE;font-size:13px;color:#4A4158"><b style="color:#211A2B">{a}</b> — {b}</div>' for a,b in refs[1])+'</div>')
    pt=col(340,'Sobre o autor',['10+ anos em operações de crédito','3+ anos em BI','Power BI · Python · SQL · Excel','Microsoft Certified: Power BI Data Analyst Associate (PL-300)'],'Ao compartilhar este guia ou as ilustrações, mantenha o crédito a Lucas Delfino (CC BY 4.0).',('Referências e inspirações',[('Financial Times · Visual Vocabulary','agrupar gráficos por objetivo.'),('Data to Viz','escolha por tipo de dado e armadilhas.'),('Guia em Power BI analisado','ponto de partida das perguntas.'),('Textos e ilustrações','originais de Lucas Delfino.')]),'')
    en=col(820,'About the author',['10+ years in credit operations','3+ years in BI','Power BI · Python · SQL · Excel','Microsoft Certified: Power BI Data Analyst Associate (PL-300)'],'When sharing this guide or its illustrations, please credit Lucas Delfino (CC BY 4.0).',('References and inspirations',[('Financial Times · Visual Vocabulary','grouping charts by goal.'),('Data to Viz','choosing by data type and pitfalls.'),('Power BI guide reviewed','starting point for the questions.'),('Texts and illustrations','original works by Lucas Delfino.')]),'')
    return (header('sobre','pt')+'<div class="a" style="left:24px;top:80px;width:200px;height:200px;border-radius:50%%;background:url(data:image/jpeg;base64,%s) center/cover"></div>'%AV
      +'<div class="a" style="left:24px;top:296px;font:800 34px/1.05 Brico,sans-serif;letter-spacing:-.6px">Lucas Delfino</div><div class="a" style="left:24px;top:338px;color:#5F5670">Data &amp; BI Analyst</div>'
      +'<div class="a" style="left:24px;top:376px;width:250px;height:38px;background:#7139B8;color:#fff;border-radius:3px;display:flex;align-items:center;justify-content:center;font-weight:600">Conectar · Connect on LinkedIn ↗</div>'
      +'<div class="a" style="left:24px;top:422px;width:250px;height:38px;border:1px solid #211A2B;color:#211A2B;border-radius:3px;display:flex;align-items:center;justify-content:center;font-weight:600">Portfólio · Portfolio ↗</div>'
      +'<div class="a" style="left:310px;top:80px;width:1px;height:590px;background:#E3DAEE"></div>'+pt+en+FOOT)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1.5)
        for name,body in [('fundo_guia_pt',guia('pt')),('fundo_guide_en',guia('en')),('fundo_credito_pt',credito('pt')),('fundo_st_pt',storytelling('pt')),('fundo_st_en',storytelling('en')),('fundo_credit_en',credito('en')),('fundo_sobre',sobre())]:
            await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'repo/imagens/fundos/{name}.png')
        await b.close()
asyncio.run(main())
