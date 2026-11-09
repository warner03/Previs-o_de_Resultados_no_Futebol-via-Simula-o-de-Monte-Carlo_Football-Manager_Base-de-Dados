# Previsão de Resultados no Futebol via Monte Carlo e Football Manager

Repositório acadêmico conjunto com duas frentes de pesquisa: **Copa do Mundo de 2026** e **Campeonato Brasileiro**. O artigo científico pertence ao projeto geral. Cada frente mantém seus próprios códigos, dados e resultados em pastas separadas.

## Navegação

| Pasta ou arquivo | Conteúdo |
|---|---|
| [`artigo/`](artigo/) | Artigo conjunto em LaTeX, bibliografia, figuras e versão PDF |
| [`copa-do-mundo/`](copa-do-mundo/) | Pasta codigos/ com notebook de partidas, simulador completo e avaliador de fases; dados, resultados e testes |
| [`brasileirao/`](brasileirao/) | Pasta reservada ao segundo pesquisador; nenhum código ou dado foi adicionado |
| `README.md` | Esta apresentação geral |

## Pesquisa da Copa do Mundo

A simulação aplica **Poisson e Monte Carlo** a 48 seleções. Foram executados **50.000 torneios completos**, passando por fase de grupos, melhores terceiros colocados, mata-mata, prorrogação e pênaltis. **Não** significa 50 mil repetições independentes de cada confronto específico do mata-mata.

- [Explicação passo a passo do projeto](copa-do-mundo/docs/GUIA_PARA_INICIANTES.md)
- [Algoritmo principal](copa-do-mundo/codigos/simulacao_campeonato_completo_copa_2026.py)
- [Notebook para Google Colab](copa-do-mundo/codigos/simulacao_partidas_isoladas_copa_2026.ipynb)
- [Resultados das simulações](copa-do-mundo/resultados/publicados/)
- [Metodologia e limitações](copa-do-mundo/docs/METODOLOGIA_E_LIMITACOES.md)

Para executar, entre em `copa-do-mundo/` e siga as instruções do guia. O simulador usa parâmetros agregados publicados no repositório; as planilhas brutas do Football Manager não foram redistribuídas, em atenção aos direitos de uso dos dados.

## Artigo conjunto e Overleaf

Em [`artigo/`](artigo/), baixe os arquivos `main.tex`, `biblioteca.bib`, `referencias_novas.bib` e `figura_probabilidades_copa_2026.png` para compilar no Overleaf. Consulte [as instruções detalhadas](artigo/README.md).

## Organização colaborativa

A pasta `brasileirao/` contém somente um `.gitkeep`, arquivo técnico para o GitHub exibir uma pasta sem conteúdo. Os dois pesquisadores podem desenvolver seus estudos sem misturar códigos ou bases; o artigo permanece compartilhado.

Os resultados da Copa distinguem a avaliação histórica (67 acertos em 104 partidas) do recálculo e do experimento de torneios completos. Consulte os limites metodológicos antes de apresentar métricas como previsões estritas dos 90 minutos.

**Autoria, licença e dados:** os direitos e a licença de distribuição devem ser acordados pelos autores. O repositório não atribui uma licença open source automaticamente.

## Avaliação adicional

O script [`avaliar_previsoes_fases_copa_2026.py`](copa-do-mundo/codigos/avaliar_previsoes_fases_copa_2026.py) compara as probabilidades das 50.000 Copas completas com as fases efetivamente alcançadas pelas seleções: recuperação top-k e Brier binário por fase. Essa avaliação **não** se confunde com a acurácia dos resultados dos 104 jogos. Os detalhes constam no artigo atualizado.
