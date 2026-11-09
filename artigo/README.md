# Artigo para Overleaf

Arquivos necessarios para compilar o PDF:

1. `main.tex` — codigo LaTeX completo do artigo.
2. `biblioteca.bib` — referencias bibliograficas originais.
3. `referencias_novas.bib` — referencias acrescentadas na revisao.
4. `figura_probabilidades_copa_2026.png` — grafico usado com `\includegraphics`.

**Nao e necessario copiar o Python para o Overleaf.** O artigo compila separadamente do simulador.

No Overleaf, use `New Project` > `Upload Project` e envie o ZIP especifico do Overleaf, disponibilizado junto ao pacote. Em um projeto novo, escolha `main.tex` como arquivo principal e `pdfLaTeX` como compilador. O arquivo PDF nesta pasta e uma pre-visualizacao, nao o codigo fonte.

O comando de bibliografia do documento e `\bibliography{biblioteca,referencias_novas}`. Os nomes dos arquivos `.bib` precisam ser exatamente esses.

## Revisão TCC e GitHub (9 nov. 2026)

A seção 4.2 foi atualizada com base no TCC fornecido pelo autor: comparação Monte Carlo/Poisson versus RNA MLP, Elo Rating, forma recente, recorte histórico de 2006, avaliação temporal 90/10 e técnicas de regularização. A regressão linear e as 20 variáveis, que não correspondem ao desenho do TCC enviado, foram retiradas dessa seção.

Ao final da metodologia, foi incluída uma referência clicável ao repositório do projeto, com uma entrada bibliográfica em `referencias_novas.bib`. Essa referência descreve os materiais efetivamente disponibilizados, sem afirmar que as bases brutas nem os códigos do Brasileirão já estejam públicos.

**Fonte atualizada:** os arquivos `main.tex` e `.bib` refletem esta revisão. O PDF armazenado neste repositório ainda corresponde à compilação anterior; gere a versão atual no Overleaf com os arquivos-fonte ou utilize o PDF atualizado fornecido à parte.


## Avaliação de fases do torneio completo

A seção 3.1 inclui nova tabela comparando as probabilidades de avanço com a classificação observada: recuperação top-k e Brier binário por fase. Veja `../copa-do-mundo/codigos/avaliar_previsoes_fases_copa_2026.py` e `../copa-do-mundo/resultados/publicados/avaliacao_fases_copa_2026.csv`.

A versão fonte `main.tex` contém os dados mais recentes; compile no Overleaf para gerar o PDF atualizado. O PDF previamente incluído na pasta pode corresponder a uma versão anterior.
