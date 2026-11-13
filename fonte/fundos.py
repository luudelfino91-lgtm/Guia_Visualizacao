# -*- coding: utf-8 -*-
import asyncio, sys
from playwright.async_api import async_playwright
CSS='''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1280px;height:720px;background:#FAF7FE;font-family:'Inter',sans-serif;color:#211A2B;position:relative;overflow:hidden}
.glow1{position:absolute;left:-180px;top:-220px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(182,107,234,.20),rgba(182,107,234,0) 68%)}
.glow2{position:absolute;right:-220px;bottom:-260px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(231,197,255,.55),rgba(231,197,255,0) 68%)}
.sig{position:absolute;left:54px;top:24px;font-size:12px;letter-spacing:.6px;color:#6B5B80}
.dot{position:absolute;left:36px;top:27px;width:10px;height:10px;border-radius:5px;background:#D7F34A;border:1.5px solid #170E27}
.sig b{color:#170E27;font-weight:700;letter-spacing:.3px}
h1{position:absolute;left:34px;top:44px;font-size:36px;font-weight:800;letter-spacing:-.8px;color:#170E27}
h1 em{font-style:normal;color:#7139B8}
.sub{position:absolute;left:36px;top:92px;font-size:13px;color:#5E516F}
.pill{position:absolute;height:32px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;letter-spacing:.5px}
.lang{left:1096px;top:30px;width:148px;background:#fff;border:1px solid #E2CDF6}
.lang span{position:absolute;top:3px;height:24px;width:70px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.on{background:#7139B8;color:#fff}.off{color:#5E516F}
.about{left:972px;top:30px;width:112px;background:#fff;border:1px solid #E2CDF6;color:#7139B8;font-weight:600}
.step{position:absolute;top:116px;height:88px;border-radius:16px;background:#fff;border:1px solid #EBDDF8;box-shadow:0 6px 18px rgba(113,57,184,.07)}
.step .n{position:absolute;left:14px;top:10px;width:22px;height:22px;border-radius:11px;background:#7139B8;color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.step .t{position:absolute;left:44px;top:12px;font-size:13px;font-weight:700;letter-spacing:.2px}
.panel{position:absolute;left:24px;top:218px;width:1232px;height:470px;border-radius:22px;background:#fff;border:1px solid #EBDDF8;box-shadow:0 10px 30px rgba(113,57,184,.07)}
.foot{position:absolute;left:36px;top:700px;font-size:10.5px;color:#8A7B9C}
.foot2{position:absolute;right:36px;top:700px;font-size:10.5px;color:#8A7B9C}
.blk{position:absolute;top:150px;width:540px}
.blk h2{font-size:15px;color:#7139B8;font-weight:700;letter-spacing:.3px;margin-bottom:10px}
.blk p,.blk li{font-size:14px;line-height:1.55;color:#211A2B}
.blk ul{list-style:none}.blk li{margin-bottom:6px}
.blk li b{color:#7139B8}
.div{position:absolute;left:640px;top:150px;width:1px;height:480px;background:#E7C5FF}
'''
STEPS={'pt':['Objetivo','Variáveis','Análise temporal?','Categorias','Valores','Composição'],
       'en':['Goal','Variables','Time analysis?','Categories','Values','Composition']}
def guia(lang):
    pt=lang=='pt'
    xs=[35+i*204 for i in range(6)]
    steps=''.join(f'<div class="step" style="left:{x}px;width:190px"><div class="n">{i+1}</div><div class="t">{STEPS[lang][i]}</div></div>' for i,x in enumerate(xs))
    title='Qual <em>gráfico</em> usar?' if pt else 'Which <em>chart</em> should I use?'
    sub='Responda às perguntas e veja só os gráficos que fazem sentido para o seu dado.' if pt else 'Answer the questions and see only the charts that fit your data.'
    lg=('<span class="on" style="left:3px">PT</span><span class="off" style="left:75px">EN</span>' if pt else '<span class="off" style="left:3px">PT</span><span class="on" style="left:75px">EN</span>')
    return f'''<div class="glow1"></div><div class="glow2"></div>
<div class="dot"></div><div class="sig"><b>Lucas Delfino</b> &nbsp;·&nbsp; Data Analytics · BI · AI</div><h1>{title}</h1><div class="sub">{sub}</div>
<div class="pill about">{'ⓘ  Sobre' if pt else 'ⓘ  About'}</div><div class="pill lang">{lg}</div>
{steps}<div class="panel"></div>
<div class="foot">{'Taxonomia inspirada em guias abertos de visualização. Textos e ilustrações originais.' if pt else 'Taxonomy inspired by open visualization guides. Original texts and illustrations.'}</div>
<div class="foot2">github.com/luudelfino91-lgtm/Guia_Visualizacao</div>'''
def sobre():
    return '''<div class="glow1"></div><div class="glow2"></div>
<div class="dot"></div><div class="sig"><b>Lucas Delfino</b> &nbsp;·&nbsp; Data Analytics · BI · AI</div><h1>Sobre <em>este guia</em> · About</h1>
<div class="sub">Clareza primeiro. / Clarity first.</div>
<div class="pill about" style="left:1012px;width:110px">← Guia</div><div class="pill about" style="left:1134px;width:110px">Guide →</div>
<div class="div"></div>
<div class="blk" style="left:48px"><h2>COMO USAR</h2><ul>
<li><b>1.</b> Escolha o <b>objetivo</b>: o que você quer mostrar?</li>
<li><b>2.</b> Responda sobre variáveis, tempo, categorias e valores. Todas são opcionais.</li>
<li><b>3.</b> Veja os cartões. Cada um traz quando usar, o cuidado principal e como fazer no Power BI.</li></ul>
<h2 style="margin-top:26px">PRINCÍPIOS</h2><ul>
<li>O gráfico serve à pergunta, não o contrário.</li>
<li>Selo <b>Use com cuidado</b>: gráficos que costumam confundir.</li>
<li>Nenhum guia substitui testar com o seu público.</li></ul>
<h2 style="margin-top:26px">FONTES E INSPIRAÇÕES</h2><ul>
<li>Financial Times Visual Vocabulary</li><li>Data Viz Project · Data to Viz · Data Viz Catalogue</li></ul></div>
<div class="blk" style="left:690px"><h2>HOW TO USE</h2><ul>
<li><b>1.</b> Pick a <b>goal</b>: what do you want to show?</li>
<li><b>2.</b> Answer about variables, time, categories and values. All are optional.</li>
<li><b>3.</b> Browse the cards. Each shows when to use it, the main caution and how to build it in Power BI.</li></ul>
<h2 style="margin-top:26px">PRINCIPLES</h2><ul>
<li>The chart serves the question, not the other way around.</li>
<li><b>Use with care</b> badge: charts that tend to mislead.</li>
<li>No guide replaces testing with your audience.</li></ul>
<h2 style="margin-top:26px">SOURCES AND INSPIRATION</h2><ul>
<li>Financial Times Visual Vocabulary</li><li>Data Viz Project · Data to Viz · Data Viz Catalogue</li></ul></div>
<div class="foot">Textos e ilustrações originais. / Original texts and illustrations.</div>
<div class="foot2">github.com/luudelfino91-lgtm/Guia_Visualizacao</div>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1.5)
        for name,body in [('fundo_guia_pt',guia('pt')),('fundo_guide_en',guia('en')),('fundo_sobre',sobre())]:
            await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'repo/imagens/fundos/{name}.png')
        await b.close()
asyncio.run(main())
