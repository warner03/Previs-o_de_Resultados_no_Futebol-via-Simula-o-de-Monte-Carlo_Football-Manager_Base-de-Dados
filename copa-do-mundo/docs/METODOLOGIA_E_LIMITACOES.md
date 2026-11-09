# Metodologia, cenario e limites

## Fluxo da simulacao

1. Calcular um score de cada selecao com variaveis agregadas do Football Manager, ranking FIFA e treinador.
2. Converter scores relativos em medias Poisson (`lambda_A = 1.35 score_A/score_B`; idem para B). A implementacao aplica bonus heuristico aos anfitrioes.
3. Sortear placares de seis jogos por grupo, computar classificacao dos 12 grupos, selecionar oito terceiros classificados.
4. Usar as 495 combinacoes do Anexo C da FIFA para o chaveamento da fase de 32 equipes.
5. Simular os jogos eliminatorios: se houver empate, 30 minutos adicionais com media `lambda/3`; persistindo empate, decisao aleatoria ponderada por score e nota do goleiro.
6. Repetir o torneio N vezes; estimar `P(fase)` e `P(campeao)` por frequencia relativa.

## Original vs extensao

O codigo historico fornecido indicava 10 mil simulacoes no valor padrao da funcao, mas sua chamada de avaliacao usava explicitamente 5 mil amostras de cada jogo. A extensao principal produziu **50 mil simulacoes do torneio inteiro**, nao 50 mil simulacoes separadas para todos os possiveis confrontos.

O artigo registra o Brier Score = 0,5427 e 67/104 acertos historicos da planilha original. A validacao recalculada pelo codigo corrigido registra 70/104 com Brier aproximado 0,54264, mas nao equivale estritamente a desempenho 90min, pois alguns placares do mata-mata correspondem ao jogo apos prorrogacao. Portanto, os 70 acertos **nao devem substituir** os 67 sem adequar o criterio de validacao.

## Hipoteses/limitacoes

- Modelo Poisson independente e pesos de score heurísticos, sem calibracao formal.
- Base com selecionados insuficientes para preencher todas as posicoes em algumas equipes.
- Distribuicao de penalidades heuristica: formula ajustada para assegurar `P(A)+P(B)=1`; nao constitui estimativa empiricamente calibrada de disputa de penaltis.
- Tempo extra aproximado por taxas Poisson `lambda/3` e independencia de gols; faltam dados de substituicoes e desgaste.
- Criterios de fair play da FIFA nao disponiveis, substituidos por ranking do modelo quando nao ha desempate pelos demais criterios.
- Aproximacao no fator casa: a sede exata de cada partida nao e parametrizada.
- Necessario verificar datas de extracao e direitos de redistribuicao dos dados de Football Manager.
- O artigo em LaTeX e uma versao editorial preliminar. Adaptar ao template da revista antes da submissao.


## Avaliação retrospectiva da classificação

Com as 50.000 simulações completas, calcula-se a probabilidade de cada uma das 48 seleções alcançar cada fase. Para cada etapa, selecionam-se as k seleções mais prováveis, com k = 32, 16, 8, 4, 2 ou 1. A recuperação top-k é a proporção dos classificados reais nesse conjunto; **não** é acurácia de jogos individuais.

O Brier Score binário, calculado com todas as 48 seleções, compara cada probabilidade prevista à ocorrência ou não da classificação. A referência uniforme utiliza a proporção k/48. Os números constam em `resultados/publicados/avaliacao_fases_copa_2026.csv` e são reproduzidos pelo script `codigos/avaliar_previsoes_fases_copa_2026.py`.

A análise é retrospectiva, baseia-se em apenas uma Copa e não comprova calibração nem descarta possível vazamento temporal dos atributos do Football Manager. O Brier binário por fase difere do Brier multiclasse de partidas.
