# Guia de Visualização · Visualization Guide
**Lucas Delfino** · Data Analytics · BI · AI

Guia interativo, em português e inglês, para escolher o gráfico certo no Power BI. / Interactive bilingual guide to pick the right chart in Power BI.

## Conteúdo / Contents
| Pasta / Folder | O que tem / What it has |
|---|---|
| `dist/Guia_Visualizacao_Lucas_Delfino.pbit` | Modelo do Power BI (template). / Power BI template. |
| `dados/` | 5 tabelas em CSV: `dim_grafico` (59 gráficos), `dim_objetivo`, `fato_selecao`, `dim_caso` (12 casos), `ponte_caso_grafico`. / 3 CSV tables. |
| `imagens/graficos/` | 59 ilustrações PNG usadas nos cartões (links públicos). / 59 PNG illustrations used on the cards. |
| `imagens/fundos/` | Fundos das 3 páginas do relatório. / Page backgrounds. |
| `tema/LucasDelfino.json` | Tema do Power BI (opcional). / Optional Power BI theme. |

## Como abrir / How to open
1. Publique este repositório no GitHub (branch `main`). / Publish this repo on GitHub (branch `main`).
2. Abra o `.pbit` no Power BI Desktop. / Open the `.pbit` in Power BI Desktop.
3. Se pedir credenciais da Web, escolha **Anônimo** e **Conectar**. / If asked for Web credentials, choose **Anonymous**.
4. Salve como `.pbix`. / Save as `.pbix`.

Os dados e as imagens são lidos de `https://raw.githubusercontent.com/luudelfino91-lgtm/Guia_Visualizacao/main/...`. Para atualizar o guia, edite os CSVs e clique em **Atualizar**. / Data and images load from the raw GitHub URLs; edit the CSVs and hit **Refresh** to update.

## Como funciona a filtragem / How filtering works
Célula vazia no original significa "tanto faz": cada linha foi expandida para todas as opções aplicáveis, então um filtro nunca esconde um gráfico válido. / An empty cell means "any": rows are expanded to every applicable option, so a filter never hides a valid chart.

## Créditos e licença / Credits
Textos e ilustrações originais de **Lucas Delfino**, sob **CC BY 4.0** (veja `LICENSE.md`): cite o autor ao reutilizar. Taxonomia inspirada em guias abertos (Financial Times Visual Vocabulary, Data to Viz, Data Viz Project, Data Viz Catalogue); nenhum texto ou imagem deles foi copiado. O visual **Card Browser** é da Microsoft (MIT). / Original texts and illustrations by **Lucas Delfino**, under **CC BY 4.0** (see `LICENSE.md`): please credit the author. Taxonomy inspired by open guides; none of their text or images were copied. The Card Browser visual is by Microsoft (MIT).
