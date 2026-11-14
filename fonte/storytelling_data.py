# -*- coding: utf-8 -*-
import pandas as pd
BASE='https://raw.githubusercontent.com/luudelfino91-lgtm/Guia_Visualizacao/main/imagens/storytelling'
TOP=[
('contexto',('Entenda o contexto','Understand the context'),('Antes de abrir o Power BI, defina quem vai ver, o que precisa decidir e como vai receber o dado.','Before opening Power BI, define who will see it, what they must decide and how they will receive the data.'),
 [('Escreva em uma frase quem é o público e que decisão ele toma.','Write in one sentence who the audience is and what decision they make.'),('Defina a ideia principal: o que a pessoa deve lembrar se esquecer o resto?','Define the big idea: what should they remember if they forget everything else?'),('Escolha o formato: relatório para explorar ou apresentação para explicar.','Pick the format: a report to explore or a presentation to explain.')],
 ('Só o gráfico, sem dizer para quem nem para quê.','Just the chart, without saying for whom or why.'),('Quem, decisão e ideia principal antes do gráfico.','Who, decision and big idea before the chart.')),
('escolher',('Escolha o gráfico certo','Pick the right chart'),('O gráfico é a resposta a uma pergunta, não um enfeite.','A chart is the answer to a question, not decoration.'),
 [('Comece pela pergunta: comparar, acompanhar no tempo, mostrar partes ou relacionar?','Start with the question: compare, track over time, show parts or relate?'),('Prefira barras e linhas: o olho mede comprimento e posição melhor que ângulo.','Prefer bars and lines: the eye reads length and position better than angle.'),('Use a aba Guia deste projeto para filtrar as opções.','Use this project\'s Guide tab to filter the options.')],
 ('Pizza com sete fatias: difícil comparar.','Pie with seven slices: hard to compare.'),('Barras ordenadas: a comparação é imediata.','Sorted bars: the comparison is immediate.')),
('ruido',('Elimine o ruído','Remove the clutter'),('Tudo o que não ajuda a entender atrapalha.','Whatever does not help understanding gets in the way.'),
 [('Remova bordas, grades pesadas e legendas repetidas.','Remove borders, heavy gridlines and repeated legends.'),('Mostre só os rótulos que importam.','Show only the labels that matter.'),('Teste: tire o elemento. Se ninguém sentir falta, ele sai.','Test it: remove the element. If nobody misses it, it stays out.')],
 ('Grade, borda, legenda e rótulo em todas as colunas.','Grid, border, legend and a label on every column.'),('Só o necessário: colunas leves e um rótulo.','Only what is needed: light columns and one label.')),
('olhar',('Direcione o olhar','Direct the eye'),('Cor, tamanho e posição dizem onde olhar primeiro.','Color, size and position say where to look first.'),
 [('Deixe tudo em lavanda ou cinza claro e destaque um elemento com a cor de ação.','Keep everything light lavender or gray and highlight one element with the action color.'),('Use no máximo uma cor de destaque por gráfico.','Use at most one highlight color per chart.'),('Ponha o mais importante no alto, à esquerda.','Put the most important thing at the top left.')],
 ('Tudo com o mesmo peso: o olho não sabe onde parar.','Everything has the same weight: the eye does not know where to stop.'),('Um destaque só e uma frase curta.','One highlight and one short phrase.')),
('designer',('Pense como designer','Think like a designer'),('Alinhamento, espaço em branco e hierarquia fazem o relatório parecer profissional.','Alignment, white space and hierarchy make a report look professional.'),
 [('Alinhe tudo a uma grade e mantenha margens iguais.','Align everything to a grid and keep margins equal.'),('Use dois ou três tamanhos de texto, não dez.','Use two or three text sizes, not ten.'),('Deixe espaço em branco: ele separa e descansa.','Leave white space: it separates and rests the eye.')],
 ('Textos soltos, tamanhos aleatórios, nada alinhado.','Loose text, random sizes, nothing aligned.'),('Mesma informação, com grade e hierarquia.','Same information, with a grid and hierarchy.')),
('historia',('Conte uma história','Tell a story'),('Uma boa história tem começo, virada e ação.','A good story has a beginning, a turn and an action.'),
 [('Contexto: onde estamos?','Context: where are we?'),('Virada: o que mudou ou o que descobrimos?','Turn: what changed or what did we find?'),('Ação: o que queremos que seja feito?','Action: what do we want done?')],
 ('Quatro gráficos soltos: cada pessoa conta uma história.','Four loose charts: everyone tells their own story.'),('Três passos, um gráfico por passo.','Three steps, one chart per step.')),
('titulo',('Escreva títulos que concluem','Write titles that conclude'),('O título deve dizer o que o dado mostra.','The title should say what the data shows.'),
 [('Troque "Vendas por mês" por uma frase com o resultado e o número.','Swap "Sales by month" for a sentence with the result and the number.'),('Coloque o título à esquerda, no alto.','Place the title at the top left.'),('Use o subtítulo para período e unidade.','Use the subtitle for period and unit.')],
 ('Título que só descreve o eixo.','A title that only describes the axis.'),('Título com a conclusão e o trecho destacado.','A title with the conclusion and the highlighted stretch.')),
('rotulos',('Rotule direto no gráfico','Label directly on the chart'),('Quanto menos o olho viaja, mais rápido a mensagem chega.','The less the eye travels, the faster the message arrives.'),
 [('Escreva o nome da série no fim da linha.','Write the series name at the end of the line.'),('Tire a legenda quando houver até cinco séries.','Drop the legend when there are up to five series.'),('Mantenha a mesma cor entre rótulo e série.','Keep the same color for label and series.')],
 ('Legenda embaixo: o olho vai e volta.','Legend at the bottom: the eye goes back and forth.'),('Nome no fim de cada linha.','Name at the end of each line.')),
]
t=[];p=[];e=[]
for i,(slug,ti,id_,steps,a,d) in enumerate(TOP,1):
    t.append(dict(id_topico=i,ordem=i,slug=slug,titulo_pt=ti[0],titulo_en=ti[1],ideia_pt=id_[0],ideia_en=id_[1]))
    for j,(sp,se) in enumerate(steps,1): p.append(dict(id_passo=i*10+j,id_topico=i,ordem=j,texto_pt=f'{j}. {sp}',texto_en=f'{j}. {se}'))
    for j,(k,rp,re_,cap) in enumerate([('antes','Antes','Before',a),('depois','Depois','After',d)],1):
        e.append(dict(id_exemplo=i*10+j,id_topico=i,ordem=j,rotulo_pt=rp,rotulo_en=re_,legenda_pt=f'{rp}: {cap[0]}',legenda_en=f'{re_}: {cap[1]}',imagem_pt=f'{BASE}/{slug}_{k}_pt.png',imagem_en=f'{BASE}/{slug}_{k}_en.png'))
for n,d in [('dim_topico',t),('dim_passo',p),('dim_exemplo',e)]: pd.DataFrame(d).to_csv(f'repo/dados/{n}.csv',index=False,encoding='utf-8')
print(len(t),len(p),len(e))
